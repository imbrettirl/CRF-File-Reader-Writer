from dataclasses import dataclass # structuring
from typing import List

import struct
import zlib

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

class CreditReportReader:
    @staticmethod
    def read_string(f):
        length_bytes = f.read(4) # reads first 4 bytes
        if not length_bytes: # checks if end of the file
            return None
        length = struct.unpack("<I", length_bytes)[0] # converts 4 bytes into int
        return f.read(length).decode("utf-8") # converts back into python string
    
    @staticmethod
    def read_file(filename):

        with open(filename, "rb") as f: # opens in read binary mode
            if f.read(3) != Magic_Number: # Error handling for non CRF files
                raise ValueError("Invalid File Format.")
            
            record_count = struct.unpack("<I", f.read(4))[0] # convert first 4 bytes into integer
            records = [] # creates empty list to hold all records

            for _ in range(record_count): # loop for each record
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

                records.append(CreditRecord(sin, name, address, credit_score, account_count, major_flags, accounts)) # appends all data onto record

            footer = f.read(len(Footer))
            if footer != Footer: # Error handling for incorrect footer
                raise ValueError("Invalid Footer.")
            
            footer_record_count = struct.unpack("<I", f.read(4))[0]
            checksum_stored = struct.unpack("<I", f.read(4))[0] # reading CRC32 checksum

            # calculate the checksum
            f.seek(-len(Footer)-4-4, 2)  # go to footer start
            footer_data = f.read(len(Footer)+4) # reads footer bytes
            checksum_calculated = zlib.crc32(footer_data) # calculates CRC32 over footer

            if checksum_calculated != checksum_stored: #validatse footer
                raise ValueError("Checksum mismatch.")
            if footer_record_count != record_count:
                raise ValueError("Record count mismatch.")

        return records