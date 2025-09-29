from dataclasses import dataclass # for easy structuring https://docs.python.org/3/library/dataclasses.html 
from typing import List # imported for readability https://docs.python.org/3/library/typing.html

import struct # transition from plain-text to binary

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
    def write_file(filename: str, records: List[CreditRecord]):
        with open(filename, "wb") as f: # write in binary
            for record in records:
                CreditReportWriter.write_string(f, record.sin)
                CreditReportWriter.write_string(f, record.name)
                CreditReportWriter.write_string(f, record.address)
                f.write(struct.pack("<I", record.credit_score))
                f.write(struct.pack("<I", record.account_count))
                f.write(struct.pack("<I", record.major_flags))
                for acc in record.accounts:
                    CreditReportWriter.write_string(f, acc.name)
                    f.write(struct.pack("<i", acc.balance)) # signed 4-byte integer