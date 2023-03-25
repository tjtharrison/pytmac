import logging
import os
def create():
    try:
        os.mkdir("tests/reports")
    except:
        logging.debug("Reports directory already exists")
