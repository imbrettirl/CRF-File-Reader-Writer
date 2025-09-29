from crf_writer import CreditReportWriter, CreditRecord, Account # access writer
from crf_reader import CreditReportReader

# sample data 1
record = CreditRecord(
    sin="111 111 111",
    name="Blah Blah",
    address="111 Blah Street",
    credit_score=1,
    account_count=1,
    major_flags=1,
    accounts=[Account("Chequing", 1)]
)

CreditReportWriter.write_file("sample.crf", [record])

if __name__ == "__main__":
    for record in CreditReportReader.read_file("sample.crf"):
        print(record)