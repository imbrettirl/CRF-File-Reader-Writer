from dataclasses import dataclass # for easy structuring https://docs.python.org/3/library/dataclasses.html 
from typing import List # imported for readability https://docs.python.org/3/library/typing.html

import struct # transition from plain-text to binary
import hashlib
import zlib

from cryptography.fernet import Fernet # fernet encryption taken from https://cryptography.io/en/latest/fernet/
import io

Magic_Number = b"CRF"
Footer = b"CRF_END"

@dataclass
class Account: # Type of account + Balance of that account
    name: str
    balance: int

@dataclass
class CreditRecord: # All info on the person and their accounts
    sin: str
    name: str
    address: str
    credit_score: int
    account_count: int
    major_flags: int
    accounts: List[Account]

class CreditReportWriter:
    @staticmethod
    def write_string(f, s: str):
        encoded = s.encode("utf-8") # converts to bytes
        f.write(struct.pack("<I", len(encoded))) # converts length into 4-byte unsigned integers & records length
        f.write(encoded) # writes UTF-8 encoded string

    @staticmethod
    def write_record(f, record: CreditRecord):
            hashed_sin = hashlib.sha256(record.sin.encode()).hexdigest() # converts sin into bytes, hashes with SHA-256 and then converted to hexadecimal string
            CreditReportWriter.write_string(f, hashed_sin)
            CreditReportWriter.write_string(f, record.name)
            CreditReportWriter.write_string(f, record.address)
            f.write(struct.pack("<I", record.credit_score))
            f.write(struct.pack("<I", record.account_count))
            f.write(struct.pack("<I", record.major_flags))
            for acc in record.accounts:
                CreditReportWriter.write_string(f, acc.name)
                f.write(struct.pack("<i", acc.balance)) # unsigned integer

    @staticmethod
    def write_file(filename: str, records: List[CreditRecord], encryption_key: bytes):

        buffer = io.BytesIO() # collect all data in buffer before encrpyting with fernet
        
        buffer.write(Magic_Number)
        buffer.write(struct.pack("<I", len(records)))

        for record in records:
            CreditReportWriter.write_record(buffer, record)

        footer_data = Footer + struct.pack("<I", len(records))
        checksum = zlib.crc32(footer_data)
        buffer.write(footer_data)
        buffer.write(struct.pack("<I", checksum))

        unencrypted_data = buffer.getvalue() # encrypted data is stored with all buffer data
        fernet = Fernet(encryption_key)
        encrypted_data = fernet.encrypt(unencrypted_data) # encrypt all the data

        with open(filename, "wb") as f:
            f.write(encrypted_data) # writes encrypted data

    @staticmethod
    def generate_key() -> bytes:
        return Fernet.generate_key() # generates encryption key