#!/usr/bin/env python

from config import *
import wx
import os
import sys


def on_start(event):
    print 'Start'

    checkDirectories(anonDirectory)
    checkDirectories(backupDirectory)

    checkFiles(anonFile)
    checkFiles(torFile)
    checkFiles(torrcFile)
    checkFiles(logFile)

    return event


def on_stop(event):
    print 'Stop'
    return event


def on_status(event):
    print 'Status'
    return event


def on_exit(self):
    dlgExit = wx.MessageBox('Do you want to stop Anonymous mode?',
                            'Anonymous',
                            wx.YES_NO)

    if dlgExit == wx.YES:
        on_stop('Exiting')

    wx.CallAfter(self.Destroy)
    sys.exit('User exited.')


def create_menu_item(menu, label, func):
    item = wx.MenuItem(menu, -1, label)
    menu.Bind(wx.EVT_MENU, func, id=item.GetId())
    menu.AppendItem(item)
    return item


def on_left_down(event):
    print 'Tray icon was left-clicked.'
    on_start(event)
    return event


class TaskBarIcon(wx.TaskBarIcon):
    def __init__(self):
        super(TaskBarIcon, self).__init__()
        self.set_icon(trayIcon)
        self.Bind(wx.EVT_TASKBAR_LEFT_DOWN, on_left_down)

    def CreatePopupMenu(self):
        print 'Tray icon was right-clicked.'
        menu = wx.Menu()
        create_menu_item(menu, 'Start', on_start)
        create_menu_item(menu, 'Status', on_status)
        create_menu_item(menu, 'Stop', on_stop)
        menu.AppendSeparator()
        create_menu_item(menu, 'Exit', on_exit)
        return menu

    def set_icon(self, path):
        icon = wx.IconFromBitmap(wx.Bitmap(path))
        self.SetIcon(icon, trayTooltip)


def checkDirectories(dir_name):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)


def checkFiles(file_name):
    if os.path.isfile(file_name) and os.access(file_name, os.R_OK):
        print ('File exists and is readable')
    else:
        if file_name == anonFile:
            dlgStart = wx.MessageBox('Script couldn\'t find configuration file!\n' +
                                     'Do you want to make a new one? ',
                                     'Anonymous',
                                     wx.YES_NO)

            if dlgStart == wx.NO:
                sys.exit('User cancel configuration.')

            anon_hostname()
            anon_random_hostname()
            anon_nameserver()
            anon_spoof_interace()
            anon_tor_uid()
            anon_non_tor()
            anon_to_kill()
            anon_bleachbit_cleaners()
            return True

        elif file_name == torFile:
            print '1'
        elif file_name == torrcFile:
            print '1'
        elif file_name == logFile:
            print '1'
        else:
            print 'what???'


def main():
    app = wx.App()
    TaskBarIcon()

    app.MainLoop()


if __name__ == '__main__':
    main()
