import csv
from typing import List
from dataclasses import dataclass


@dataclass
class CSVData:
    rows: List[List[str]]


class CSVProcessor:
    def __init__(self, file_path):
        self.file_path = file_path
        # print("CSVProcessor now at this file path: ", self.file_path)
#         TODO add logger service


class CSVFileHandler(CSVProcessor):

    def __init__(self, file_path):
        super().__init__(file_path)
        self.csv_reader = None
        self.csv_data = None
        self.CSV_HEADER_SKIP = None

    def skip_csv_initial_headings(self):
        if self.CSV_HEADER_SKIP is not None:
            for _ in range(self.CSV_HEADER_SKIP):
                next(self.csv_reader)

    def read_file(self) -> CSVData:
        with open(self.file_path, mode='r') as csv_file:
            self.csv_reader = csv.reader(csv_file)
            self.skip_csv_initial_headings()
            rows = [row for row in self.csv_reader]
            self.csv_data = CSVData(rows=rows)
            return self.csv_data
