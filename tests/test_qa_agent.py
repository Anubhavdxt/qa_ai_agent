import pytest
from subprocess import Popen, PIPE

def test_qa_agent():
    process = Popen(["python", "qa_agent.py", "--url", "https://help.example.com"], stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    assert "Error" not in stderr.decode()