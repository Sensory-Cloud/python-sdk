import os
import sys
import argparse


def get_options() -> argparse.Namespace:
    """
    Function that reads in command line arguments:
    --version sets the new version to be published
    --upload determines whether or not the new distribution should be
        uploaded to pypi

    Returns:
        argparse.Namespace: Command line arguments containing the new
            version as a string and a boolean flag indicating whether
            or not to upload to Pypi.
    """
    
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Publish Sensory Cloud Python SDK"
    )
    parser.add_argument(
        "--version",
        dest="new_version",
        type=str,
        required=True,
        help="new version to be published",
    )
    parser.add_argument(
        "--upload",
        dest="upload",
        type=bool,
        required=False,
        default=False,
        help="boolean flag indicating whether or not to upload to pypi",
    )

    args: argparse.Namespace = parser.parse_args()

    return args


def build(args) -> None:
    """
    Function that upgrades the version number and builds the new
    distribution files
    """
    
    if args.new_version[0] == "v":
        args.new_version: str = args.new_version[1:]

    with open("setup.py", "r") as f:
        setup_text: str = f.read()

    current_version: str = eval(setup_text.split("version=")[1].split(",")[0])

    new_setup_text: str = setup_text.replace(
        f'version="{current_version}"', f'version="{args.new_version}"'
    )

    with open("setup.py", "w") as f:
        f.write(new_setup_text)

    os.system("python setup.py sdist")


def upload_to_pypi(args) -> None:
    """
    Function that uploads the new distribution to Pypi if the --upload command line
    argument is set to true
    """
    
    if args.upload:
        os.system("twine upload dist/*")


if __name__ == "__main__":
    args = get_options()

    build(args)
    upload_to_pypi(args)
