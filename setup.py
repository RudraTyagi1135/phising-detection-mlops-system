from pathlib import Path
from typing import List

from setuptools import find_packages, setup


def get_requirements() -> List[str]:
    requirements_path = Path(__file__).with_name("requirements.txt")
    requirements: List[str] = []

    if not requirements_path.exists():
        return requirements

    for raw_line in requirements_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or line == "-e .":
            continue
        requirements.append(line)

    return requirements


setup(
    name="phishing-detection-mlops-system",
    version="1.0.0",
    author="Rudra Tyagi",
    author_email="rudratyagi777@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements(),
)
