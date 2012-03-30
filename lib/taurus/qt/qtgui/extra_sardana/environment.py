#!/usr/bin/env python

#############################################################################
##
## This file is part of Taurus, a Tango User Interface Library
## 
## http://www.tango-controls.org/static/taurus/latest/doc/html/index.html
##
## Copyright 2011 CELLS / ALBA Synchrotron, Bellaterra, Spain
## 
## Taurus is free software: you can redistribute it and/or modify
## it under the terms of the GNU Lesser General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
## 
## Taurus is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU Lesser General Public License for more details.
## 
## You should have received a copy of the GNU Lesser General Public License
## along with Taurus.  If not, see <http://www.gnu.org/licenses/>.
##
#############################################################################

"""This module contains a taurus environment widgets."""

__all__ = ["SardanaEnvironmentTreeWidget"]

__docformat__ = 'restructuredtext'

from taurus.core import TaurusDevice
from taurus.qt import Qt
from taurus.qt.qtcore.tango.sardana.model import SardanaEnvironmentModel
from taurus.qt.qtgui.tree import TaurusBaseTreeWidget


class SardanaEnvironmentTreeWidget(TaurusBaseTreeWidget):
    
    KnownPerspectives = { "Type" : {
                          "label" : "By key",
                          "icon" : ":/python-file.png",
                          "tooltip" : "View elements by key",
                          "model" : [SardanaEnvironmentModel],
                        },
    }
    DftPerspective = "Type"
        
    def getModelClass(self):
        return TaurusDevice
    
    @classmethod
    def getQtDesignerPluginInfo(cls):
        ret = TaurusBaseTreeWidget.getQtDesignerPluginInfo()
        ret['module'] = 'taurus.qt.qtgui.extra_sardana'
        ret['group'] = 'Taurus Extra Sardana'
        ret['icon'] = ":/designer/listview.png"
        return ret


def main_SardanaTreeWidget(device):
    w = SardanaEnvironmentTreeWidget(with_navigation_bar=True)
    w.setWindowTitle("Sardana browser - " + device)
    w.setModel(device)
    w.setMinimumSize(400,800)
    w.show()
    return w

def demo(device="V3"):
    """"""
    w = main_SardanaTreeWidget(device)
    return w

def main():
    import sys
    import taurus.qt.qtgui.application
    Application = taurus.qt.qtgui.application.TaurusApplication
    
    app = Application.instance()
    owns_app = app is None
    
    if owns_app:
        app = Application(app_name="Sardana environment tree demo", app_version="1.0",
                          org_domain="Taurus", org_name="Tango community")
    
    args = app.get_command_line_args()
    if len(args)==1:
        w = demo(device=args[0])
    else:
        w = demo()
        
    w.show()
    if owns_app:
        sys.exit(app.exec_())
    else:
        return w
    
if __name__ == "__main__":
    main()


