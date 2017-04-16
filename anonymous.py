#!/usr/bin/env python

from config import *
import wx
import os
import socket
import sys


def create_menu_item(menu, label, func):
    item = wx.MenuItem(menu, -1, label)
    menu.Bind(wx.EVT_MENU, func, id=item.GetId())
    menu.AppendItem(item)
    return item


def on_left_down(event):
    print 'Tray icon was left-clicked.'
    print homeDirectory
    print anonDirectory
    print backupDirectory
    print cwd
    print socket.gethostname()


class TaskBarIcon(wx.TaskBarIcon):
    def __init__(self):
        super(TaskBarIcon, self).__init__()
        self.set_icon(trayIcon)
        self.Bind(wx.EVT_TASKBAR_LEFT_DOWN, on_left_down)

    def CreatePopupMenu(self):
        menu = wx.Menu()
        create_menu_item(menu, 'Start', self.on_start)
        create_menu_item(menu, 'Status', self.on_status)
        create_menu_item(menu, 'Stop', self.on_stop)
        menu.AppendSeparator()
        create_menu_item(menu, 'Exit', self.on_exit)
        return menu

    def set_icon(self, path):
        icon = wx.IconFromBitmap(wx.Bitmap(path))
        self.SetIcon(icon, trayTooltip)

    def on_start(self, event):
        print 'Start'

    def on_status(self, event):
        print 'Status'

    def on_stop(self, event):
        print 'Stop'

    def on_exit(self, event):
        wx.CallAfter(self.Destroy)
        sys.exit('User exited.')


def checkDirectories(dirName):
    if not os.path.exists(dirName):
        os.makedirs(dirName)


def checkFiles(fileName):
    if os.path.isfile(fileName) and os.access(fileName, os.R_OK):
        print ('File exists and is readable')
    else:
        if fileName == anonFile:
            dlgStart = wx.MessageBox('Script couldn\'t find configuration file!\n' +
                                     'Do you want to make a new one? ',
                                     'Anonymous',
                                     wx.YES_NO)

            if dlgStart == wx.NO:
                sys.exit('User cancel configuration.')

            # ###
            anon_hostname()
            anon_random_hostname()
            anon_nameserver()
            anon_spoof_interace()
            anon_tor_uid()
            anon_non_tor()
            anon_to_kill()
            anon_bleachbit_cleaners()
            return True

        elif fileName == torFile:
            print '1'
        elif fileName == torrcFile:
            print '1'
        elif fileName == logFile:
            print '1'
        else:
            print 'what???'


def main():
    app = wx.App()
    TaskBarIcon()

    checkDirectories(anonDirectory)
    checkDirectories(backupDirectory)

    checkFiles(anonFile)
    checkFiles(torFile)
    checkFiles(torrcFile)
    checkFiles(logFile)

    app.MainLoop()


if __name__ == '__main__':
    main()
