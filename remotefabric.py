#! /bin/python env
# -*- coding: utf-8 -*-

# If you're using python 2.5
from __future__ import with_statement

"""Define here your command to the Fabric API"""

__docformat__ = 'restructuredtext en'

import fabric.api

__author__ = "Guillaume Delpierre"
__credits__ = "Guillaume Delpierre"
__license__ = "beerware"
__maintainer__ = "Guillaume Delpierre"
__email__ = "gde@nbs-system.com"
__status__ = "Development"

# Xen run commands remotely with fabric API.

class CmdFabric(object):
    """foo"""
    def __init__(self):
        """foo"""
        
    @staticmethod
    def sudo_fabric(cmd):
        """foo"""
        return fabric.api.sudo("%s" % (cmd), pty=True)
        
    @staticmethod
    def run_fabric(cmd):
        """foo"""
        return fabric.api.run("%s" % (cmd), pty=True)
