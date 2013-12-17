#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# Copyright (C) 2013, Cameron White

import logging

from kitnirc.modular import Module

_log = logging.getLogger(__name__)

class NickToolsModule(Module):
    """A KitnIRC module which automatically configures nick.  """
    
    @Module.handle("WELCOME")
    def register_nick(self, client, hostmask):

        _log.info("Beginning automatic nick configuration...")

        host = client.server.host
        if self.controller.config.has_option(str(host), "nick"):
            nick = self.controller.config.get(str(host), "nick")
            client.nick(nick)
        if self.controller.config.has_option(str(host), "nick_password"):
            nick_password = self.controller.config.get(str(host), "nick_password")
            client.msg("NickServ", "IDENTIFY {}".format(nick_password))

        _log.info("Automatic nick configuration complete.")

module = NickToolsModule
