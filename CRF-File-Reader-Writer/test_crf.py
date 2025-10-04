from crf_writer import CreditReportWriter, CreditRecord, Account
from crf_reader import CreditReportReader
import os

# Sample data set 1
sample_1_records = [
    CreditRecord(
        sin="111111111",
        name="Blah blah man",
        address="111 blah street",
        credit_score=111,
        account_count=1,
        major_flags=1,
        accounts=[
            Account("Chequing", 11)
        ]
    ),
    CreditRecord(
        sin="987-654-321",
        name="Johnson johnson",
        address="587 John st NW",
        credit_score=500,
        account_count=2,
        major_flags=1,
        accounts=[
            Account("Chequing", 2000),
            Account("Line of Credit", -5000)
        ]
    ),
    CreditRecord(
        sin="676767676",
        name="Carol Williams",
        address="1340 4 ave, Calgary, AB",
        credit_score=800,
        account_count=4,
        major_flags=0,
        accounts=[
            Account("Chequing", 10000),
            Account("Savings", 50000),
            Account("Investment", 100001),
            Account("Credit Card", -1000)
        ]
    )
]

# Sample data set 2
sample_2_records = [
    CreditRecord(
        sin="111-222-333",
        name="David Chen",
        address="483 University Dr, Calgary, AB",
        credit_score=670,
        account_count=2,
        major_flags=3,
        accounts=[
            Account("Chequing", 500),
            Account("Credit Card", -8000)
        ]
    ),
    CreditRecord(
        sin="123456789",
        name="Samantha Liu",
        address="64 North St, North Pole",
        credit_score=710,
        account_count=3,
        major_flags=1,
        accounts=[
            Account("Chequing", 3000),
            Account("Savings", 12000),
            Account("Auto Loan", -1500000)
        ]
    )
]

script_dir = os.path.dirname(os.path.abspath(__file__)) # finds file path of test script

key_1 = CreditReportWriter.generate_key() # generates encryption keys
key_2 = CreditReportWriter.generate_key()

file_path_1 = os.path.join(script_dir, "sample_1.crf")
file_path_2 = os.path.join(script_dir, "sample_2.crf")

print("Writing CRF files")
CreditReportWriter.write_file(file_path_1, sample_1_records, key_1) # calls writer to write into 2 filepaths, 2 different records and 2 different keys
CreditReportWriter.write_file(file_path_2, sample_2_records, key_2)
print(f"CRF 1 File Created: {file_path_1}")
print(f"CRF 2 File Created: {file_path_2}")

keys_file = os.path.join(script_dir, "encryption_keys.txt") # stores keys in text file, will be stored in secure database, etc.
with open(keys_file, "w") as f:
    f.write(f"sample_1.crf key: {key_1.decode()}\n")
    f.write(f"sample_2.crf key: {key_2.decode()}\n")
print(f"Keys saved to: {keys_file}") # saves decoded keys to encryption_keys.txt file

if __name__ == "__main__":
    print("\n" + "="*60)
    print("Reading and displaying sample_1.crf:") # aesthetic printing for visibility
    print("="*60)
    
    try:
        metadata_1 = CreditReportReader.read_metadata(file_path_1, key_1)
        print(f"\nFile 1 Metadata:")
        print(f"  Version: {metadata_1.version}")
        print(f"  Record Count: {metadata_1.record_count}")
    except Exception as e:    
        print(f"Error reading metadata: {e}")

    try:
        records_1 = CreditReportReader.read_file(file_path_1, key_1) # call reader
        for i, record in enumerate(records_1, 1): # enumerates records starting at 1
            print(f"\nRecord {i}:") # displays what record is being displyed
            print(f"  SIN (hashed): {record.sin}")
            print(f"  Name: {record.name}")
            print(f"  Address: {record.address}")
            print(f"  Credit Score: {record.credit_score}")
            print(f"  Major Flags: {record.major_flags}")
            print(f"  Accounts:")
            for acc in record.accounts:
                print(f"    - {acc.name}: ${acc.balance:,}") # loop to print all that records accounts
    except Exception as e:
        print(f"Error reading sample_1.crf: {e}") # simple error handling

    print("\n" + "="*60)
    print("Reading and displaying sample_2.crf:") # divider for sample data 2
    print("="*60)
    
    try:
        metadata_2 = CreditReportReader.read_metadata(file_path_2, key_2)
        print(f"\nFile 2 Metadata:")
        print(f"  Version: {metadata_2.version}")
        print(f"  Record Count: {metadata_2.record_count}")
    except Exception as e:    
        print(f"Error reading metadata: {e}")

    try:
        records_2 = CreditReportReader.read_file(file_path_2, key_2)
        for i, record in enumerate(records_2, 1):
            print(f"\nRecord {i}:")
            print(f"  SIN (hashed): {record.sin}")
            print(f"  Name: {record.name}")
            print(f"  Address: {record.address}")
            print(f"  Credit Score: {record.credit_score}")
            print(f"  Major Flags: {record.major_flags}")
            print(f"  Accounts:")
            for acc in record.accounts:
                print(f"    - {acc.name}: ${acc.balance:,}")
    except Exception as e:
        print(f"Error reading sample_2.crf: {e}")

    print("\n" + "="*60)
    print("Testing encryption security (wrong key):") # key testing
    print("="*60)
    try:
        CreditReportReader.read_file(file_path_1, key_2)  # wrong key
        print("This text shouldn't display")
    except Exception as e:
        print(f"Incorrect key used: {type(e).__name__}") # should skip to this error message with wrong key