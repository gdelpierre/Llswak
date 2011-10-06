#! /bin/python env
# -*- coding: utf-8 -*-
"""
Retrieves the return of control over LVM Fabric.
Can also process the output of LVM.
"""

# If you're using python 2.5
from __future__ import with_statement

__docformat__ = 'restructuredtext en'

import fabric.context_managers
import remotefabric

__author__ = "Guillaume 'Llew' Delpierre"
__credits__ = "Guillaume 'Llew' Delpierre"
__license__ = "beerware"
__maintainer__ = "Guillaume 'Llew' Delpierre"
__email__ = "gde@nbs-system.com"
__status__ = "Development"

class Lvm(object):
    """
    This class is used to retrieve useful information
    from LVM through Fabric API.
    """
    def __init__(self):
        self.fabric = remotefabric.CmdFabric()

    def lvmpv(self):
        """Retrieve result of pvs command through Fabric API"""
        try:
            return self.fabric.sudo_fabric("pvs --separator :")
        except Exception:
            raise RunTimeError("Command pvs not found")

    def lvmvg(self):
        """Retrieve result of vgs command through Fabric API"""
        try:
            return self.fabric.sudo_fabric("vgs --separator :")
        except Exception:
            raise RunTimeError("Command vgs not found")

    def lvmlv(self):
        """Retrieve result of lvdisplay command through Fabric API"""
        try:
            return self.fabric.sudo_fabric("lvdisplay -C --separator :")
        except Exception:
            raise RunTimeError("Command lvdisplay not found")

    @staticmethod
    def _build_list(lvm_raw):
        """Use to build generic list."""
        lvm_split = lvm_raw.splitlines()
        if lvm_raw.return_code != 0:
            return list()
        else:
            lvm_list = list()
            key = lvm_split[0].split(':')
            for args in lvm_split[1:]:
                arg = args.strip()
                value = arg.split(':')
                lvm_list.append(dict(zip(key, value)))
            return lvm_list

    def build_lvmpv(self):
        """Build a list of usefull information retrieve from lvm pv."""
        return self._build_list(self.lvmpv())

    def build_lvmvg(self):
        """Build a list of usefull information retrieve from lvm vg."""
        return self._build_list(self.lvmvg())

    def build_lvmlv(self):
        """Build a list of usefull information retrieve from lvm lv."""
        return self._build_list(self.lvmlv())
