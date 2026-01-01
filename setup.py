"""
Setup configuration for Sindh Archives Backend.

This file contains the setup configuration for packaging and distributing
the Sindh Archives Backend application.
"""
from setuptools import setup, find_packages
import os

# Read the contents of README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Read requirements from requirements.txt
with open(os.path.join(this_directory, 'requirements.txt'), encoding='utf-8') as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name="sindh-archives-backend",
    version="0.1.0",
    author="Sindh Archives Team",
    author_email="admin@sindh-archives.org",
    description="A secure PostgreSQL record management system backend foundation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sindh-archives/backend",
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Database",
        "Topic :: Security",
    ],
    python_requires='>=3.11',
    install_requires=requirements,
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pytest-cov>=4.0.0',
            'black>=23.0.0',
            'mypy>=1.0.0',
            'pylint>=2.15.0',
        ],
    },
    entry_points={
        'console_scripts': [
            'init-db=sindh_archives.scripts.init_db:main',
        ],
    },
    keywords='postgresql, database, records, management, security',
    project_urls={
        'Bug Reports': 'https://github.com/sindh-archives/backend/issues',
        'Source': 'https://github.com/sindh-archives/backend',
    },
)