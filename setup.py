from setuptools import setup, find_packages

setup(
    name="qa_agent",
    version="0.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "requests",
        "beautifulsoup4",
        "spacy",
        "transformers",
        "sentence-transformers",
    ],
    entry_points={
        "console_scripts": [
            "qa_agent = agent.qa_agent:main",
        ],
    },
)
