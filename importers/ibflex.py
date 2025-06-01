"""
Creating IBKR importer from scratch.
"""

from collections import defaultdict
import os
import re
import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional

import beangulp  # type: ignore
from beancount.core import amount, data, flags, position, realization
from beangulp import cache
from beangulp.importers.mixins.identifier import identify
import ibflex
from ibflex import Types
from ibflex.enums import BuySell, CashAction, OpenClose, Reorg
from loguru import logger


class AccountTypes(str, Enum):
    """Account types in the configuration file"""

    CASH = "cash_account"
    STOCK = "stock_account"
    DIVIDEND = "dividend_account"
    INTEREST = "interest_account"
    WHTAX = "whtax_account"


class Importer(beangulp.Importer):
    """IBKR Flex Query XML importer for Beancount"""

    def __init__(self, *args, **kwargs):
        logger.debug("Initializing IBKR importer")

        # get config, the first argument.
        self.config = args[0]

        # create symbol dictionaries.
        self.symbol_to_isin, self.isin_to_symbol = self.create_symbol_dictionaries()

        super().__init__(**kwargs)

    @property  # type: ignore
    def name(self) -> str:
        logger.debug("Getting importer name")

        return "AS IBKR importer (new)"

    def identify(self, filepath: str) -> bool:
        """Indicates whether the importer can handle the given file"""
        logger.debug(f"Identifying {filepath}")

        matchers = {
            # File is xml
            "mime": [re.compile(r"text/xml")],
            # The main XML tag is FlexQueryResponse
            "content": [re.compile(r"<FlexQueryResponse ")],
        }

        return identify(matchers, None, cache.get_file(filepath))

    def account(self, filepath: str) -> data.Account:
        """Return the archiving account associated with the given file."""
        logger.debug(f"Getting account for {filepath}")

        # TODO : return the correct account
        return "ib-aus"

    def filename(self, filepath: str) -> Optional[str]:
        """Returns the archival filename for the report"""
        return os.path.basename(filepath)

    def extract(self, filepath: str, existing: data.Entries) -> data.Entries:
        """
        Extract transactions and other directives from a document.
        Existing entries are received as an argument, if Beancount file was
        specified.
        Deduplication is done against these.
        A list of imported directives should be returned.
        """
        logger.debug(f"Extracting from {filepath}")

        # if False and self.use_existing_holdings and existing_entries is not None:
        #     self.holdings_map = self.get_holdings_map(existing_entries)
        # else:
        #     self.holdings_map = defaultdict(list)
        statements = ibflex.parser.parse(open(filepath, "r", encoding="utf-8"))
        assert isinstance(statements, Types.FlexQueryResponse)

        statement = statements.FlexStatements[0]
        assert isinstance(statement, Types.FlexStatement)

        transactions = (
            #     self.Trades(statement.Trades) +
            self.cash_transactions(statement.CashTransactions)
            +
            #     + self.Balances(statement.CashReport)
            self.cash_balances(statement.CashReport)
            +
            #     + self.corporate_actions(statement.CorporateActions)
            self.stock_balances(statement.OpenPositions, statement.CashReport)
        )

        transactions = self.merge_dividend_and_withholding(transactions)
        # # self.adjust_closing_trade_cost_basis(transactions)
        # return self.autoopen_accounts(transactions, existing_entries) + transactions

        return transactions

    def create_symbol_dictionaries(self):
        """Create symbol dictionaries, to fetch Symbols/ISINs"""
        array = self.config.get("symbols")

        symbol_to_isin = {}
        isin_to_symbol = {}

        # 2. Populate the dictionaries from your list
        for symbol, isin in array:
            symbol_to_isin[symbol] = isin
            isin_to_symbol[isin] = symbol

        return symbol_to_isin, isin_to_symbol

    def get_account_name(self, acct_type: AccountTypes, symbol=None, currency=None):
        """Get the account name from the config file"""
        account_name = self.config.get(acct_type)

        # Populate template fields.
        if symbol is not None:
            account_name = account_name.replace("{symbol}", symbol.replace(" ", ""))
        if currency is not None:
            account_name = account_name.replace("{currency}", currency)
        return account_name

    def cash_transactions(self, ct):
        """Extract cash transactions"""
        transactions = []
        for index, row in enumerate(ct):
            if row.type == CashAction.DEPOSITWITHDRAW:
                # TODO : implement
                # transactions.append(self.deposit_from_row(index, row))
                pass
            elif row.type in (CashAction.BROKERINTRCVD, CashAction.BROKERINTPAID):
                # TODO : implement
                # transactions.append(self.Interest_from_row(index, row))
                pass
            elif row.type in (CashAction.FEES, CashAction.COMMADJ):
                # TODO : implement
                # transactions.append(self.fee_from_row(index, row))
                pass
            elif row.type in (
                CashAction.WHTAX,
                CashAction.DIVIDEND,
                CashAction.PAYMENTINLIEU,
            ):
                transactions.append(
                    self.dividends_and_withholding_tax_from_row(index, row)
                )
            else:
                raise RuntimeError(f"Unknown cash transaction type: {row.type}")
        return transactions

    def dividends_and_withholding_tax_from_row(self, idx, row: Types.CashTransaction):
        """Converts dividends, payment inlieu of dividends and withholding tax to a
        beancount transaction.
        Stores div type in metadata for the merge step to be able to match tax withdrawals
        to the correct div.
        """
        assert isinstance(row.currency, str)
        assert isinstance(row.amount, Decimal)
        amount_ = amount.Amount(row.amount, row.currency)

        text = row.description
        # Find ISIN in description in parentheses
        # isin = re.findall(r"\(([a-zA-Z]{2}[a-zA-Z0-9]{9}\d)\)", text)[0]
        isin = row.isin
        # TODO: fix
        # pershare_match = re.search(r"(\d*[.]\d*)(\D*)(PER SHARE)", text, re.IGNORECASE)
        # payment in lieu of a dividend does not have a PER SHARE in description
        # pershare = pershare_match.group(1) if pershare_match else ""
        pershare = ""

        # meta = {"isin": isin, "per_share": pershare}
        meta = {}

        account = ""
        if row.type == CashAction.WHTAX:
            account = self.get_account_name(
                AccountTypes.WHTAX, row.symbol, row.currency
            )
        elif row.type == CashAction.DIVIDEND or row.type == CashAction.PAYMENTINLIEU:
            account = self.get_account_name(
                AccountTypes.DIVIDEND, row.symbol, row.currency
            )
        else:
            # TODO : implement
            # account = self.get_div_income_account(row.currency, row.symbol)
            # type_ = row.type
            meta["div"] = True
        # meta["div_type"] = row.type.value

        postings = [
            data.Posting(account, -amount_, None, None, None, None),
            data.Posting(
                self.get_account_name(AccountTypes.CASH, row.symbol, row.currency),
                amount_,
                None,
                None,
                None,
                None,
            ),
        ]
        metadata = data.new_metadata(
            "dividend",
            0,
            meta,
        )

        assert isinstance(row.reportDate, date)

        # row.dateTime = the effective/book date.
        # row.reportDate = the date when the transaction happened and appeared in the report.

        return data.Transaction(
            metadata,
            row.reportDate,
            flags.FLAG_OKAY,
            self.config.get("dividend_payee").replace("{symbol}", row.symbol),
            text,
            data.EMPTY_SET,
            data.EMPTY_SET,
            postings,
        )

    def merge_dividend_and_withholding(self, entries):
        """This merges together transactions for earned dividends with the witholding tax ones,
        as they can be on different lines in the cash transactions statement.
        """
        grouped = defaultdict(list)
        for e in entries:
            if not isinstance(e, data.Transaction):
                continue
            if "div_type" in e.meta and "isin" in e.meta:
                grouped[(e.date, e.payee, e.meta["div_type"])].append(e)
        for group in grouped.values():
            if len(group) < 2:
                continue
            # merge
            try:
                d = [e for e in group if "div" in e.meta][0]
            except IndexError:
                continue
            for e in group:
                if e != d:
                    d.postings.extend(e.postings)
                    entries.remove(e)
            del d.meta["div_type"]
            del d.meta["div"]
            # merge postings with the same account
            grouped_postings = defaultdict(list)
            for p in d.postings:
                grouped_postings[p.account].append(p)
            d.postings.clear()
            for account, postings in grouped_postings.items():
                units = [p.units for p in postings if isinstance(p.units, data.Amount)]
                d.postings.append(
                    data.Posting(
                        account,
                        reduce(amount_add, (p.units for p in postings)),
                        None,
                        None,
                        None,
                        None,
                    )
                )
        return entries

    def date(self, filepath: str) -> datetime.date | None:
        """Archival date of the file"""
        logger.debug(f"Getting date for {filepath}")

        # return super().date(filepath)
        statements = ibflex.parser.parse(open(filepath, "r", encoding="utf-8"))

        return statements.FlexStatements[0].whenGenerated

    def cash_balances(self, cr):
        """Account balance assertions"""
        transactions = []
        for row in cr:
            if row.currency == "BASE_SUMMARY":
                continue  # this is a summary balance that is not needed for beancount
            amount_ = amount.Amount(row.endingCash, row.currency)

            transactions.append(
                data.Balance(
                    data.new_metadata("balance", 0),
                    row.toDate + datetime.timedelta(days=1),
                    self.get_account_name(AccountTypes.CASH, currency=row.currency),
                    amount_,
                    None,
                    None,
                )
            )
        return transactions

    def stock_balances(self, rows, cash_report):
        """Stock balance assertions"""
        assert cash_report

        txns = []
        date = self.get_balance_assertion_date(cash_report)
        # Balance is as of the next day
        date = date + datetime.timedelta(days=1)

        for row in rows:
            account = self.get_account_name(AccountTypes.STOCK, row.symbol)
            # isin = row.isin

            # Get the symbol from Beancount by ISIN
            # row.symbol
            symbol = self.isin_to_symbol[row.isin]

            txns.append(
                data.Balance(
                    data.new_metadata("balance", 0),
                    date,
                    account,
                    amount.Amount(row.position, symbol),
                    None,
                    None,
                )
            )

        return txns

    # def stock_trades(self, trades):
    #     """Generates transactions for IB stock trades.
    #     Tries to keep track of available holdings to disambiguate sales when lots are not enough,
    #     e.g. when there were multiple buys of the same symbol on the specific date.
    #     Currently, it does not take into account comission when calculating cost for stocks,
    #     just the trade price. It keeps the "real" cost as "ib_cost" metadata field though, which might be utilized in the future.
    #     It is mostly because I find the raw unafected price nicer to see in my beancount file.
    #     It also creates the fee posting for comission with "C" flag to distinguish it from other postings.
    #     """
    #     transactions = []
    #     for row, lots in iter_trades_with_lots(trades):
    #         if row.buySell in (BuySell.SELL, BuySell.CANCELSELL):
    #             op = "SELL"
    #         elif row.buySell in (BuySell.BUY, BuySell.CANCELBUY):
    #             op = "BUY"
    #         else:
    #             raise RuntimeError(f"Unknown buySell value: {row.buySell}")
    #         currency = row.currency
    #         assert isinstance(currency, str)

    #         currency_IBcommision = row.ibCommissionCurrency
    #         assert isinstance(currency_IBcommision, str)

    #         symbol = row.symbol
    #         assert isinstance(row.netCash, Decimal)
    #         net_cash = amount.Amount(row.netCash, currency)

    #         assert isinstance(row.ibCommission, Decimal)
    #         commission = amount.Amount(row.ibCommission, currency_IBcommision)

    #         assert isinstance(row.quantity, Decimal)
    #         quantity = amount.Amount(row.quantity, get_currency_from_symbol(symbol))
    #         assert isinstance(row.tradePrice, Decimal)
    #         price = amount.Amount(row.tradePrice, currency)
    #         assert isinstance(row.tradeDate, datetime.date)
    #         date = row.dateTime.date()

    #         if row.openCloseIndicator == OpenClose.OPEN:
    #             self.add_holding(row)
    #             cost = position.CostSpec(
    #                 number_per=price.number,
    #                 number_total=None,
    #                 currency=currency,
    #                 date=row.tradeDate,
    #                 label=None,
    #                 merge=False,
    #             )
    #             lotpostings = [
    #                 data.Posting(
    #                     self.get_asset_account(symbol),
    #                     quantity,
    #                     cost,
    #                     price,
    #                     None,
    #                     {"ib_cost": row.cost},
    #                 ),
    #             ]
    #         else:
    #             lotpostings = []
    #             for clo in lots:
    #                 try:
    #                     clo_price = self.get_and_reduce_holding(clo)
    #                 except ValueError as e:
    #                     warnings.warn(str(e))
    #                     clo_price = None
    #                 cost = position.CostSpec(
    #                     clo_price,
    #                     number_total=None,
    #                     currency=clo.currency,
    #                     date=clo.openDateTime.date(),
    #                     label=None,
    #                     merge=False,
    #                 )

    #                 lotpostings.append(
    #                     data.Posting(
    #                         self.get_asset_account(symbol),
    #                         amount.Amount(
    #                             -clo.quantity, get_currency_from_symbol(clo.symbol)
    #                         ),
    #                         cost,
    #                         price,
    #                         None,
    #                         {"ib_cost": clo.cost},
    #                     )
    #                 )

    #             lotpostings.append(
    #                 data.Posting(
    #                     self.get_pnl_account(symbol), None, None, None, None, None
    #                 )
    #             )
    #         postings = (
    #             [
    #                 data.Posting(
    #                     self.get_account_name(AccountTypes.CASH, currency=currency),
    #                     net_cash,
    #                     None,
    #                     None,
    #                     None,
    #                     None,
    #                 )
    #             ]
    #             + lotpostings
    #             + [
    #                 data.Posting(
    #                     self.get_fees_account(currency_IBcommision),
    #                     minus(commission),
    #                     None,
    #                     None,
    #                     "C",
    #                     None,
    #                 )
    #             ]
    #         )

    #         transactions.append(
    #             data.Transaction(
    #                 data.new_metadata("trade", 0),
    #                 date,
    #                 flags.FLAG_OKAY,
    #                 symbol,  # payee
    #                 " ".join([op, quantity.to_string(), "@", price.to_string()]),
    #                 data.EMPTY_SET,
    #                 data.EMPTY_SET,
    #                 postings,
    #             )
    #         )

    #     return transactions

    def get_balance_assertion_date(self, cash_report) -> datetime.date:
        """Get the date to use for balance assertions."""
        summary = cash_report[0]
        return summary.toDate

    def deduplicate(self, entries: data.Entries, existing: data.Entries) -> None:
        """Mark duplicates in extracted entries."""
        logger.debug(f"Deduplicating {len(entries)} entries")

        return super().deduplicate(entries, existing)


