#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# Copyright (C) 2013, Cameron White

import logging
import argparse
from StringIO import StringIO
from kitnirc.modular import Module
from PyOLP import PyOLP
from PyOLP.api_objects import NotSet

_log = logging.getLogger(__name__)

LIMIT = 5

OLP = PyOLP()

parser_output = StringIO()

class ArgumentParser(argparse.ArgumentParser):
    def _print_message(self, message, file=None):
        super(ArgumentParser, self)._print_message(message, parser_output)
    def exit(self, status=0, message=None):
        if message:
            self._print_message(message, None)

parser = ArgumentParser()
subparsers = parser.add_subparsers(dest='subparser')
subparser_product = subparsers.add_parser('!product')
subparser_product.add_argument('id', type=str)
subparser_products = subparsers.add_parser('!products')
subparser_products.add_argument('--code', type=str, default=NotSet)
subparser_products.add_argument('--proof', type=float, default=NotSet)
subparser_products.add_argument('--on_sale', type=bool, default=NotSet)
subparser_products.add_argument('--status', type=str, default=NotSet)
subparser_products.add_argument('--title', type=str, default=NotSet)
subparser_store = subparsers.add_parser('!store')
subparser_store.add_argument('id', type=str)
subparser_stores = subparsers.add_parser('!stores')
subparser_price = subparsers.add_parser('!price')
subparser_price.add_argument('id', type=str)
subparser_prices = subparsers.add_parser('!prices')
subparser_prices.add_argument('product_id', type=str)

def reset_parser_output():
    parser_output.seek(0, 0)
    parser_output.truncate()

class WhiskeyBotModule(Module):
    
    @Module.handle("PRIVMSG")
    def whiskey(self, client, actor, recipient, message):
        # Only pay attention if addressed directly in channels
        try:
            args = parser.parse_args(message.split())
        except (NameError, TypeError):
            reset_parser_output()
            return

        if parser_output.getvalue():
            parser_output.seek(0, 0)
            parser_output.truncate()
            return
            
        # Log a message to the INFO log level - see here for more details:
        # http://docs.python.org/2/library/logging.html
        _log.info("Responding to %r in %r", actor, recipient)
        
        if args.subparser == "!products":
            products = OLP.get_products(
                proof=args.proof,
                on_sale=args.on_sale,
                status=args.status,
                title=args.title,
            )
        
        i = 0
        for product in products:
            if i > LIMIT:
                break;
            i += 1
            price = product.get_price()
            message = '{}: {} - {} for ${}'.format(
                product.id,
                product.title,
                product.size,
                price.amount,
            )

            # The 'reply' function automatically sends a replying PM if
            # the bot was PM'd, or addresses the user in a channel who
            # addressed the bot in a channel.
            client.reply(recipient, actor, message)
            
            reset_parser_output()

        # Stop any other modules from handling this message.
        return True

module = WhiskeyBotModule
