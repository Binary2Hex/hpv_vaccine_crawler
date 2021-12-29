#!/usr/bin/env python3

import json
import sys


def main():
    input_f = sys.argv[1]
    output_f = sys.argv[2]
    with open(input_f, 'r') as in_f:
        json_data = json.load(in_f)
        with open(output_f, 'w') as out_f:
            json.dump(json_data, out_f, indent=4)


if __name__ == "__main__":
    main()