_initial_missing = object()


def reduce(function, sequence, initial=_initial_missing):
    """
    reduce(function, iterable[, initial], /) -> value

    Apply a function of two arguments cumulatively to the items of an iterable, from left to right.

    This effectively reduces the iterable to a single value.  If initial is present,
    it is placed before the items of the iterable in the calculation, and serves as
    a default when the iterable is empty.

    For example, reduce(lambda x, y: x+y, [1, 2, 3, 4, 5])
    calculates ((((1 + 2) + 3) + 4) + 5).
    """

    it = iter(sequence)

    if initial is _initial_missing:
        try:
            value = next(it)
        except StopIteration:
            raise TypeError(
                "reduce() of empty iterable with no initial value"
            ) from None
    else:
        value = initial

    for element in it:
        value = function(value, element)

    return value


def amount_add(a1, a2):
    """
    add two amounts
    """
    if a1.currency == a2.currency:
        quant = a1.number + a2.number
        return amount.Amount(quant, a1.currency)
    else:
        raise ValueError(
            f"Cannot add amounts of differnent currencies: {a1.currency} and {a2.currency}"
        )


def convert_date(self, d):
    """Converts a date string to a datetime object."""
    d = d.split(" ")[0]
    return datetime.datetime.strptime(d, self.date_format)
