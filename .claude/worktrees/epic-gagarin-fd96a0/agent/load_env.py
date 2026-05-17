"""
Helper: load .env before running agent.py when python-dotenv is available.
Usage: python load_env.py
"""
from dotenv import load_dotenv
load_dotenv()

import agent
agent.run_agent()
