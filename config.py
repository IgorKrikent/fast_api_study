from dotenv import load_dotenv

import os

load_dotenv()

USER = os.getenv("USER") or ''
PASSWORD = os.getenv("PASSWORD") or ''
