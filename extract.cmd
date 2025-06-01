:: execute the importer
@REM uv run python import.py extract ./downloads > out/tmp.beancount
uv run python import.py extract ./downloads
:: Add existing file -e ...