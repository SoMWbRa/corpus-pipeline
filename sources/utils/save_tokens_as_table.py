import csv
import math


def split_into_columns(words, num_columns=3):
    num_rows = math.ceil(len(words) / num_columns)
    table = [words[i:i + num_rows] for i in range(0, len(words), num_rows)]
    return table


def save_as_csv(words, filename="tokenized_text.csv", num_columns=3):
    table = split_into_columns(words, num_columns)

    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for row in table:
            writer.writerow(row)

    print(f"CSV file '{filename}' saved successfully.")


def save_tokens_as_table(tokens):
    save_as_csv(tokens, "tokenized_text.csv", num_columns=10)
