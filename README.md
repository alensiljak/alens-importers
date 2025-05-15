# ib-flex-importer
Tool for importing IB Flex report entries into Beancount journal

Converting the functionality of interactive-brokers-flex-rs, ibflex, [repo](https://github.com/alensiljak/interactive-brokers-flex-rs) project to Python.
Since Beancount provides an ingestion framework, beangulp, the tool should utilize that.

# Run
```sh
uv run python import.py extract ./downloads > tmp.beancount
```

# Docs
Following the examples at beangulp [repo](https://github.com/beancount/beangulp/tree/master/examples/).

# References
- Beangulp [repo](https://github.com/beancount/beangulp)
- beancounttools, [repo](https://github.com/tarioch/beancounttools)
- uabean, [repo](https://github.com/OSadovy/uabean/)
