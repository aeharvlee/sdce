from itertools import count
from sys import argv
import pandas as pd
import argparse
from datetime import datetime
from IPython.display import display
from tabulate import tabulate


def parse():
    parser = argparse.ArgumentParser(
        prog="sdce",
        usage="%(prog)s -f <file_path> -m <month>",
        description="Extract the self-development authentication statistics by given month.",
        add_help=True,
    )
    parser.add_argument(
        "-f",
        "--file",
        help="Indicate csv file to parse.",
    )
    parser.add_argument(
        "-mc",
        "--minimum",
        help="Minimum count of auth.",
    )
    parser.add_argument(
        "-m",
        "--month",
        help="Indicate which month's statistics are to be calculated.",
    )
    args = parser.parse_args()
    return args.file, args.minimum, args.month


def run(file_path, minimum_count, month):
    auth_text = "ㅇㅈㅎ"
    df = pd.read_csv(file_path)
    all_users = df["User"].unique()

    year = datetime.now().year
    month = "{:02d}".format(int(month))

    start_date = f"{year}-{month}-01 00:00:00"
    end_date = f"{year}-{month}-31 23:59:59"

    month_df = df[(df["Date"] >= start_date) & (df["Date"] <= end_date)]

    def contains_auth(msg: str) -> bool:
        if msg:
            if auth_text in msg:
                return True
        return False

    def remove_whitespace_at_name(name: str):
        name.strip()

    filtered_df = month_df[month_df["Message"].apply(contains_auth)]
    counted_df = filtered_df.groupby("User").count()
    counted_df = counted_df.drop("Message", axis=1)
    trimmed_names = list()
    for idx, row in counted_df.iterrows():
        trimmed_names.append(idx.translate(str.maketrans("", "", " \n\t\r")))
    counted_df = counted_df.reset_index()
    counted_df["User"] = trimmed_names

    zero_auth_users = set(all_users) - set(counted_df.index)
    print(f"============NoAuth Users=============")
    print(zero_auth_users)
    print(f"=========================")

    print(f"============Under {minimum_count}=============")
    print(
        tabulate(counted_df[counted_df["Date"] < 10], headers="keys", tablefmt="psql")
    )
    print(counted_df[counted_df["Date"] < 10].to_csv())
    print(f"=========================")

    print(f"============Successed Users=============")
    print(
        tabulate(counted_df[counted_df["Date"] >= 10], headers="keys", tablefmt="psql")
    )
    print(counted_df[counted_df["Date"] >= 10].to_csv())
    print(f"=========================")


def main():
    file_path, minimum, month = parse()
    run(file_path=file_path, minimum_count=minimum, month=month)


main()
