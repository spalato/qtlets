import pathlib
from setuptools import setup

# Minimal shim to keep compatibility with tooling that imports setup.py
# Metadata is defined in pyproject.toml (PEP 621). Keep install-time
# requirements fallback for older pip/setuptools.

HERE = pathlib.Path(__file__).parent

def _read_requirements():
    req_file = HERE / 'requirements.txt'
    if not req_file.exists():
        return []
    return [line.strip() for line in req_file.read_text(encoding='utf8').splitlines() if line.strip()]

if __name__ == '__main__':
    setup(install_requires=_read_requirements())
