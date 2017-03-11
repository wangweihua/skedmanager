#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2017--2020, Shanghai Astronomical Observatory.
# All rights reserved.
"""sked automated runner for geovlbi

this script depends on download program and update program
Please changes the configure file manager.conf

type 'skedrunner.py <obscode>' to run the program
type "skedrunner.py -h" to see usage.
"""
import argparse
import datetime
import time
import imp
import logging
import os
import subprocess
import pexpect

import logger
import myemail
import version


class SkedRunner(object):
    """Sked automated Runner
    """
    def __init__(self, settings):
        self.email = myemail.SmtpEmail(settings)
        self.receivers = settings['receivers']
        self.logging_dir = settings['logging_dir']

    def sked(self):
        """run sked"""
        command = 'python'
        child = pexpect.spawn(command)
        child.expect('>>>')
        print(child.before)

        subcmd = '1 + 1'
        child.sendline(subcmd)
        child.expect('>>>')
        print(child.before)


    def run(self, obscode):
        """download and update the data"""
        # get the log file
        tmpfn = '{0}.log'.format(obscode)
        logfile = os.path.join(self.logging_dir, tmpfn)

        self.sked()


class PMain(object):
    """Python Main class
    """
    def __init__(self):
        # parse the command line
        self.parseCommandline()

        # parse the configure file
        self.parseConfigfile(self.configfile)

        # init the logger
        self.initLogger()

    def parseCommandline(self):
        """parse the command line
        """
        parser = argparse.ArgumentParser(
            description="SHAO Sked Runner for VLBI geodesy observations")
        parser.add_argument('obscodes', metavar='obscodes', nargs='+',
                            help='the code of geodesy observations')
        parser.add_argument('--config', action='store', dest='configfile',
                            help='Specify the configure file.')
        parser.add_argument('-m', '--msglev', action='store', dest='msglev',
                            default='info', choices=logger.msgnames,
                            help='Specify the logging msglev.')
        parser.add_argument('-l', '--logfile', action='store', dest='logfile',
                            help='Specify the logging logfile.')
        parser.add_argument('-v', '--version', action='version',
                            version=version.__version__,
                            help='Print the program version.')
        args = parser.parse_args()

        # config file
        if args.configfile is not None:
            self.configfile = args.configfile
        else:
            # use default config file
            self.configfile = self.getDefaultConfigfile()
        # obscodes
        self.obscodes = args.obscodes
        self.msglev = args.msglev
        self.logfile = args.logfile

    def getDefaultConfigfile(self):
        """return the default config file"""
        configfile = 'skedrunner.conf'
        if not os.path.exists(configfile):
            configfile = '.skedrunnerconf'

        return configfile

    def parseConfigfile(self, configfile):
        """Load the configure file
        """
        # import the manager configfile (.py)
        try:
            settings = imp.load_source('settings', configfile)
        except:
            import settings

        self.settings = {}
        # contact person and logging file
        self.settings['host'] = settings.host
        self.settings['port'] = settings.port
        self.settings['user'] = settings.user
        self.settings['password'] = settings.password
        self.settings['receivers'] = settings.receivers
        self.settings['logging_dir'] = settings.logging_dir
        # use the default logging file if not specified by user
        if self.logfile is None:
            self.logfile = settings.logging_file

    def initLogger(self):
        """init logger"""
        logger.init_logger(self.msglev, self.logfile)

    def check_input(self):
        """check the user inputs
        """
        logging.record('configfile = %s', self.configfile)
        logging.record('obscodes: %s', ', '.join(self.obscodes))
        logging.record('receivers: %s', self.settings['receivers'])

    def mainloop(self):
        """the main loop
        """
        # check the input
        self.check_input()

        # build a sked
        sked = SkedRunner(self.settings)
        for obscode in self.obscodes:
            logging.record('run sked to prepare the %s observation', obscode)
            sked.run(obscode)
            logging.record("finished to sched the observation")


def main():
    """the main entry
    """
    p = PMain()
    p.mainloop()


if __name__ == "__main__":
    main()
