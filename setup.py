# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='retrievable-core',
    version='0.1.0',
    description='',
    long_description=readme,
    author='Craig Willis',
    author_email='willis8@illinois.edu',
    url='https://github.com/craig-willis/retrievable',
    license=license,
    packages=['retrievable.core', 'retrievable.scorers'],
    entry_points={
        'console_scripts': [
            'run-queries = retrievable.core.run_queries:main',
            'create-ts = retrievable.core.create_ts:main'
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
