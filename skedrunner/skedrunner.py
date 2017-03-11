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
import configparser
import logging
import os
import pexpect
import sys
import yaml

import logger
import version


class SkedRunner(object):
    """Sked automated Runner"""
    def __init__(self, settings):
        self.receivers = settings['email_receivers']
        self.logger_topdir = settings['logger_topdir']
        self.commandsfile = settings['commandsfile']
        self.commands = self.loadCommandsfile(self.commandsfile)
        self.program = self.commands['program']
        self.subcommands = self.commands['subcommands']

    def loadCommandsfile(self, commandsfile):
        """load the commands file"""
        with open(commandsfile, 'r') as fh:
            try:
                return yaml.load(fh)
            except yaml.YAMLError as err:
                logging.error('Failed to load %s yaml file：%s',
                              commandsfile, err)

    def sked(self, obscode, logfile):
        """run sked"""
        logging.info('run %s', self.program)
        child = pexpect.spawn(self.program)
        child.expect('>>>')
        logging.info(child.before)

        for subcmd in self.subcommands:
            logging.info('>>> %s', subcmd)
            child.sendline(subcmd)
            child.expect('>>>')
            logging.info(child.before)

    def run(self, obscode):
        """download and update the data"""
        # get the log file
        tmpfn = '{0}.log'.format(obscode)
        logfile = os.path.join(self.logger_topdir, tmpfn)
        # execute the sked
        self.sked(obscode, logfile)


class PMain(object):
    """Python Main class"""
    def __init__(self):
        # parse the command line
        self.parseCommandline()

        # parse the configure file
        self.parseConfigfile()

        # init the logger
        self.initLogger()

    def parseCommandline(self):
        """parse the command line"""
        parser = argparse.ArgumentParser(
            description='SHAO Sked Runner for geodestic VLBI observations')
        parser.add_argument('obscodes', metavar='obscodes', nargs='+',
                            help='the code of geodesy observations')
        configfile = self.getDefaultConfigfile()
        parser.add_argument('--config', action='store', dest='configfile',
                            default=configfile,
                            help='Specify the configure file.')
        parser.add_argument('--commands', action='store', dest='commandsfile',
                            help='Specify the sked commands file.')
        parser.add_argument('-m', '--msglev', action='store', dest='msglev',
                            default='info', choices=logger.msgnames,
                            help='Specify the logging msglev.')
        parser.add_argument('-l', '--logfile', action='store', dest='logfile',
                            help='Specify the logging logfile.')
        parser.add_argument('-v', '--version', action='version',
                            version=version.__version__,
                            help='Print the program version.')
        args = parser.parse_args()

        self.configfile = args.configfile
        self.commandsfile = args.commandsfile
        self.obscodes = args.obscodes
        self.msglev = args.msglev
        self.logfile = args.logfile

    def getDefaultConfigfile(self):
        """return the default config file"""
        configfile = 'skedrunner.conf'
        if not os.path.exists(configfile):
            configfile = os.path.join(os.getenv('HOME'), '.skedrunnerconf')

        return configfile

    def parseConfigfile(self):
        """Parse the configure file"""
        configfile = self.configfile
        if not os.access(configfile, os.F_OK):
            logging.final('Failed to access configure file %s', configfile)
            sys.exit(-1)

        # settings from config file
        self.settings = {}
        # read the file with configparser
        cfg = configparser.ConfigParser()
        cfg.read(configfile)
        try:
            if self.commandsfile is None:
                self.settings['commandsfile'] = cfg.get('sked', 'commands')
            else:
                self.settings['commandsfile'] = self.commandsfile

            # email
            self.settings['email_host'] = cfg.get('email', 'host')
            self.settings['email_port'] = cfg.get('email', 'port')
            self.settings['email_user'] = cfg.get('email', 'user')
            self.settings['email_password'] = cfg.get('email', 'password')
            self.settings['email_receivers'] = cfg.get('email', 'receivers')

            # logger
            self.settings['logger_topdir'] = cfg.get('logger', 'topdir')
            # use the default logger file if not specified
            if self.logfile is None:
                self.logfile = cfg.get('logger', 'logfile')
        except configparser.NoSectionError as err:
            logging.error("Failed to read configure file %s:%s",
                          configfile, err)
            sys.exit(-1)
        except configparser.NoOptionError as err:
            logging.error("Failed to read configure file %s:%s",
                          configfile, err)
            sys.exit(-1)

    def initLogger(self):
        """init the application logger"""
        logger.init_logger(self.msglev, self.logfile)

    def check_input(self):
        """check the user inputs"""
        logging.record('configfile = %s', self.configfile)
        logging.record('obscodes: %s', ', '.join(self.obscodes))

        commandsfile = self.settings['commandsfile']
        if not os.path.exists(commandsfile):
            logging.error('no commands file %s', commandsfile)
            sys.exit(-1)
        logging.record('commandsfile = %s', commandsfile)

    def mainloop(self):
        """the main loop"""
        self.check_input()

        # build a sked runner
        sked = SkedRunner(self.settings)
        for obscode in self.obscodes:
            logging.record('schedule geodetic VLBI observation %s', obscode)
            sked.run(obscode)
            logging.record("finished the VLBI observation")


def main():
    """the main entry"""
    p = PMain()
    p.mainloop()


if __name__ == "__main__":
    main()
