from dataclasses import dataclass # structuring
from typing import List
import struct

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
        records = [] # creates empty list to hold all records
        with open(filename, "rb") as f: # opens in read binary mode
            record_count_bytes = f.read(4) # reads 4 bytes ti get number of records
            if not record_count_bytes:
                return records
            record_count = struct.unpack("<I", record_count_bytes)[0] # convert first 4 bytes into integer

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

                records.append(CreditRecord(sin, name, address, credit_score, account_count, major_flags, accounts))
        return records