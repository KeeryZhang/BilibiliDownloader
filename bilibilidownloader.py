#!/usr/bin/python3
"""Start here"""

import argparse
from combine import Combine


def param_parse():
    """Parse input params"""
    parser = argparse.ArgumentParser()
    parser.add_argument("inputpath", help="Video downloading root path")
    parser.add_argument("outputpath", help="Video output root path")
    parser.add_argument("--title", "-t", default=None, help="Set title manually")
    args = parser.parse_args()
    return args

def main():
    """Start from here"""
    args = param_parse()
    combination = Combine(args.inputpath, args.outputpath, args.title)
    combination.processing()


if __name__ == "__main__":
    main()
