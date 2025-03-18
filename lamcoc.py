#!/usr/bin/env python3

import argparse
import os
from lamcoc.planner import generate_plan
from lamcoc.creator import create_zip


def main():
    parser = argparse.ArgumentParser(description="LAMCOC - Lambda Code Creator")
    parser.add_argument("command", choices=["plan", "create"], help="Action to perform")

    args = parser.parse_args()

    project_root = os.getcwd()  # Run in the current directory

    if args.command == "plan":
        generate_plan(project_root)
    elif args.command == "create":
        create_zip(project_root)
    else:
        print("Error en arguments")


if __name__ == "__main__":
    main()
