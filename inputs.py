import os
import random

PARSERS = {
    #'csv': CsvParser,
    #'xls': XlsParser,
    #....
}

class BaseParser(object):
    """
    Different input format parsers should be based off this
    """
    def __init__(self, discounts):
        self.discounts = discounts

    def parse(self):
        raise NotImplementedError


class DummyParser(BaseParser):
    """
    Dummy parser that just returns a list of 35 random
    """
    def parse(self):
        return [{
            'product_id': i,
            'product_name': 'Product {}'.format(i),
            'product_description': 'This is the {}th product'.format(i),
            'price': round(random.uniform(0.99, 100), 2),
            'discount': round(random.uniform(0.05, 0.55), 2),
            'shipping_discount': round(random.uniform(0, 0.55), 2),
            } for i in range(35)]


def get_parser(filename):
    _, extension = os.path.splitext(filename)
    return PARSERS.get(extension.strip('.'), DummyParser)


def parse(discounts):
    """
    """
    parser = get_parser(discounts.filename)
    return parser(discounts).parse()
