# alens-importers
Tool for importing IB Flex report entries into Beancount journal

Converting the functionality of interactive-brokers-flex-rs, ibflex, [repo](https://github.com/alensiljak/interactive-brokers-flex-rs) project to Python.
Since Beancount provides an ingestion framework, beangulp, the tool should utilize that.

Former ib-flex-importer.

# Setup

Install the ibflex package from the git repository directly:
```sh
uv pip install git+https://github.com/csingley/ibflex/
```
Eventually, also install the latest beangulp:
```sh
uv pip install git+https://github.com/beancount/beangulp/
```

# Run
```sh
uv run python import.py extract ./downloads > out/tmp.beancount
# with deduplication
uv run python import.py extract ./downloads -e existing.beancount > out/tmp.beancount
```

# Testing
From terminal, the template is:
```sh
uv run pytest
uv run pytest <file_path>::<test_function_name>
uv run pytest <file_path>::<TestClassName>::<test_method_name>
```
Individual tests:
```sh
uv run pytest tests\test_ibflex.py::test_tax_reversal
uv run pytest tests\test_ibflex.py::test_cash_balances
```

# Publish

The project cannot be published as it depends on the development version of the beangulp package, which is not published yet.

# Docs
Following the examples at beangulp [repo](https://github.com/beancount/beangulp/tree/master/examples/).

To configure the Flex report, see the [instructions](report-configuration.md).

# Related Projects
- Beangulp [repo](https://github.com/beancount/beangulp)
- beancounttools, [repo](https://github.com/tarioch/beancounttools)
- uabean, [repo](https://github.com/OSadovy/uabean/)
- Red's Importers, [repo](https://github.com/redstreet/beancount_reds_importers/)
