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

class LvmRaw:
    """
    This class is used to retrieve useful information
    from LVM through Fabric API.
    """
    def __init__(self):
        self.fabric = remotefabric.CmdFabric()

    def lvmpv(self):
        """Retrieve result of pvs command through Fabric API"""
        return self.fabric.sudo_fabric("pvs --separator :")

    def lvmvg(self):
        """Retrieve result of vgs command through Fabric API"""
        return self.fabric.sudo_fabric("vgs --separator :")

    def lvmlv(self):
        """Retrieve result of lvdisplay command through Fabric API"""
        return self.fabric.sudo_fabric("lvdisplay -C --separator :")

class LvmProcessing:
    """Use to data retrieved processing"""
    def __init__(self):
        self.lvm = LvmRaw()

    @staticmethod
    def _build_list(lvm_raw):
        """Use to build generic list"""
        lvm_split = lvm_raw.splitlines()
        lvm_list = []
        key = lvm_split[0].split(':')
        for args in lvm_split[1:]:
            arg = args.strip()
            value = arg.split(':')
            lvm_list.append(dict(zip(key, value)))
        return lvm_list

    def build_lvmpv(self):
        """Build a list of usefull information retrieve from lvm pv"""
        return self._build_list(self.lvm.lvmpv())

    def build_lvmvg(self):
        """Build a list of usefull information retrieve from lvm vg"""
        return self._build_list(self.lvm.lvmvg())

    def build_lvmlv(self):
        """Build a list of usefull information retrieve from lvm lv"""
        return self._build_list(self.lvm.lvmlv())
