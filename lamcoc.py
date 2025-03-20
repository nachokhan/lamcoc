#!/usr/bin/env python3

import argparse
import os
import sys
from lamcoc.planner import generate_plan
from lamcoc.creator import create_zip


def main():
    parser = argparse.ArgumentParser(description="LAMCOC - Lambda Code Creator")

    parser.add_argument("command", choices=["plan", "create"], help="Action to perform")

    parser.add_argument("-p", "--project-dir", type=str, default=os.getcwd(),
                        help="Specify the project directory to work from (default: current directory)")

    parser.add_argument("-o", "--output-dir", type=str, default=os.getcwd(),
                        help="Specify the output directory for generated files (default: current directory)")

    parser.add_argument("-cd", "--config-dir", type=str, default=os.getcwd(),
                        help="Specify the directory where the config file is located (default: current directory)")

    parser.add_argument("-cf", "--config-file", type=str, default="include.yaml",
                        help="Specify the config file name (default: include.yaml)")

    parser.add_argument("-zf", "--zip-file", type=str, default="lambda.zip",
                        help="Specify the output ZIP file name (default: lambda.zip)")

    try:
        args = parser.parse_args()
    except SystemExit as e:
        print(f"❌ Invalid arguments: {e}")
        parser.print_help()
        sys.exit(1)

    # Ensure project directory exists
    project_dir = os.path.abspath(args.project_dir)
    if not os.path.exists(project_dir):
        print(f"❌ Error: Project directory does not exist: {project_dir}")
        return

    # Ensure output directory exists
    output_dir = os.path.abspath(args.output_dir)
    os.makedirs(output_dir, exist_ok=True)

    if args.command == "plan":
        generate_plan(**vars(args))
    elif args.command == "create":
        create_zip(**vars(args))
    else:
        print("❌ Error: Invalid command")


if __name__ == "__main__":
    main()
