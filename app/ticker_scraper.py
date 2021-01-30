from ftplib import FTP
from io import BytesIO


class FTPReader:

    def __init__(self):
        self.ftp = FTP("ftp.nasdaqtrader.com")
        self.ftp.login()

    def get_data_from_file(self, file_name: str):
        raw_data = BytesIO()
        self.ftp.retrbinary(f"RETR /SymbolDirectory/{file_name}", raw_data.write)
        # Cut out a couple extra rows of unnecessary data and headers
        processed_data = raw_data.getvalue().decode("utf-8").split("\r\n")[1:-2]

        return [row.split("|")[:2] for row in processed_data if len(row) > 1]


def main():

    reader = FTPReader()
    file_names = ["nasdaqlisted.txt", "otherlisted.txt", "mfundslist.txt"]

    ticker_symbols = []

    for file_name in file_names:
        ticker_symbols += reader.get_data_from_file(file_name)

    for (ticker_symbol, company_name) in ticker_symbols:
        print(f"{ticker_symbol}: {company_name}")


if __name__ == '__main__':
    main()
