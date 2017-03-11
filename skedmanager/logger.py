#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2017--2020, Shanghai Astronomical Observatory.
# All rights reserved.
"""custom logger
"""
import logging

# default message names
defaultMsgnames = ['debug', 'info', 'warning', 'info', 'critical']
# custom message names
msgnames = ['debug', 'info', 'warning', 'info', 'critical', 'record']


def addLoggingRecordLevel():
    """add a new logging level record to the `logging` module
    """
    level = 60
    levelName = 'RECORD'
    methodName = levelName.lower()

    # define two method
    def logForLevel(self, message, *args, **kwargs):
        if self.isEnabledFor(level):
            self._log(level, message, args, **kwargs)

    def logToRoot(message, *args, **kwargs):
        logging.log(level, message, *args, **kwargs)

    logging.addLevelName(level, levelName)
    setattr(logging, levelName, level)
    setattr(logging.getLoggerClass(), methodName, logForLevel)
    setattr(logging, methodName, logToRoot)


def init_logger(msglev='info', logfile=None):
    """init the logging logger"""
    # add a logging level RECORD
    addLoggingRecordLevel()

    # message to logging level
    msgname2level = {'debug': logging.DEBUG,
                     'info': logging.INFO,
                     'warning': logging.WARNING,
                     'error': logging.ERROR,
                     'critical': logging.CRITICAL,
                     'record': logging.RECORD}
    level = msgname2level[msglev.lower()]
    # set the logging config
    logfmt = '%(asctime)s:%(module)s:%(levelname)s:%(message)s'
    datefmt = '%Y-%m-%dT%Hh%Mm%Ss'
    logging.basicConfig(level=level, format=logfmt,
                        datefmt=datefmt, filename=logfile)
    # add stream handler
    logfmt = '%(asctime)s:%(levelname)s:%(message)s'
    formatter = logging.Formatter(logfmt, datefmt=datefmt)
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    ch.setFormatter(formatter)
    logging.getLogger("").addHandler(ch)
