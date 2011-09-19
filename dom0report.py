#!/usr/bin/env python
# -*- coding: utf-8 -*-

# If you're using python 2.5
from __future__ import with_statement

"""
Related usefull informations on dom0
Usage:
        fab -f dom0_report -h
"""

__docformat__ = 'restructuredtext en'

import os

import fabric.api
import fabric.operations

__author__ = "Guillaume Delpierre"
__credits__ = "Guillaume Delpierre"
__license__ = "beerware"
__maintainer__ = "Guillaume Delpierre"
__email__ = "gde@nbs-system.com"
__status__ = "Development"

# Get informations from Xen.

def get_xm_info():
    """Retrieve informations from xm info."""
    cmd_xm_info = "xm info"
    cmd_xm_info_c = "%s -c" % (cmd_xm_info)
    pid = fabric.api.sudo('kill -0 $(cat /var/run/xend.pid)', pty=True)
    xm_info_output = fabric.api.sudo("%s && %s" % \
                                    (cmd_xm_info, cmd_xm_info_c), \
                                    pty=True).split('\r\n')
    return xm_info_output

def get_xm_list():
    """Retrieve informations from xm list."""
    cmd_xm_list = "xm list"
    pid = fabric.api.sudo('kill -0 $(cat /var/run/xend.pid)', pty=True)
    xm_list_output = fabric.api.sudo("%s" % (cmd_xm_list), \
                                    pty=True).split("\r\n")
    return xm_list_output

def get_xm_list_extended():
    """Retrieve extended informations from xm list."""
    cmd_xm_list_l = "xm list -l"
    xm_list_l_output = fabric.api.sudo("%s" % (cmd_xm_list_l), \
                                        pty=True).split("\r\n")
    return xm_list_l_output

# Get informations from lvm

def get_lvmpv_infos():
    """Retrieve informations on physical volume"""
    cmd_pvs = "pvs --separator :"
    cmd_output = fabric.api.sudo("%s" % (cmd_pvs), pty=True).split("\r\n")
    return cmd_output

def get_lvmvg_infos():
    """Retrieve informations from lvm on non-diskless dom0"""
    cmd_vgs = "vgs --separator :"
    cmd_output = fabric.api.sudo("%s" % (cmd_vgs), pty=True).split("\r\n")
    return cmd_output

def get_lvmlv_infos():
    """lvm display infos"""
    cmd_lvm = "lvdisplay -C --separator :"
    cmd_output = fabric.api.sudo("%s" % (cmd_lvm), pty=True).split("\r\n")
    return cmd_output

# Get informations from dmidecode.

def get_memory_infos():
    """Retrieve memory info from dmidecode"""
    cmd_memory =  "dmidecode -t memory"
    get_memory = fabric.api.sudo("%s" % (cmd_memory), pty=True).split("\r\n")
    print get_memory
    return get_memory

def get_processor_type():
    """Retrieve processor type from dmidecode"""
    cmd_processor = "dmidecode -t processor"
    get_processor = fabric.api.sudo("%s" % (cmd_processor), \
                                    pty=True).split("\r\n")
    print get_processor
    return get_processor

# Structure retrieve informations

def get_dom0_infos():
    """Build a dictionnary from xm info output."""
    xm_info = get_xm_info()
    dom0 = {}
    for line in xm_info:
        if not line.startswith('   '):
            key, value = line.split(':', 1)
            key = key.strip()
            dom0[key] = value.strip()
        else:
            secondlinevalue = " ".join(line.split())
            dom0[key] = dom0[key] + ' ' + secondlinevalue
    return dom0

def get_domu_infos():
    """Build a list of virtual servers."""
    xm_list = get_xm_list()
    domus = []
    key = xm_list[0].split()
    for line in xm_list[1:]:
        values = line.split()
        domus.append(dict(zip(key, values)))
    return domus

# Build list from lvm informations

def build_lvmpv_list():
    """Build a list of usefull information retrieve from lvm pv"""
    lvmpv = get_lvmpv_infos()
    lvmpv_list = []
    key = lvmpv[0].split(':')
    for args in lvmpv[1:]:
        values = args.split(':')
        lvmpv_list.append(dict(zip(key, values)))
    return lvmpv_list

def build_lvmvg_list():
    """Build a list of usefull information retrieve from lvm vg"""
    lvmvg = get_lvmvg_infos()
    lvmvg_list = []
    key = lvmvg[0].split(':')
    for args in lvmvg[1:]:
        values = args.split(':')
        lvmvg_list.append(dict(zip(key, values)))
    return lvmvg_list

def build_lvmlv_list():
    """Build a list of usefull information retrieve from lvm lv"""
    lvmlv = get_lvmlv_infos()
    lvmlv_list = []
    key = lvmlv[0].split(':')
    for args in lvmlv[1:]:
        values = args.split(':')
        lvmlv_list.append(dict(zip(key, values)))
    return lvmlv_list

# vim:set et sts=4 ts=4 tw=80:
