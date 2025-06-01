# ib-flex-importer
Tool for importing IB Flex report entries into Beancount journal

Converting the functionality of interactive-brokers-flex-rs, ibflex, [repo](https://github.com/alensiljak/interactive-brokers-flex-rs) project to Python.
Since Beancount provides an ingestion framework, beangulp, the tool should utilize that.

# Setup

Install the latest beangulp (0.3.0) from the git repository directly:
```sh
uv pip install git+https://github.com/beancount/beangulp/
```

# Run
```sh
uv run python import.py extract ./downloads > out/tmp.beancount
```

# Debugging
Install the latest beangulp (0.3.0) from a git clone instead.
```sh
uv pip install -e <path to beangulp>
```

# Docs
Following the examples at beangulp [repo](https://github.com/beancount/beangulp/tree/master/examples/).

To configure the Flex report, see the [instructions](report-configuration.md).

# References
- Beangulp [repo](https://github.com/beancount/beangulp)
- beancounttools, [repo](https://github.com/tarioch/beancounttools)
- uabean, [repo](https://github.com/OSadovy/uabean/)
