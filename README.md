# Retrievable: Framework for information retrieval research and experimentation

Retrievable provides a general-purpose framework for experimental evaluation of 
information retrieval methods including both novel scoring algorithms and 
query performance prediction.

The framework is built on the [Indri](http://www.lemurproject.org/indri/) search
engine using the [pyndri](https://github.com/cvangysel/pyndri/) Python interface.


## Usage

Creating temporal time series index:
```
create-ts -i /data/indexes/ap.temporal/ -o tsindex/ap.tsindex.csv.gz
```

Running a custom scorer with configurable parameter values:
```
run-queries -c config/scorers.yaml
```

Running cross-validation.
```
run-cv -d eval/ap/dir/ -k 5 -m map -s
```

## Developing

Installing locally:
```
pip install -e .
```

Installing from pypi:
```
pip install retrievable-core
```

Running unit tests:
```
pytest --cov=retrievable  retrievable/tests --show-capture=stdout
```

Publishing to pypi:
```
python3 setup.py sdist bdist_wheel
twine upload --repository-url https://test.pypi.org/legacy/ dist/*

```
