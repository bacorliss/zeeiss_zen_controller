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
import socket
import atexit
import threading

# Global Variables
tcp_socket = None
tcp_conn = None
listen_thread = None
listen_thread_pid = None

# Parameters
ID_START = wx.NewId()
ID_STOP = wx.NewId()

# Define notification event for thread completion
EVT_RESULT_ID = wx.NewId()


CMD_DELIM = ';'
MSG_DELIM = ';;'

BUFFER_SIZE = 1024
APP_W = 700
APP_H = 350
PAD=10

class TextFrame(wx.Frame):
    def __init__(self):
        """ Initialize tcp server gui."""
        wx.Frame.__init__(self, None, -1, 'Zen Controller Debug Server', size=(APP_W , APP_H))
        # Add panel
        self.panel = wx.Panel(self, wx.ID_ANY)
        # TCP Connection Objects
        self.hostAddress_text = wx.StaticText(self.panel, -1, "IP Address", pos=(10,10))
        self.hostAddress_edit = wx.TextCtrl(self.panel, -1, "127.0.0.1", pos=(100, 10), size=(75, 15))
        self.hostPort_text = wx.StaticText(self.panel, -1, "Port", pos=(10, 25), size=(20,20))
        self.hostPort_edit = wx.TextCtrl(self.panel, -1, "22500", pos=(100, 25), size=(75, 15))
        self.startserver_toggle = wx.ToggleButton(self.panel, -1, "Start Server", pos=(200, 8), size=(100,35))
        # Command input
        self.output_text = wx.StaticText(self.panel, -1, "Output", pos=(10,50))
        self.output_edit = wx.TextCtrl(self.panel, -1,"",size=(APP_W - 3*PAD, 200),
                                          style=wx.TE_MULTILINE, pos=(PAD,70))
        self.output_edit.SetEditable(False)

    
        # Callbacks
        self.startserver_toggle.Bind(wx.EVT_TOGGLEBUTTON, self.StartServer_Callback, self.startserver_toggle)
        # Recieve timer
        self.recieve_timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.TcpAcceptConnection, self.recieve_timer)


    def StartServer_Callback(self, event):
        """ Starts or stops acting as tcp server."""
        global listen_thread
        global listen_thread_pid
        global tcp_socket
        global tcp_conn

        if self.startserver_toggle.GetValue():
            self.LogThis("Starting server...")
            self.startserver_toggle.SetLabel("Stop Server")
            self.TcpServerConnect()
            # Start new thread for listening
            listen_thread = threading.Thread(target=self.TcpAcceptConnection)
            listen_thread.setDaemon(True)
            listen_thread.start()
        else:
            self.LogThis("Stopping server...")
            self.startserver_toggle.SetLabel("Start Server")
            # Close tcp connection if it exists
            if tcp_conn is not None: tcp_conn.close()
            if tcp_socket is not None: tcp_socket.close()           
            # Terminate listen thread if it exists
            if listen_thread is not None and listen_thread.isAlive():
                self.LogThis("Killing listen_thread: {0}".format(listen_thread_pid))
                os.popen("kill -9 " + str(listen_thread_pid))
                try: listen_thread._Thread__stop()
                except:  self.LogThis('Listen thread could not be terminated')
            tcp_conn = None
            tcp_socket = None
            


    def TcpServerConnect(self):
        """ Initialize tcp connection for server"""
        global tcp_socket
        global tcp_conn
        # Initialize tcp socket
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.LogThis("Binding and listening: " + self.hostAddress_edit.GetLabel() +
                     ": " + self.hostPort_edit.GetLabel())
        tcp_socket.bind((self.hostAddress_edit.GetLabel(), int(self.hostPort_edit.GetLabel())))
        tcp_socket.listen(1)

        

    
    def TcpAcceptConnection(self):
        """ Monitors connection, collects message in buffer until message sent, responds, repeats."""
        global tcp_socket
        global tcp_conn
        global listen_thread_pid

        # Get PID
        listen_thread_pid = os.getpid()

        self.LogThis("Waiting for client connection...")
        tcp_conn, addr = tcp_socket.accept()        
        self.LogThis("Client address: " + "".join(str(addr)))
        while True:
            msg_buffer = ''
            while True:
                if not self.startserver_toggle.GetValue(): return
                wx.Yield()
                self.LogThis("Waiting for client message...")
                msg_buffer += tcp_conn.recv(BUFFER_SIZE)
                if msg_buffer.find(MSG_DELIM) >= 0:
                    self.LogThis("Client:\t " + msg_buffer)
                    # Send RECIEVE
                    self.LogThis("Server:\t " + "RECIEVED" + MSG_DELIM)
                    tcp_conn.sendall("RECIEVED" + MSG_DELIM)
                    # Send DONE to terminate message group
                    self.LogThis("Server:\t " + "DONE" + MSG_DELIM)
                    tcp_conn.sendall("DONE" + MSG_DELIM)
                    break
                time.sleep(.5)
                
            
    
    def LogThis(self, output_str):
        print output_str
        self.output_edit.AppendText("\n" + output_str)
        self.output_edit.ShowPosition(self.output_edit.GetLastPosition())
        self.output_edit.Refresh()


def main():
    app = wx.PySimpleApp()
    frame = TextFrame()
    frame.Show()
    app.MainLoop()


if __name__ == "__main__":
    main()


