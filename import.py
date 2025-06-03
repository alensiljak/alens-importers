"""
The main import script.
"""

import beangulp  # type: ignore
from beancount.core import data
#from uabean.hooks import detect_transfers
# from uabean.importers import ibkr

from alens.importers import ibflex


fund_codes = [["OPI", "US67623C1099"], ["VAP.AX", "AU000000VAP7"]]

ibflex_config = {
    "cash_account": "Assets:Investments:IB:Cash-{currency}",
    "stock_account": "Assets:Investments:IB:Stocks:{symbol}",
    "dividend_account": "Income:Investments:Dividend:IB:{currency}:{symbol}",
    "dividend_payee": "{symbol} distribution",
    "interest_account": "Income:Investments:Interest:IB:{symbol}",
    "broker_interest_account": "Income:Investments:Interest:IB:Cash",
    "fees_account": "Expenses:Commissions:IB",
    "whtax_account": "Expenses:Investments:IB:WithholdingTax",
    "txfer-EUR": "Assets:Bank-Accounts:EUR",
    "txfer-AUD": "Assets:Bank-Accounts:AUD",
    "symbols": fund_codes,
}

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
    ibflex.Importer(ibflex_config),
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
hooks = [clean_up_descriptions, process_extracted_entries]


if __name__ == "__main__":
    ingest = beangulp.Ingest(importers, hooks)
    ingest()
