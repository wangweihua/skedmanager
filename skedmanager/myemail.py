#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2017--2020, Shanghai Astronomical Observatory.
# All rights reserved.
"""Smtp Email Wraplibary.
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header


class SmtpEmail(object):
    """SMTP Email"""
    def __init__(self, settings):
        self.host = settings['host']
        self.port = settings.get('port', 25)
        self.user = settings['user']
        self.password = settings['password']

    def sendemail(self, receivers, sub, contents):
        """send an email to tolist
        """
        # Create a text/plain message
        msg = MIMEText(contents, _subtype='plain')
        msg['Subject'] = sub
        msg['From'] = self.user
        msg['To'] = ';'.join(receivers)

        # Send the message via the SMTP server
        try:
            smtp = smtplib.SMTP()
            # for SMTP AUTH extension
            smtp.connect(self.host, self.port)
            smtp.starttls()
            smtp.login(self.user, self.password)
            smtp.sendmail(self.user, receivers, msg.as_string())
            smtp.close()
            return True
        except Exception as err:
            logging.error('Failed to send email: %s', err)
            return False

    def sendemail_attach(self, receivers, sub, contents, attachfile):
        """send an email to tolist
        """
        # Create a MIMEMultipart with an attach
        msg = MIMEMultipart()
        msg['From'] = Header(self.user)
        msg['To'] = Header(';'.join(receivers))
        msg['Subject'] = Header(sub)
        # contents
        msg.attach(MIMEText(contents, _subtype='plain'))
        # attach file
        att1 = MIMEText(open(attachfile, 'r').read(), 'base64')
        att1["Content-Type"] = 'application/octet-stream'
        filename = os.path.basename(attachfile)
        disposition = 'attachment; filename="{0}"'.format(filename)
        att1["Content-Disposition"] = disposition
        msg.attach(att1)
        # Send the message via the SMTP server
        try:
            smtp = smtplib.SMTP()
            # for SMTP AUTH extension
            smtp.connect(self.host, self.port)
            smtp.starttls()
            smtp.login(self.user, self.password)
            smtp.sendmail(self.user, receivers, msg.as_string())
            smtp.close()
            return True
        except Exception as err:
            logging.error('Failed to send email: %s', err)
            return False
