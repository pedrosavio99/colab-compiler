# your_app/compilerwithmodules/utils.py
import uuid
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("Compiler")

def generate_unique_id():
    return str(uuid.uuid4())[:8]