from dataclasses import dataclass  # for easy structuring https://docs.python.org/3/library/dataclasses.html
from typing import List, Dict       # imported for readability https://docs.python.org/3/library/typing.html
import struct                      # transition from plain-text to binary
import hashlib
import zlib
from cryptography.fernet import Fernet  # fernet encryption taken from https://cryptography.io/en/latest/fernet/
import io

Magic_Number = b"CRF"   # file identifier to recognize CRF files
VERSION = 2            # version number for compatibility checks
Footer = b"CRF_END"    # footer marker to indicate the end of the file

@dataclass
class Account:  # Type of account + Balance of that account
    name: str
    balance: int

@dataclass
class CreditRecord:  # All info on the person and their accounts
    sin: str
    name: str
    address: str
    credit_score: int
    account_count: int
    major_flags: int
    accounts: List[Account]

@dataclass
class FileMetadata:
    version: int
    record_count: int

class CreditReportWriter:
    @staticmethod
    def write_string(f, s: str):
        encoded = s.encode("utf-8")  # converts string to bytes
        f.write(struct.pack("<I", len(encoded)))  # converts length into 4-byte unsigned int & records length
        f.write(encoded)  # writes UTF-8 encoded string

    @staticmethod
    def write_record(f, record: CreditRecord, hashed_sin: str = None) -> int:
        start_pos = f.tell()  # determines starting position in the buffer
        
        if hashed_sin is None:
            # converts SIN into bytes, hashes with SHA-256, then converts to hexadecimal string
            hashed_sin = hashlib.sha256(record.sin.encode()).hexdigest()
        CreditReportWriter.write_string(f, hashed_sin)
        CreditReportWriter.write_string(f, record.name)
        CreditReportWriter.write_string(f, record.address)
        f.write(struct.pack("<I", record.credit_score))
        f.write(struct.pack("<I", record.account_count))
        f.write(struct.pack("<I", record.major_flags))
        for acc in record.accounts:
            CreditReportWriter.write_string(f, acc.name)
            f.write(struct.pack("<i", acc.balance))  # writes account balance as 4-byte signed integer
        
        end_pos = f.tell()  # determines ending position
        return end_pos - start_pos  # returns total size of the record

    @staticmethod
    def write_file(filename: str, records: List[CreditRecord], encryption_key: bytes):
        buffer = io.BytesIO()  # collect all data in memory before encrypting with Fernet
        
        # Write header
        buffer.write(Magic_Number)  # magic number for file identification
        buffer.write(struct.pack("<H", VERSION))  # 2-byte unsigned short version
        buffer.write(struct.pack("<I", len(records)))  # number of records as a 4-byte unsigned int
        
        # Build index in a temporary buffer first
        index: Dict[str, int] = {}
        temp_records = io.BytesIO()
        
        for record in records:
            # convert SIN into bytes and hash with SHA-256 for privacy/security
            hashed_sin = hashlib.sha256(record.sin.encode()).hexdigest()
            record_offset = temp_records.tell()  # current position relative to start of records
            index[hashed_sin] = record_offset    # store mapping of hashed SIN → record byte offset
            CreditReportWriter.write_record(temp_records, record, hashed_sin)
        
        # Write index block
        index_data = CreditReportWriter._serialize_index(index)  # builds a Python dictionary into a binary index
        buffer.write(struct.pack("<I", len(index_data)))         # writes size of index block as 4-byte int
        buffer.write(index_data)                                 # writes serialized index bytes
        
        # Write serialized records
        buffer.write(temp_records.getvalue())
        
        # Write footer
        footer_data = Footer + struct.pack("<I", len(records))  # footer marker + number of records as 4-byte int
        checksum = zlib.crc32(footer_data)                      # calculates CRC32 checksum for data integrity
        buffer.write(footer_data)                               # writes footer to buffer
        buffer.write(struct.pack("<I", checksum))              # writes checksum as 4-byte int
        
        # Encrypt final data
        unencrypted_data = buffer.getvalue()  # get full unencrypted binary data
        fernet = Fernet(encryption_key)
        encrypted_data = fernet.encrypt(unencrypted_data)  # encrypt entire buffer
        
        # Write encrypted data to disk
        with open(filename, "wb") as f:
            f.write(encrypted_data)  # writes encrypted CRF file

    @staticmethod
    def _serialize_index(index: Dict[str, int]) -> bytes:
        buffer = io.BytesIO()
        buffer.write(struct.pack("<I", len(index)))  # number of entries in the index
        for sin_hash, offset in index.items():
            CreditReportWriter.write_string(buffer, sin_hash)  # hash key
            buffer.write(struct.pack("<I", offset))            # byte offset for each record
        return buffer.getvalue()

    @staticmethod
    def generate_key() -> bytes:
        return Fernet.generate_key()  # generates encryption key
