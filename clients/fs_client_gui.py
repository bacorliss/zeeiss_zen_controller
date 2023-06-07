#!/usr/bin/env python
"""
Copyright (c) 2012, Bruce A. Corliss
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
    * Neither the name of the BACETech Consulting nor the
      names of its contributors may be used to endorse or promote products
      derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL Bruce A. Corliss BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
import wx
import os
import shutil

class TextFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, 'Zen Controller Debug Client', size=(350, 340))
        self.panel = wx.Panel(self, -1)
        # First GUI line
        self.multiLabel = wx.StaticText(self.panel, -1, "Micro COM File", pos=(10,10))
        self.comFilePath = wx.TextCtrl(self.panel, -1, "C:\micro_com.txt", pos=(100, 10), size=(200, 20))
        self.browse_button = wx.Button(self.panel, -1, "...", pos=(310, 10), size=(20,20))

        self.multiLabel = wx.StaticText(self.panel, -1, "Enter Commands Here", pos=(10,50))
        self.multiText = wx.TextCtrl(self.panel, -1,"",size=(320, 200), style=wx.TE_MULTILINE, pos=(10,70))
        self.com_button = wx.Button(self.panel, -1, "Send Command", pos=(10, 280), size=(100,20))
        self.clearText_checkbox = wx.CheckBox(self.panel, -1, 'Clear Text on Command', (200, 285))
        self.clearText_checkbox.SetValue(True)
        self.multiText.SetInsertionPoint(0)

        
        

        self.browse_button.Bind(wx.EVT_BUTTON, self.OnButtonClick, self.browse_button)
        self.com_button.Bind(wx.EVT_BUTTON, self.SendCommand, self.com_button)


    def OnButtonClick(self, event):
        self.panel.Refresh()

    def SendCommand(self, event):
        com_txt =  self.multiText.GetLabelText()

        # Write command to temp file
        f = open(os.path.split(__file__)[0] + '/temp_micro_com.txt', 'w')
        f.write(com_txt)
        f.close()
        # Copy file to where the communication text file is
        shutil.copyfile(os.path.split(__file__)[0] + '/temp_micro_com.txt', self.comFilePath.GetLabelText())

        if self.clearText_checkbox.GetValue():
            self.multiText.SetLabel("")


def main():
    app = wx.PySimpleApp()
    frame = TextFrame()
    frame.Show()
    app.MainLoop()




if __name__ == "__main__":
    main()
