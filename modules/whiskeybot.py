#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# Copyright (C) 2013, Cameron White

import logging

from kitnirc.modular import Module

_log = logging.getLogger(__name__)

class WhiskeyBotModule(Module):
    
    @Module.handle("PRIVMSG")
    def whiskey(self, client, actor, recipient, message):
        # Only pay attention if addressed directly in channels
        if not message.startswith("%s:" % client.user.nick):
            return

        # Log a message to the INFO log level - see here for more details:
        # http://docs.python.org/2/library/logging.html
        _log.info("Responding to %r in %r", actor, recipient)

        # The 'reply' function automatically sends a replying PM if
        # the bot was PM'd, or addresses the user in a channel who
        # addressed the bot in a channel.
        client.reply(recipient, actor, "WHISKEY!!!!!")

        # Stop any other modules from handling this message.
        return True

module = WhiskeyBotModule
