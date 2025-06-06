# IBKR Flex Query Configuration

Instructions for setting up the IBKR Flex Query report to be used by the importer.

Create an Activity Flex Query in Flex Queries using the following parameters:

Sections

## Account Information
1.AccountID
2.Currency

## Cash Report

Options:Currency Breakout

Fields:
1.Currency
2.StartingCash
3.EndingCash
4.NetCashBalance (SLB)
5.ToDate

## Cash Transactions

Options:
Dividends, Payment in Lieu of Dividends, Withholding Tax, 871(m) Withholding, Advisor Fees, Other Fees, Deposits & Withdrawals, Carbon Credits, Bill Pay, Broker Interest Paid, Broker Interest Received, Broker Fees, Bond Interest Paid, Bond Interest Received, Price Adjustments, Commission Adjustments,Detail

Fields:
1.Currency
2.Symbol
3.ISIN
4.Date/Time
5.Amount
6.Type
7.CommodityType
8.Description

## Corporate Actions

Options: Detail

## Net Stock Position Summary
1.Symbol
2.ISIN
3.ReportDate
4.NetShares

## Open Dividend Accruals
1.Symbol
2.ISIN
3.PayDate
4.Quantity
5.GrossAmount
6.NetAmount

## Open Positions
Options: Summary
1.Symbol
2.ISIN
3.Quantity

## Trades
Options: Execution, Closed Lots

- Currency
- Symbol
- SecurityID
- ISIN
- DateTime
- TransactionType
- Quantity
- TradePrice
- TradeMoney
- Proceeds
- IBCommission
- IBCommissionCurrency
- NetCash
- CostBasis
- Realized P/L
- Buy/Sell

## Transfers
Options: Transfer
1.Symbol
2.ISIN
3.DateTime
4.Quantity
5.TransferPrice


## Delivery Configuration
- Accounts Format XML
- Period Last N Calendar Days
- Number of Days 120


## General Configuration
- Date Format `yyyy-MM-dd`
- Time format `HH:mm:ss`; not `HH:mm:ss TimeZone`
- Date/Time Separator ` ` (single-space)
- Profit and Loss `Default`
- Include Canceled Trades? `No`
- Include Currency Rates? `No`
- Include Audit Trail Fields? `No`
- Display Account Alias in Place of Account ID? `No`
- Breakout by Day? `No`
