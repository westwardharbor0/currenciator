# Currenciator 3000

## Introduction
Curreciator is a simple CLI / Api which allows you to convert from / to your favorite currencies

## Rates source
New currency rates are downloaded from [ČNB](https://www.cnb.cz/en/financial-markets/foreign-exchange-market/central-bank-exchange-rate-fixing/central-bank-exchange-rate-fixing/) every time
they get updated. After they get updated they are stored in cache file to prevent useless updating until they are expired.
## Supported currencies
| Currency code | Currency symbol |
| :------------:|:-------------:|
|USD | US$ |
| JPY| ¥ |
| BGN| BGN |
|CZK |  Kč|
| DKK| Kr |
| EUR| € |
| GBP| £ |
| HUF| Ft |
| PLN|  zł|
| RON| L |
| SEK| kr |
| CHF|  Fr.|
| NOK|kr|
| HRK| kn |
| RUB|  R|
| TRY|  TRY|
| AUD| $ |
| BRL|  R$|
| CAD| $ |
| CNY| ¥ |
| HKD| HK$ |
| IDR| Rp |
| ILS|  ₪|
| INR| ₹ |
| KRW| W |
| MXN|$ |
| MYR| RM |
| NZD|  NZ$|
| PHP| ₱ |
| SGD| S$ |
| THB| ฿|
|  ZAR| R|

## Requirements
- Python 3 
- Python `flask`
- Python `requests`

To install all dependencies you run `make boostrap` in project root dir.
This command will install all dependencies in virtual enviroment. 

## Basic usage
###Parameters
Only these few parameters are needed to run in all modes
```bash
amount=int # required, amount of money to be converted
input_currency=str # required, input currency code / symbol
output_currency=str # optional, output currency code / symbol
```
### CLI mode
This mode is contained in `currenciator_cli.py` file.<br>
To run it using `make` (the easier way) you need to use `make cli`
<strong>Example cli call:</strong> <br>
```JSON
make cli py amount=20 input_currency=USD output_currency=CZK
{
  "input": {
      "amount": 20,
      "currency": "USD"
  }, 
  "output": {
      "CZK": 495.16
  }
}
```
To run it the <strong>"raw"</strong> way, use `venv/bin/python3 currenciator_cli.py`. <br>
<strong>Example raw call:</strong> <br>
```JSON
venv/bin/python3 currenciator_cli.py --amount 20 --input_currency USD --output_currency CZK
{
  "input": {
      "amount": 20,
      "currency": "USD"
  }, 
  "output": {
      "CZK": 495.16
  }
}
```
If no output currency is supplied, the cli will convert to all supported currencies <br><br>
### API mode
Currency api can be run in two modes:
#### venv
To run api in venv / local mode you can use `make run`.
This mode requires requirements mentioned in beginning.

#### Docker
To run api in docker mode you need to build docker image first using `make docker-build`.
After successful build you can run `make docker-run` to start the api in docker.
<br><br>
After starting the api in one of those modes you can finally use it. 
The api runs on port `3692` and has only one endpoint for converting currencies.
Since this endpoint is set to GET you can paste this example URL to browser and try it yourself.<br>
<br>
<strong>Example call:</strong>

```JSON
http://127.0.0.1:3692/currency_convertor?amount=20&input_currency=USD&output_currency=CZK
{
  "input": {
      "amount": 20,
      "currency": "USD"
  }, 
  "output": {
      "CZK": 495.16
  }
}
```

# Possible TODO's
 - [ ] gitlab ci integration
 - [ ] kubernetes deployment
 - [ ] different rates sources
 - [ ] load balancing
    .....
