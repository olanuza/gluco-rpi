# -*- coding: utf-8 -*-
"""Common exceptions for glucometerutils."""

__author__ = 'Diego Elio Pettenò'
__email__ = 'flameeyes@flameeyes.eu'
__copyright__ = 'Copyright © 2013, Diego Elio Pettenò'
__license__ = 'MIT'

from glucometerutils.status_support import status

class Error(Exception):
  """Base class for the errors."""

  def __str__(self):
    return self.message


class CommandLineError(Error):
  """Error with commandline parameters provided."""

  def __init__(self, message=''):
    status.show_status(1,"Error with commandline parameters provided.")
    self.message = message


class ConnectionFailed(Error):
  """It was not possible to connect to the meter."""

  def __init__(self, message='Unable to connect to the meter.'):
    status.show_status(1,"It was not possible to connect to the meter")
    self.message = message


class InvalidResponse(Error):
  """The response received from the meter was not understood"""

  def __init__(self, response):
    status.show_status(1,"The response received from the meter was not understood")
    self.message = 'Invalid response received:\n%s' % response


class InvalidChecksum(InvalidResponse):
  def __init__(self, expected, gotten):
    status.show_status(1,"The response received from the meter was not understood")
    self.message = (
      'Response checksum not matching: %08x expected, %08x gotten' %
      (expected, gotten))


class InvalidGlucoseUnit(Error):
  """Unable to parse the given glucose unit"""
  def __init__(self, unit):
    status.show_status(1,"Unable to parse the given glucose unit")
    self.message = 'Invalid glucose unit received:\n%s' % unit

#####
class db_error(Error):
  """Sqlite3 error message"""

  def __init__(self, response):
    status.show_status(1,"Sqlite3 error message")
    self.message = 'SQLite3 Data Base Error:\n%s' % response

class server_error(Error):
  """Server path error message"""

  def __init__(self, response):
    status.show_status(1,"Server path error message")
    self.message = 'Specify the server:\n%s' % response


#####