from .setting import *
from .manager import Manager
import argparse
import logging
import asyncio

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



def main():
    app = Manager()
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument('--version', action='version', version=VERSION)
    parser.add_argument('--uuid', action='store_true', help="Generate a new UUID")
    args = parser.parse_args()
    if args.uuid:
        print(f"Generated UUID: {app.UuidGen()}")
    logger.info("Start Manager..")
    # print(app.UuidGen())
    # asyncio.run(app.main())
