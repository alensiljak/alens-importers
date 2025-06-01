"""
The main import script.
"""

import beangulp  # type: ignore
from beancount.core import data
from uabean.hooks import detect_transfers
from uabean.importers import ibkr

from importers import ibflex

importers = [
    # utrade.Importer(
    #     "USD",
    #     "Assets:US:UTrade",
    #     "Assets:US:UTrade:Cash",
    #     "Income:US:UTrade:{}:Dividend",
    #     "Income:US:UTrade:{}:Gains",
    #     "Expenses:Financial:Fees",
    #     "Assets:US:BofA:Checking",
    # ),
    # ofx.Importer("379700001111222", "Liabilities:US:CreditCard", "bofa"),
    # acme.Importer("Assets:US:ACMEBank"),
    # csvbank.Importer("Assets:US:CSVBank", "USD"),
    ibflex.Importer(),
    # ibkr.Importer(),
]


def clean_up_descriptions(extracted_entries, existing_entries):
    """Example filter function; clean up cruft from narrations.

    Args:
      extracted_entries: A list of directives.
    Returns:
      A new list of directives with possibly modified payees and narration
      fields.
    """
    clean_entries = []
    for entry in extracted_entries:
        if isinstance(entry, data.Transaction):
            if entry.narration and " / " in entry.narration:
                left_part, _ = entry.narration.split(" / ")
                entry = entry._replace(narration=left_part)
            if entry.payee and " / " in entry.payee:
                left_part, _ = entry.payee.split(" / ")
                entry = entry._replace(payee=left_part)
        clean_entries.append(entry)
    return clean_entries


def process_extracted_entries(extracted_entries_list, ledger_entries):
    """Example filter function;

    Args:
      extracted_entries_list: A list of (filename, entries) pairs, where
        'entries' are the directives extract from 'filename'.
      ledger_entries: If provided, a list of directives from the existing
        ledger of the user. This is non-None if the user provided their
        ledger file as an option.
    Returns:
      A possibly different version of extracted_entries_list, a list of
      (filename, entries), to be printed.
    """
    return [
        (filename, clean_up_descriptions(entries, ledger_entries), account, importer)
        for filename, entries, account, importer in extracted_entries_list
    ]


# A list of hook functions to be applied during the import process.
# These hooks are used by the beangulp importer to modify or process extracted entries
# before final ingestion.
hooks = [clean_up_descriptions, process_extracted_entries, detect_transfers]


if __name__ == "__main__":
    ingest = beangulp.Ingest(importers, hooks)
    ingest()
