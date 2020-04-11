from src.cached_source import CachedSource
from src.currency import Currency

from argparse import ArgumentParser

# init cached source , the cache is not much needed here
cached = CachedSource()
# loads rates
rates = cached.get_rates()
# init the currency convert with loaded rates
currency = Currency(rates=rates["rates"])

# load the args from command line
parser = ArgumentParser(description='The ultimate currency convertor 3000')
parser.add_argument('--amount', type=int, help='amount of money we wan to convert')
parser.add_argument('--input_currency', type=str, help='currency from which we will convert')
parser.add_argument('--output_currency', type=str,
                    help='currency which we will convert to, if empty it converts to all known')

# parse given arguments to use
input_args = parser.parse_args()

# convert the currency
c = currency.convert(input_args.amount, input_args.input_currency, input_args.output_currency, json_resp=True)

# print ? the result
print(c)
