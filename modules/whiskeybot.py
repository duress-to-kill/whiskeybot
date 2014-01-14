#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# Copyright (C) 2013, Cameron White

import logging
import argparse
from kitnirc.modular import Module
from PyOLP import PyOLP
from PyOLP.api_objects import NotSet
from botparse import BotParse

_log = logging.getLogger(__name__)

LIMIT = 5

OLP = PyOLP()

parser = BotParse()
command_product = parser.add_command('!product')
command_product.add_argument('id', type=str)
command_products = parser.add_command('!products')
command_products.add_argument('--code', type=str, default=NotSet)
command_products.add_argument('--proof', type=float, default=NotSet)
command_products.add_argument('--on_sale', type=bool, default=NotSet)
command_products.add_argument('--status', type=str, default=NotSet)
command_products.add_argument('--title', type=str, default=NotSet)
command_store = parser.add_command('!store')
command_store.add_argument('id', type=str)
command_stores = parser.add_command('!stores')
command_price = parser.add_command('!price')
command_price.add_argument('id', type=str)
command_prices = parser.add_command('!prices')
command_prices.add_argument('product_id', type=str)

class WhiskeyBotModule(Module):
    
    @Module.handle("PRIVMSG")
    def whiskey(self, client, actor, recipient, message):
        # Only pay attention if addressed directly in channels
        try:
            args = parser.parse_args(message.split())
        except (NameError, TypeError):
            return
            
        # Log a message to the INFO log level - see here for more details:
        # http://docs.python.org/2/library/logging.html
        _log.info("Responding to %r in %r", actor, recipient)
        
        if args.command == "!help":
            messages = parser.format_help().split('\n')

        elif args.command == "!product":
            if args.help:
                messages = command_product.format_help().split('\n')

        elif args.command == "!products":
            if args.help:
                messages = command_products.format_help().split('\n')
            else:
                products = OLP.get_products(
                    proof=args.proof,
                    on_sale=args.on_sale,
                    status=args.status,
                    title=args.title,
                )
                
                messages = []
                i = 0
                for product in products:
                    if i > LIMIT:
                        break;
                    i += 1
                    price = product.get_price()
                    messages.append('{}: {} - {} for ${}'.format(
                        product.id,
                        product.title,
                        product.size,
                        price.amount,
                    ))

        elif args.command == "!price":
            if args.help:
                messages = command_price.format_help().split('\n')

        elif args.command == "!prices":
            if args.help:
                messages = command_prices.format_help().split('\n')

        elif args.command == "!store":
            if args.help:
                messages = command_price.format_help().split('\n')

        elif args.command == "!stores":
            if args.help:
                messages = command_prices.format_help().split('\n')
        
        for message in messages:
            # The 'reply' function automatically sends a replying PM if
            # the bot was PM'd, or addresses the user in a channel who
            # addressed the bot in a channel.
            client.reply(recipient, actor, message)

        # Stop any other modules from handling this message.
        return True

module = WhiskeyBotModule
