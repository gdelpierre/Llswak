#! /bin/python env
# -*- coding: utf-8 -*-

# If you're using python 2.5
from __future__ import with_statement

"""Define here your command to the Fabric API"""

__docformat__ = 'restructuredtext en'

import remotefabric

__author__ = "Guillaume Delpierre"
__credits__ = "Guillaume Delpierre"
__license__ = "beerware"
__maintainer__ = "Guillaume Delpierre"
__email__ = "gde@nbs-system.com"
__status__ = "Development"

class XenRaw:
    """
    This class is used to retrieve useful information
    from Xen through Fabric API.
    """
    def __init__(self):
        self.fabric = remotefabric.CmdFabric()

    def xm_info(self):
        """Retrieve result of xm info command through Fabric API"""
        cmd_xm = ("xm info")
        cmd_xmext = ("%s -c" % (cmd_xm))
        return self.fabric.sudo_fabric("%s && %s" % (cmd_xm, cmd_xmext))

    def xm_list(self):
        """Retrieve result of xm list command through Fabric API"""
        return self.fabric.sudo_fabric("xm list")

class XenProcessing:
    """Use to data retrieved processing"""
    def __init__(self):
        self.xm = XenRaw()

    def build_xminfo(self):
        """Build a dictionnary from xm info output"""
        raw_split = self.xm.xm_info().splitlines()
        xm_entries = {}
        for line in raw_split:
            if not line.startswith('    '):
                key, value = line.split(':', 1)
                key = key.strip()
                xm_entries[key] = value.strip()
            else:
                secondlinevalue = " ".join(line.split())
                xm_entries[key] = xm_entries[key] + ' ' + secondlinevalue
        
        return xm_entries

    def build_xmlist(self):
        """Build a list of virtual servers located on dom0"""
        raw_split = self.xm.xm_list().splitlines()
        vservers = []
        key = raw_split[0].split()
        for line in raw_split[1:]:
            value = line.split()
            vservers.append(dict(zip(key, value)))

        return vservers

class ProcessingAvailableResources:
    """Use to processing available resources on dom0 and domus"""
    def __init__(self):
        self.dom0 = XenProcessing().build_xminfo()
        self.domus = XenProcessing().build_xmlist()

    def used_cpus(self):
        """Number of used CPUs on dom0"""
        domus = self.domus

        return sum([int(domu['VCPUs']) for domu in domus])
    
    def free_cpus(self, used_cpus):
        """Number of free CPUs on dom0"""
        dom0 = self.dom0
        
        return int(dom0['nr_cpus']) - self.used_cpus()
