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
import socket
import sys
import time
import threading

tcp_socket = None
recieve_timer = None

CMD_DELIM_DEFAULT = ';'
MSG_DELIM_DEFAULT = ';;'
APP_W = 700
APP_H = 700
PAD=10
BUFFER_SIZE = 1024


class TextFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, 'Zen Controller Debug Client', size=(APP_W , APP_H))
        # Add panel
        self.panel = wx.Panel(self, wx.ID_ANY)
        # TCP Connection Objects
        self.hostAddress_text = wx.StaticText(self.panel, -1, "IP Address", pos=(150,10))
        self.hostAddress_edit = wx.TextCtrl(self.panel, -1, "127.0.0.1", pos=(210, 10), size=(75, 15))
        self.hostPort_text = wx.StaticText(self.panel, -1, "Port", pos=(150, 25), size=(20,20))
        self.hostPort_edit = wx.TextCtrl(self.panel, -1, "22500", pos=(210, 25), size=(75, 15))
        self.connect_toggle = wx.ToggleButton(self.panel, -1, "Connect", pos=(10, 8), size=(100,35))

        self.cmdDelim_edit = wx.StaticText(self.panel, -1, "Cmd Delim", pos=(330, 10))
        self.cmdDelim_edit = wx.TextCtrl(self.panel, -1, CMD_DELIM_DEFAULT, pos=(390, 10), size=(25, 15))
        self.msgDelim_edit = wx.StaticText(self.panel, -1, "Msg Delim", pos=(330, 25))
        self.msgDelim_edit = wx.TextCtrl(self.panel, -1, MSG_DELIM_DEFAULT, pos=(390, 25), size=(25, 15))
        # Command input
        self.command_text = wx.StaticText(self.panel, -1, "Enter Commands (one per line, no Cmd or Msg Delims).", pos=(10,50))
        self.command_edit = wx.TextCtrl(self.panel, -1,"",size=(APP_W - 3*PAD, 200),
                                          style=wx.TE_MULTILINE, pos=(PAD,70))
        self.command_edit.SetInsertionPoint(0)
        self.com_button = wx.Button(self.panel, -1, "Send all Commands", pos=(10, 275), size=(100,20))
        self.clearText_checkbox = wx.CheckBox(self.panel, -1, 'Clear Text on Send', (APP_W-150, 280))
        self.loopCmd_checkbox = wx.CheckBox(self.panel, -1, 'Loop Send', (120, 280))
        self.clearText_checkbox.SetValue(False)
        # Server response
        self.output_text = wx.StaticText(self.panel, -1, "Output", pos=(PAD,305))
        self.output_edit = wx.TextCtrl(self.panel, -1,'',size=(APP_W - 3*PAD, 325),
                                          style=wx.TE_MULTILINE, pos=(PAD,320))
        self.output_edit.SetEditable(False)

        # Callbacks
        self.command_edit.Bind(wx.EVT_CHAR, self.onCharEvent)
        self.com_button.Bind(wx.EVT_BUTTON, self.SendCommand, self.com_button)
        self.connect_toggle.Bind(wx.EVT_TOGGLEBUTTON, self.ConnectCallback, self.connect_toggle)

        
    def ConnectCallback(self, event):
        """ Initialize TCP connection and then start a new thread to listen for messages."""
        if self.connect_toggle.GetValue():
            self.LogThis("Attempting to connect...")
            self.connect_toggle.SetLabel("Disconnect")
            self.TcpConnect()
        else:
            self.LogThis("Disconnecting...")
            self.connect_toggle.SetLabel("Connect")
            if not tcp_socket and tcp_socket.isalive():
                # Closing tcp connection
                tcp_socket.close()
            
 
    def TcpConnect(self):
        global tcp_socket
        host = self.hostAddress_edit.GetLabel()
        port = self.hostPort_edit.GetLabel()
        # Connect to server
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.LogThis("Connecting to: " + host + ": " + port)
        tcp_socket.connect((host,int(port)))      


            
    def ContinuousRecieveData(self, event):
        """ Wait for server to send data, and print to comamnd line."""
        global tcp_socket
        print "Waiting for server response"
        while True:
            buffer_str = "";
            while True:
                if not self.connect_toggle.GetValue(): return
                wx.Yield() 
                buffer_str += tcp_socket.recv(BUFFER_SIZE)
                print "Server response recieved"
                if buffer_str.find(MSG_DELIM) >= 0:
                    print  msg_str + "EOM"
                time.sleep(.5)

        
    def onCharEvent(self, event):
        keycode = event.GetKeyCode()
        controlDown = event.CmdDown()
        altDown = event.AltDown()
        shiftDown = event.ShiftDown()
        # Communication delimiters
        CMD_DELIM = self.cmdDelim_edit.GetValue()
        MSG_DELIM = self.msgDelim_edit.GetValue()
        
        if controlDown and keycode == wx.WXK_SPACE:
            # Send current line or selection to command window
            (ind1, ind2) = self.command_edit.GetSelection()
            if ind1 == ind2:
                curPos = self.command_edit.GetInsertionPoint()
                lineNum = len(self.command_edit.GetRange( 0, self.command_edit.GetInsertionPoint() ).split("\n"))-1
                msg_out = self.command_edit.GetLineText(lineNum)
                self.LogThis(msg_out + "\n")
                tcp_socket.sendall(msg_out + MSG_DELIM)
                # Recieve data until "DONE;;" is recieved
                self.RecieveServerResponse()
            else:
                lineNum1 = len(self.command_edit.GetRange( 0, ind1).split("\n"))-1
                lineNum2 = len(self.command_edit.GetRange( 0, ind2).split("\n"))
                msg_out = [self.command_edit.GetLineText(x) for x in range(lineNum1, lineNum2)]
                self.LogThis("Client:\t" + CMD_DELIM.join(msg_out) + CMD_DELIM + MSG_DELIM)
                tcp_socket.sendall(CMD_DELIM.join(msg_out) + MSG_DELIM)
                # Recieve data until Msg Delim
                self.RecieveServerResponse()
        else:
            event.Skip()


    def LogThis(self, output_str):
        print output_str
        self.output_edit.AppendText("\n" + output_str)
        self.output_edit.ShowPosition(self.output_edit.GetLastPosition())
        self.output_edit.Refresh()
        
    def RecieveServerResponse(self):
        global tcp_socket
        MSG_DELIM = self.msgDelim_edit.GetValue()
        CMD_DELIM = self.cmdDelim_edit.GetValue()
        buffer_str = ''
        while True:
            if not self.connect_toggle.GetValue(): return
            wx.Yield() 
            buffer_str += tcp_socket.recv(1024)
            if buffer_str.find("DONE" + MSG_DELIM) >= 0:
                
                self.LogThis("Server:\t" + (MSG_DELIM + "\nServer:\t").join(buffer_str.split(MSG_DELIM)[:-1]) + MSG_DELIM)
                break
            
        
    def OnButtonClick(self, event):
        self.panel.Refresh()


    def SendCommand(self, event):
        global tcp_socket
        MSG_DELIM = self.msgDelim_edit.GetValue()
        CMD_DELIM = self.cmdDelim_edit.GetValue()
        
        while True:
            wx.Yield() 
            msg_out =  self.command_edit.GetValue()
            
            self.LogThis("Client:\t" + (CMD_DELIM+' ').join(msg_out.split('\n')) + MSG_DELIM)
            tcp_socket.sendall(CMD_DELIM.join(msg_out.split('\n')) + MSG_DELIM)
            # Recieve data until Msg Delim
            self.RecieveServerResponse()
            if not self.loopCmd_checkbox.GetValue() or not self.connect_toggle.GetValue(): break
            time.sleep(1)
                
        



def main():
    app = wx.PySimpleApp()
    frame = TextFrame()
    frame.Show()
    app.MainLoop()




if __name__ == "__main__":
    main()
