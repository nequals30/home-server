#!/usr/bin/env python3
from create_one_conf import create_one_conf

def main():
    """
    Processes a pipe-delimited file containing domain and port pairs, and generates
    NGINX server block configurations for each pair.
    """

    in_path = "services.txt"

    with open("services.txt", 'r') as file:
        for line in file:
            parts = line.split('|')
            if len(parts) == 2:
                domain = parts[0].strip()
                port = parts[1].strip()
                conf = create_one_conf(domain, int(port), True)
            elif len(parts) ==3:
                domain = parts[0].strip()
                port = parts[1].strip()
                host = parts[2].strip()
                conf = create_one_conf(domain, int(port), True, host=host)
            else:
                print(f"Skipping invalid line: {line.strip()}")

if __name__ == "__main__":
    main()
