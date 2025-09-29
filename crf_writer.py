from dataclasses import dataclass # for easy structuring https://docs.python.org/3/library/dataclasses.html 
from typing import List # imported for readability https://docs.python.org/3/library/typing.html

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

