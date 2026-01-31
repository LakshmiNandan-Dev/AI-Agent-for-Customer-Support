import pytest

from app.agent import process_query

def text_process_query():
    response = process_query("what is your skills alex have?")
    assert len(response) > 0
