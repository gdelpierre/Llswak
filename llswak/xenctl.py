#! /bin/python env
# -*- coding: utf-8 -*-
"""Define here your command to the Fabric API"""

# If you're using python 2.5
from __future__ import with_statement

__docformat__ = 'restructuredtext en'

import remotefabric

__author__ = "Guillaume 'Llew' Delpierre"
__credits__ = "Guillaume 'Llew' Delpierre"
__license__ = "beerware"
__maintainer__ = "Guillaume 'Llew' Delpierre"
__email__ = "gde@nbs-system.com"
__status__ = "Development"

class Xen(object):
    """
    This class is used to retrieve useful information
    from Xen through Fabric API.
    """
    def __init__(self, load=True):
    # True by default, explain specify False whem you need it.
        self.fabric = remotefabric.CmdFabric()
        self.xm_entries = None
        self.vservers = None
        self.name = ""
        self.cpus = ""
        self.free_memory = ""
        self.total_memory = ""
        self.used_memory = ""
        if load:
            self.load_xm_info()
            self.load_xm_list()
        
    def raw_xm_info(self):
        """Retrieve result of xm info command through Fabric API"""
        cmd_xm = ("xm info")
        cmd_xmext = ("%s -c" % (cmd_xm))
        return self.fabric.sudo_fabric("%s && %s" % (cmd_xm, cmd_xmext))

    def raw_xm_list(self):
        """Retrieve result of xm list command through Fabric API"""
        return self.fabric.sudo_fabric("xm list")

    def load_xm_info(self):
        """Build a dictionnary from xm info output"""
        raw_split = self.raw_xm_info().splitlines()
        xm_entries = {}
        for line in raw_split:
            if not line.startswith('    '):
                key, value = line.split(':', 1)
                key = key.strip()
                xm_entries[key] = value.strip()
            else:
                secondlinevalue = " ".join(line.split())
                xm_entries[key] = xm_entries[key] + ' ' + secondlinevalue
        
        self.name = xm_entries['host']
        self.cpus = int(xm_entries['nr_cpus'])
        self.total_memory = int(xm_entries['total_memory'])
        self.free_memory = int(xm_entries['free_memory'])
        self.used_memory = int(self.total_memory - self.free_memory)
        return xm_entries

    def load_xm_list(self):
        """Build a list of virtual servers located on dom0"""
        raw_split = self.raw_xm_list().splitlines()
        vservers = []
        key = raw_split[0].split()
        for line in raw_split[1:]:
            value = line.split()
            vservers.append(dict(zip(key, value)))
        return vservers

    def domus(self):
        """Load vservers informations"""
        if None == self.vservers:
            self.load_xm_list()
        return self.vservers

    def dom0(self):
        """Load dom0 informations"""
        if None == self.xm_entries:
            self.load_xm_info()
        return self.xm_entries

    def used_cpus(self):
        """Number of used CPUs on dom0"""
        domus = self.domus()
        return sum([int(domu['VCPUs']) for domu in domus])
    
    def free_cpus(self):
        """Number of free CPUs on dom0"""
        return self.cpus - self.used_cpus()

    def __repr__(self):
        return "dom0: %s - %s CPUs - %s MB (free) / %s MB (total)" \
                " / %s MB (used)" %  (self.name, self.cpus, self.free_memory, 
                                        self.total_memory, self.used_memory)
