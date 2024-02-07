# Identifies to whom the DNA sequence belong from csv and txt files
import csv
import sys


def main():

    # Check for command-line usage
    if len(sys.argv) != 3:
        print("Invalid number of arguments")
        sys.exit()

    # Read database file into a variable
    rows = []
    database_file = sys.argv[1]
    if database_file == 'databases/small.csv':
        sequences = ["AGATC", "AATG", "TATC"]
    elif database_file == 'databases/large.csv':
        sequences = ["AGATC", "TTTTTTCT", "AATG", "TCTAG", "GATA", "TATC", "GAAA", "TCTG"]
    with open(sys.argv[1], newline='') as file:
        database = csv.reader(file)
        header = next(database)
        for row in database:
            row_dict = {header[i]: int(value) if value.isdigit() else value for i, value in enumerate(row)}
            rows.append(row_dict)

    # Read DNA sequence file into a variable
    with open(sys.argv[2], 'r') as file:
        dna = file.read()

    # Find longest match of each STR in DNA sequence
    matches = {seq: longest_match(dna, seq) for seq in sequences}

    # Check database for matching profiles
    for row in rows:
        if all(row[seq] == matches[seq] for seq in sequences):
            print(row["name"])
            sys.exit()
    print("No match")


def longest_match(sequence, subsequence):

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
