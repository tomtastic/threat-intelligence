#!/usr/bin/env python3
"""Take filenames and turn the CSV data into adblock hosts format"""

import csv
import sys
import re
import os.path

def main():
    # Check if at least one input file is provided
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} file1.csv [file2.csv ...]")
        sys.exit(1)

    output_file = "hosts"
    domains = set()  # Use a set to avoid duplicates

    # Process each input file
    for input_file in sys.argv[1:]:
        if not os.path.isfile(input_file):
            print(f"Warning: File '{input_file}' not found, skipping.")
            continue

        print(f"Processing {input_file}...")

        try:
            with open(input_file, 'r', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    # Check if this is a domain type indicator
                    if row.get('type') == 'domain':
                        # Clean up the domain (remove brackets)
                        indicator = row.get('indicator', '')
                        clean_domain = indicator.replace('[.]', '.')
                        domains.add(clean_domain)
        except Exception as e:
            print(f"Error processing {input_file}: {e}")

    # Write the hosts file
    with open(output_file, 'w') as f:
        f.write("# Hosts file generated from CSV\n")
        f.write("# Format: IP_ADDRESS DOMAIN_NAME\n\n")

        for domain in sorted(domains):
            f.write(f"127.0.0.1 {domain}\n")

    print(f"Hosts file created as '{output_file}' with {len(domains)} unique domains")

if __name__ == "__main__":
    main()

