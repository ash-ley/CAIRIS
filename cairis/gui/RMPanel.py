#  Licensed to the Apache Software Foundation (ASF) under one
#  or more contributor license agreements.  See the NOTICE file
#  distributed with this work for additional information
#  regarding copyright ownership.  The ASF licenses this file
#  to you under the Apache License, Version 2.0 (the
#  "License"); you may not use this file except in compliance
#  with the License.  You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing,
#  software distributed under the License is distributed on an
#  "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#  KIND, either express or implied.  See the License for the
#  specific language governing permissions and limitations
#  under the License.


import wx
import os
from cairis.core.armid import *
from EditorBase import EditorBase
from RequirementsGrid import RequirementsGrid

NAME_POS = 0
DESCRIPTION_POS = 1
PRIORITY_POS = 2
RATIONALE_POS = 3
FITCRITERION_POS = 4
ORIGINATOR_POS = 5
TYPE_POS = 6

class RMPanel(EditorBase):
  def __init__(self,parent,id):
    self.objectDimension = 'asset'
    self.objectLabel = 'Assets'
    EditorBase.__init__(self,parent,id)
    self.grid = RequirementsGrid(self,self.modCombo,self.envCombo)
    self.sizer.Add( self.grid,1,wx.EXPAND )
    self.resizeColumns()
    self.SetSizeHints(1225,400)
    self.SetSizer(self.sizer)
    self.Bind(wx.EVT_COMBOBOX, self.onObjectChange,id = RMFRAME_TOOL_COMBOOBJECT)
    self.Bind(wx.EVT_COMBOBOX, self.onEnvironmentChange,id = RMFRAME_TOOL_COMBOENVIRONMENT)

  def onObjectChange(self,evt):
    self.envCombo.SetValue('')
    self.refresh()

  def onEnvironmentChange(self,evt):
    self.modCombo.SetValue('')
    self.refresh()


  def resizeColumns(self):
    self.grid.SetColSize(NAME_POS,150)
    self.grid.SetColSize(DESCRIPTION_POS,250)
    self.grid.SetColSize(PRIORITY_POS,65)
    self.grid.SetColSize(RATIONALE_POS,150)
    self.grid.SetColSize(FITCRITERION_POS,250)
    self.grid.SetColSize(ORIGINATOR_POS,100)
    self.grid.SetColSize(TYPE_POS,115)
    self.grid.SetDefaultRowSize(35)

  def relabel(self):
    pass

  def addObject(self):
    grid = self.FindWindowById(ID_REQGRID)
    pos = grid.GetGridCursorRow()
    grid.InsertRows(pos)

