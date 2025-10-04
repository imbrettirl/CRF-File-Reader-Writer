from dataclasses import dataclass # structuring
from typing import List

import struct
import zlib

from cryptography.fernet import Fernet
import io

Magic_Number = b"CRF"
Footer = b"CRF_END"

@dataclass
class Account:
    name: str
    balance: int

@dataclass
class CreditRecord:
    sin: str
    name: str
    address: str
    credit_score: int
    account_count: int
    major_flags: int
    accounts: List[Account]

@dataclass
class FileMetaData:
    version: int
    record_count: int

class CreditReportReader:
    @staticmethod
    def read_string(f):
        length_bytes = f.read(4) # reads first 4 bytes
        if not length_bytes: # checks if end of the file
            return None
        length = struct.unpack("<I", length_bytes)[0] # converts 4 bytes into int
        return f.read(length).decode("utf-8") # converts back into python string
    
    @staticmethod
    def read_file(filename: str, encryption_key: bytes):

        with open(filename, "rb") as file:
            encrypted_data = file.read() # read encrypted data from file

        try:
            fernet = Fernet(encryption_key) # uses encryption key to decrpyt
            decrypted_data = fernet.decrypt(encrypted_data)
        except Exception as e:
            raise ValueError(f"Decryption failed. Invalid key or corrupted file: {e}")

        f = io.BytesIO(decrypted_data) # parse decrypted data from in-memory buffer

        if f.read(3) != Magic_Number: # error handling for non crf files
            raise ValueError("Invalid File Format.")
        
        version = struct.unpack("<H", f.read(2))[0]
        if version < 1 or version > 2:
            raise ValueError(f"Unsupported file version: {version}")

        record_count = struct.unpack("<I", f.read(4))[0]
        index_size = struct.unpack("<I", f.read(4))[0]
        f.read(index_size)
        records = [] # creates empty list to hold records

        for _ in range(record_count):
            sin = CreditReportReader.read_string(f)
            name = CreditReportReader.read_string(f)
            address = CreditReportReader.read_string(f)
            credit_score = struct.unpack("<I", f.read(4))[0]
            account_count = struct.unpack("<I", f.read(4))[0]
            major_flags = struct.unpack("<I", f.read(4))[0]

            accounts = []
            for _ in range(account_count):
                acc_name = CreditReportReader.read_string(f)
                balance = struct.unpack("<i", f.read(4))[0]
                accounts.append(Account(acc_name, balance))

            records.append(CreditRecord(sin, name, address, credit_score, account_count, major_flags, accounts))

        footer = f.read(len(Footer))
        if footer != Footer:
            raise ValueError("Invalid Footer.")
        
        footer_record_count = struct.unpack("<I", f.read(4))[0]
        checksum_stored = struct.unpack("<I", f.read(4))[0]

        f.seek(-len(Footer)-4-4, 2) # finds footer start
        footer_data = f.read(len(Footer)+4)
        checksum_calculated = zlib.crc32(footer_data) # verify the checksum

        if checksum_calculated != checksum_stored:
            raise ValueError("Checksum mismatch.")
        if footer_record_count != record_count:
            raise ValueError("Record count mismatch.")

        return records
    
    @staticmethod
    def read_metadata(filename: str, encryption_key: bytes) -> FileMetaData:
        with open(filename, "rb") as file:
            encrypted_data = file.read()

        try:
            fernet = Fernet(encryption_key)
            decrypted_data = fernet.decrypt(encrypted_data)
        except Exception as e:
            raise ValueError(f"Decryption failed: {e}")
        
        f = io.BytesIO(decrypted_data)

        if f.read(3) != Magic_Number:
            raise ValueError("Invalid File Format.")
        
        version = struct.unpack("<H", f.read(2))[0]
        record_count = struct.unpack("<I", f.read(4))[0]

        return FileMetaData(version = version, record_count = record_count)