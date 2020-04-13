from flask import Flask, request
from json import dumps

from src.cached_source import CachedSource
from src.currency import Currency
from src.exceptions import UnknownCurrency

# init flask api app
app = Flask(__name__)
# init cache
cached = CachedSource()

# basic endpoint to convert some currencies
@app.route('/currency_convertor')
def convert():
    # get rates and reload if needed
    rates = cached.get_rates()
    # init currency to convert
    currency = Currency(rates=rates["rates"])

    # load some arguments from request
    amount = float(request.args.get("amount"))
    input_currency = request.args.get("input_currency")
    output_currency = request.args.get("output_currency")

    # convert the amount to given or all currencies
    try:
        response = currency.convert(amount, input_currency, output_currency, json_resp=True)
    except UnknownCurrency as ex:
        return ex.message, 404
    # some nice json response
    return app.response_class(
        response=dumps(response),
        status=200,
        mimetype='application/json'
    )
