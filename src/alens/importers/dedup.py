'''
Deduplication of transactions.
'''

from beancount.core import data


# Metadata field that indicates the entry is a likely duplicate.
DUPLICATE = "__duplicate__"


def _get_transaction_key(t: data.Transaction):
    if not isinstance(t, data.Transaction):
        return None

    # Sort postings to ensure consistent key generation regardless of order
    def _get_posting_key(p: data.Posting):
        return (p.account, str(p.units.number), p.units.currency)

    filtered_postings = [p for p in t.postings if not p.account.startswith('Equity:Currency')]
    postings_sorted = tuple(sorted([_get_posting_key(p) for p in filtered_postings]))
    return (t.date, postings_sorted)

def deduplicate(entries: data.Entries, existing: data.Entries) -> None:
    """
    Deduplicate transactions

    Entries that are determined to be duplicates of existing entries
    are marked setting the "__duplicate__" metadata field.
    """
    existing_transactions_map = {}
    for entry in existing:
        if isinstance(entry, data.Transaction) and DUPLICATE not in entry.meta:
            key = _get_transaction_key(entry)
            if key:
                existing_transactions_map[key] = entry

    for entry in entries:
        if not isinstance(entry, data.Transaction):
            continue

        key = _get_transaction_key(entry)
        if key and key in existing_transactions_map:
            entry.meta[DUPLICATE] = True
            target_transaction = existing_transactions_map[key]
            target_transaction.meta[DUPLICATE] = True
            del existing_transactions_map[key] # Remove to prevent re-matching
