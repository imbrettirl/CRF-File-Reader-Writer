from dataclasses import dataclass # for easy structuring https://docs.python.org/3/library/dataclasses.html 
from typing import List # imported for readability https://docs.python.org/3/library/typing.html

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
    def write_file(filename: str, records: List[CreditRecord]):
        with open(filename, "wb") as f: # write in binary
            for record in records:
                f.write(record.sin.encode() + b"\n")
                f.write(record.name.encode() + b"\n")
                f.write(record.address.encode() + b"\n")
                f.write(str(record.credit_score).encode() + b"\n")
                f.write(str(record.account_count).encode() + b"\n")
                f.write(str(record.major_flags).encode() + b"\n")
                for acc in record.accounts:
                    f.write(acc.name.encode() + b"\n")
                    f.write(str(acc.balance).encode() + b"\n")
