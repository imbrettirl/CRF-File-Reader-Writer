from dataclasses import dataclass # for easy structuring https://docs.python.org/3/library/dataclasses.html 
from typing import List # imported for readability https://docs.python.org/3/library/typing.html

import struct # transition from plain-text to binary
import hashlib
import zlib

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
            hashed_sin = hashlib.sha256(record.sin.encode()).hexdigest() # converts sin into bytes, hashes with SHA-256 and then converted to dexadecimal string
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
    def write_file(filename: str, records: List[CreditRecord]):
        with open(filename, "wb") as f: # write in binary

            f.write(Magic_Number) # header
            f.write(struct.pack("<I", len(records)))  # number of records

            for record in records:
                CreditReportWriter.write_record(f, record)

            footer_data = Footer + struct.pack("<I", len(records))
            checksum = zlib.crc32(footer_data) # detect accidental corruption, creates 4-byte footprint of footer data, https://docs.python.org/3/library/zlib.html
            f.write(footer_data)
            f.write(struct.pack("<I", checksum))