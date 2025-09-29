from dataclasses import datalclass # structuring

@datalclassclass
class CreditRecord:
    sin: str
    name: str
    address: str

class CreditReportReader:
    @staticmethod
    def read_string(f):
        line = f.readline() # returns line from the file
        if not line:
            return None
        return line.strip().decode("utf-8") # removes spaces & decodes
    
    @staticmethod
    def read_file(filename):
        records = []
        with open(filename, "rb") as f: # rb means read binary
            while True: # checks for a sin to keep reading
                sin = CreditReportReader.read_string(f)
                if sin is None:
                    break
                name = CreditReportReader.read_string(f)
                address = CreditReportReader.read_string(f)
                records.append(CreditRecord(sin, name, address))

        return records
    
if __name__ == "__main__":
    for record in CreditReportReader.read_file("sample.crf"):
        print(record)