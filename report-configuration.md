# IBKR Flex Query Configuration

Instructions for setting up the IBKR Flex Query report to be used by the importer.

Create an Activity Flex Query in Flex Queries using the following parameters:

Sections

## Account Information
1.AccountID
2.Currency

## Cash Report
1.Currency
2.StartingCash
3.EndingCash
4.NetCashBalance (SLB)
5.ToDate

## Cash Transactions
1.Currency
2.Symbol
3.ISIN
4.Date/Time
5.Amount
6.Type
7.CommodityType
// add description

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
Options: Execution
- CurrencyPrimary
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
- Date Format yyyy-MM-dd
// Time Format HH:mm:ss TimeZone
- Use the time format `HH:mm:ss`
- Date/Time Separator ' ' (single-space)
- Profit and Loss Default
- Include Canceled Trades? No
- Include Currency Rates? No
- Include Audit Trail Fields? No
- Display Account Alias in Place of Account ID? No
- Breakout by Day? No
