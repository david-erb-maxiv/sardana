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

"""Extension of :mod:`guiqwt.tools`"""



__docformat__ = 'restructuredtext'


from guiqwt.tools import CommandTool, DefaultToolbarID, QActionGroup, add_actions
from PyQt4 import Qt, Qwt5
from taurus.qt.qtgui.resource import getIcon
from taurus.qt.extra_guiqwt.builder import make
from taurus.qt.extra_guiqwt.curve import TaurusCurveItem
from taurus.qt.extra_guiqwt.curvesmodel import CurveItemConfDlg, CurveItemConf
from taurus.qt.qtgui.panel import TaurusModelChooser
from taurus.core import TaurusElementType
from taurus.qt.qtgui.plot import DateTimeScaleEngine

class TaurusCurveChooserTool(CommandTool):
    """
    A tool that shows the Taurus Model Chooser to create/edit the taurus curves of a plot
    """
    def __init__(self, manager, toolbar_id=DefaultToolbarID):
        super(TaurusCurveChooserTool,self).__init__(manager, "Taurus Models...", getIcon(":/taurus.png"), toolbar_id=toolbar_id)

    def activate_command(self, plot, checked):
        """Activate tool"""
        #retrieve current Taurus curves
        tauruscurves = [item for item in plot.get_public_items() if isinstance(item, TaurusCurveItem)]
        #show a dialog
        confs, ok = CurveItemConfDlg.showDlg(parent=plot, curves=tauruscurves)
        if ok:
            #remove previous taurus curves
            plot.del_items(tauruscurves)
            #create curve items and add them to the plot 
            for c in confs:
                if c.taurusparam.yModel:
                    item = make.pcurve(c.taurusparam.xModel or None, c.taurusparam.yModel, c.curveparam)
                    plot.add_item(item)
                    if c.axesparam is not None:
                        c.axesparam.update_axes(item)

class TaurusImageChooserTool(CommandTool):
    """
    A tool that shows the Taurus Model Chooser and adds new taurus image items to a plot
    """
    def __init__(self, manager, toolbar_id=DefaultToolbarID):
        super(TaurusImageChooserTool,self).__init__(manager, "Add Taurus images...", getIcon(":/taurus.png"), toolbar_id=toolbar_id)

    def activate_command(self, plot, checked):
        """Activate tool"""
        #show a dialog
        models, ok = TaurusModelChooser.modelChooserDlg(parent=plot, selectables=[TaurusElementType.Attribute])
        if ok:
            #create image items and add them to the plot 
            for m in models:
                item = make.image(taurusmodel=m)
                plot.add_item(item)


class TaurusModelChooserTool(CommandTool):
    """
    A tool that shows the Taurus Model Chooser and adds new taurus image items to a plot
    """
    def __init__(self, manager, toolbar_id=DefaultToolbarID):
        super(TaurusModelChooserTool,self).__init__(manager, "Add Taurus images...", getIcon(":/taurus.png"), toolbar_id=toolbar_id)

    def activate_command(self, plot, checked):
        """Activate tool"""
        #show a dialog
        models, ok = TaurusModelChooser.modelChooserDlg(parent=plot, selectables=[TaurusElementType.Attribute])
        if ok and len(models)==1:
            self.manager.setModel(models[0])
            
          
class TimeAxisTool(CommandTool):
    def __init__(self, manager):
        super(TimeAxisTool, self).__init__(manager, "Time Scale",
                                            icon=getIcon(":/status/awaiting.svg"),
                                            tip=None, toolbar_id=None)
        self.action.setEnabled(True)
                                 
    def create_action_menu(self, manager):
        """Create and return menu for the tool's action"""
        menu = Qt.QMenu()
        group = QActionGroup(manager.get_main())
        y_x = manager.create_action("y(x)", toggled=self.set_scale_y_x)
        y_t = manager.create_action("y(t)", toggled=self.set_scale_y_t)
        t_x = manager.create_action("t(x)", toggled=self.set_scale_t_x)
        t_t = manager.create_action("t(t)", toggled=self.set_scale_t_t)
        self.scale_menu = {(False, False): y_x, (False, True): y_t,
                           (True, False): t_x, (True, True): t_t}
        for obj in (group, menu):
           add_actions(obj, (y_x, y_t, t_x, t_t))
        return menu
    
    def _getAxesUseTime(self, item):
        """
        Returns a tuple (xIsTime, yIsTime) where xIsTime is True if the item's x
        axis uses a TimeScale. yIsTime is True if the item's y axis uses a Time
        Scale. Otherwise they are False.
        """
        plot = item.plot()
        if plot is None:
            return (False,False)
        xEngine = plot.axisScaleEngine(item.xAxis())
        yEngine = plot.axisScaleEngine(item.yAxis())
        return isinstance(xEngine, DateTimeScaleEngine), isinstance(yEngine, DateTimeScaleEngine)
         
    def update_status(self, plot):
        item = plot.get_active_item()
        active_scale = (False, False)
        if item is not None:
            active_scale = self._getAxesUseTime(item)
        for scale_type, scale_action in self.scale_menu.items():
            if item is None:
                scale_action.setEnabled(True)
            else:
                scale_action.setEnabled(True)
                if active_scale == scale_type:
                    scale_action.setChecked(True)
                else:
                    scale_action.setChecked(False)
                    
    def _setPlotTimeScales(self, xIsTime, yIsTime):
        plot = self.get_active_plot()
        if plot is not None:
            for axis,isTime in zip(plot.get_active_axes(), (xIsTime, yIsTime)):
                if isTime:
                    DateTimeScaleEngine.enableInAxis(plot, axis, rotation=-45)
                else:
                    DateTimeScaleEngine.disableInAxis(plot, axis)
            plot.replot()
            
        
    def set_scale_y_x(self, checked):
        if not checked:
            return
        self._setPlotTimeScales(False, False)
        
    def set_scale_t_x(self, checked):
        if not checked:
            return
        self._setPlotTimeScales(False, True)
    
    def set_scale_y_t(self, checked):
        if not checked:
            return
        self._setPlotTimeScales(True, False)
    
    def set_scale_t_t(self, checked):
        if not checked:
            return
        self._setPlotTimeScales(True, True)


def testTool(tool):
    from taurus.qt.qtgui.application import TaurusApplication
    from guiqwt.plot import CurveDialog
    import sys
    
    app = TaurusApplication()
    win = CurveDialog(edit=False, toolbar=True)
    win.add_tool(tool)
    win.show()
    win.exec_()
    
        
def test_timeAxis():
    testTool(TimeAxisTool)
#    testTool(TaurusCurveChooserTool)


if __name__ == "__main__":
    test_timeAxis()    