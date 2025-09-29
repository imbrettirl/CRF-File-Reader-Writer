from crf_writer import CreditReportWriter, CreditRecord, Account # access writer
from crf_reader import CreditReportReader

import os

# sample data
records = [
    CreditRecord(
        sin="111 111 111",
        name="Blah Blah",
        address="111 Blah Street",
        credit_score=1,
        account_count=1,
        major_flags=1,
        accounts=[Account("Chequing", 1)]
    ),
    CreditRecord(
        sin="222 222 222",
        name="two man",
        address="222 two Street",
        credit_score=2,
        account_count=2,
        major_flags=9,
        accounts=[Account("Savings", 500), Account("Credit", -100)]
    )
]

script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "sample.crf")

CreditReportWriter.write_file(file_path, records) # saving to script directory

if __name__ == "__main__":
    for record in CreditReportReader.read_file("sample.crf"):
        print(record)

