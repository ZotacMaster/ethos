import sys
import os
from setuptools import setup, find_packages
sys.path.append(os.getcwd())


print("Detected packages: ", find_packages())

setup(
    name="Ethos",
    version="1.0.0",
    author="Vyse",
    author_email="vyse@gmail.com",
    description="An elegant solution to a modern problem",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Itz-Agasta/ethos",
    packages=find_packages(include=["ethos", "ethos.*"]),
    install_requires=open("requirements.txt").read().splitlines(),
    entry_points={
        "console_scripts": [
            "ethos=ethos.main:main",  # Adjust to your module structure
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.13.1',
)