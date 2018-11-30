# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='retrievable',
    version='0.1.0',
    description='',
    long_description=readme,
    author='Craig Willis',
    author_email='willis8@illinois.edu',
    url='https://github.com/craig-willis/retrievable',
    license=license,
    packages=find_packages(include=['retrievable', 'retrievable.*']),
    entry_points={
        'console_scripts': [
            'run-queries = retrievable.run_queries:main',
            'create-ts = retrievable.create_ts:main'
        ]
    },
    install_requires=[
        "pyndri",
        "pandas",
        "tqdm",
        "parsl",
        "pyaml",
        "xmltodict",
    ],
)
