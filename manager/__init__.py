from .setting import *
from .manager import Manager
import argparse
import logging
import asyncio

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)








def main():
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument('--version', action='version', version=VERSION)
    args = parser.parse_args()
    logger.info("Start Manager..")
    app = Manager()
    asyncio.run(app.main())
