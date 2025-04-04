# Currency Conversion Tracker

|Route|HTTP METHOD|Description|Parameters|
|-----|----| --------|-----|
|/transactions|GET|Apply currency conversion on all transactions|None|
|/transactions/<id>|GET|Apply currency conversion on selected transaction by id| (integer)|
|/transactions/search|GET|Apply currency conversion on selected transaction based on applied search criteria|before (YYYY-MM-DD), after (YYYY-MM-DD), below(Decimal), exceed(Decimal), match(String), currency(String)|

## Brief description

## Start Flask Application
```sh
flask run
```
## Getting Started


## Technologies used


## Generate CSV file
* Currencies list https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies.json
