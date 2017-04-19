import os
from os.path import expanduser
import wx
import sys
import socket
import netifaces


cwd = os.getcwd()
homeDirectory = expanduser("~")
anonDirectory = homeDirectory + '/.anonpy'
backupDirectory = anonDirectory + '/Backup'

anonFile = anonDirectory + '/anonymous.conf'
logFile = anonDirectory + '/anonymous.log'
torFile = anonDirectory + '/tor'
torrcFile = anonDirectory + '/torrc'

trayTooltip = 'Anonymous'
trayIcon = cwd + '/icon.png'

anonConfig = '''#Anonymous configuration
#Default Hostname
HOSTNAME=

# Randomize Hostname on start
HOSTNAME_RANDOMIZE=

#Nameserver IP
NAMESERVER=

#Spoof MAC address
SPOOF_INTERFACE=

#Default Tour UID
TOR_UID=

#IP addresses excluded from tor network
NON_TOR=

#Kill selected applications before starting anonymous script
TO_KILL=

#What to clean after stopping anonymous script
BLEACHBIT_CLEANERS=

#Cleaning options
BLEACHBIT_DELETE=
'''

torConfig = ''' Tor config file
RUN_DAEMON=\"yes\"

CLEANUP_OLD_COREFILES=y

if [ -e /etc/default/tor.vidalia ] && [ -x /usr/bin/vidalia ]; then
. /etc/default/tor.vidalia
fi"""

torrcConfig = """# Torrc config file
#define virtual network mask
VirtualAddrNetwork 10.192.0.0/10
AutomapHostsOnResolve 1
AutomapHostsSuffixes .exit,.onion

#use tor to resolve domain names
DNSPort 53

#tor ports
TransPort 9040
SocksPort 9050

#daemonize
RunAsDaemon 1

#sandbox
Sandbox 1

#use hardware accaleration when possible for crypto
HardwareAccel 1

#socket safety hacks
TestSocks 1
AllowNonRFC953Hostnames 0
WarnPlaintextPorts 23,109,110,143,80

#dns safety hacks
ClientRejectInternalAddresses 1

#circuit hacks
NewCircuitPeriod 40
MaxCircuitDirtiness 600
MaxClientCircuitsPending 48
UseEntryGuards 1
UseEntryGuardsAsDirGuards 1
EnforceDistinctSubnets 1'''

anon_random_hostname_options = ['Yes', 'No', 'Ask me every time']
anon_spoof_options = (['All', 'Select device(s) manually', 'Ask me every time', 'Disable spoof (Not recomended)'])
kill_options = (['google-chrome', 'firefox', 'thunderbird', 'pidgin', 'xchat', 'Select more applications'])
anon_bleachbit_options = (['bash.history', 'system.cache', 'system.clipboard', 'system.custom',
                           'system.recent_documents', 'system.rotated_logs', 'system.tmp',
                           'system.trash', 'Select more cleaners'])

netIfaces = netifaces.interfaces()[:]
netIfaces.remove('lo')


def error_handler(a, b):
    if a.ShowModal() == wx.ID_CANCEL:
        sys.exit('User canceled configuration.')

    if b == 'text_entry':
        if not a.GetValue():
            sys.exit('Empty value.')
    elif b == 'multi_entry':
        if not a.GetSelections():
            sys.exit('Empty value.')
            # elif b == 'single_entry':
            #     if not a.GetSelection():
            #        sys.exit('Empty value.')


def anon_hostname():
    dlg = wx.TextEntryDialog(None,
                             'What is your default Hostname?',
                             'Anonymous [1/9]',
                             socket.gethostname())

    error_handler(dlg, 'text_entry')
    HOSTNAME = dlg.GetValue()

    print "Default Hostname: "+str(HOSTNAME)
    return HOSTNAME


def anon_random_hostname():
    dlg = wx.SingleChoiceDialog(None,
                                'Do you want to randomize your Hostname on start?\n' +
                                '(To increase security enable it.)',
                                'Anonymous [2/9]',
                                anon_random_hostname_options,
                                wx.CHOICEDLG_STYLE)

    error_handler(dlg, 'single_entry')
    RANDOM_HOSTNAME = dlg.GetStringSelection().partition(' ')[0]

    print "Randomize Hostname: " + str(RANDOM_HOSTNAME)
    return RANDOM_HOSTNAME


def anon_nameserver():
    dlg = wx.TextEntryDialog(None,
                             'Nameserver IP:\n' +
                             '(Leave Localhost IP by default.)',
                             'Anonymous [3/9]',
                             '127.0.0.1')

    error_handler(dlg, 'text_entry')
    NAMESERVER = dlg.GetValue()
    print "Nameserver IP: " + str(NAMESERVER)
    return NAMESERVER


def anon_spoof_interace():
    dlg = wx.SingleChoiceDialog(None,
                                'Choose which device MAC address do you want to Spoof?\n' +
                                '(To increase security enable spoofing on your main network interface.)',
                                'Anonymous [4/9]',
                                anon_spoof_options,
                                wx.CHOICEDLG_STYLE)

    error_handler(dlg, 'single_entry')

    if dlg.GetStringSelection() == anon_spoof_options[0]:
        SPOOF_INTERFACES = "all"
    elif dlg.GetStringSelection() == anon_spoof_options[1]:
        dlg = wx.MultiChoiceDialog(None, 'Select network interfaces to spoof', 'Anonymous [4/9]', netIfaces)

        error_handler(dlg, 'multi_entry')

        SPOOF_INTERFACES = ' '.join([netIfaces[x] for x in dlg.GetSelections()])

    elif dlg.GetStringSelection() == anon_spoof_options[2]:
        SPOOF_INTERFACES = "ask"
    else:
        SPOOF_INTERFACES = "disabled"

    print "Spoof interface(s): " + str(SPOOF_INTERFACES)
    return SPOOF_INTERFACES


def anon_tor_uid():
    dlg = wx.TextEntryDialog(None, 'What is your Tor UID?\n' +
                             '(On Debian/Ubuntu distros it\'s: debian-tor)',
                             'Anonymous [5/9]',
                             'debian-tor')

    error_handler(dlg, 'text_entry')
    TOR_UID = dlg.GetValue()

    print "Tor UID: " + str(TOR_UID)
    return TOR_UID


def anon_non_tor():
    dlg = wx.TextEntryDialog(None,
                             'Select IP address(es) to exclude from Tor network.\n' +
                             '(This should be your local network IP range.)\n' +
                             'Allowed formats:\n\n' +
                             'IPv4  -  192.168.1.1\n' +
                             'IPv4 CIDR  -  192.168.1.0/24\n' +
                             'IPv6  -  2001:0db8:7654:3210:fedc:ba98:7654:3210\n' +
                             'IPv6 CIDR  -  2001:d78:7654:3210::\n\n' +
                             'Separate networks with spaces!',
                             'Anonymous [6/9]',
                             '192.168.1.0/24')

    error_handler(dlg, 'text_entry')
    NON_TOR = dlg.GetValue()

    print "Non Tor IP Address(es): " + str(NON_TOR)
    return NON_TOR


def anon_to_kill():
    dlg = wx.MultiChoiceDialog(None,
                               'To prevent DNS leaks, script needs to kill all active internet applications.\n' +
                               'Please select applications you wish to kill before script runs.',
                               'Anonymous [7/9]',
                               kill_options)

    error_handler(dlg, 'multi_entry')

    TO_KILL = ' '.join([kill_options[x] for x in dlg.GetSelections()])

    if 'Select more applications' in TO_KILL:
        dlg = wx.TextEntryDialog(None,
                                 'Enter more applications that you wish to kill.\n' +
                                 'Separate applications with spaces!\n\n' +
                                 'Example: app1 app2 app3',
                                 'Anonymous [7/9]')

        error_handler(dlg, 'text_entry')

        TO_KILL_2 = (TO_KILL + str(dlg.GetValue())).replace('Select more applications', '')

        print "To kill: " + str(TO_KILL_2)
        return TO_KILL_2
    else:
        print "To kill: " + str(TO_KILL)
        return TO_KILL


def anon_bleachbit_cleaners():
    dlg = wx.MultiChoiceDialog(None,
                               'What do you want to clean after script stops?\n',
                               'Anonymous [8/9]',
                               anon_bleachbit_options)

    error_handler(dlg, 'multi_entry')

    BLEACHBIT_CLEANERS = ' '.join([anon_bleachbit_options[x] for x in dlg.GetSelections()])

    if 'Select more cleaners' in BLEACHBIT_CLEANERS:
        dlg = wx.TextEntryDialog(None,
                                 'Enter more cleaners.\n' +
                                 'Separate cleaners with spaces!\n\n' +
                                 'Example: option1, option2, option3',
                                 'Anonymous [8/9]')

        error_handler(dlg, 'text_entry')

        TOTAL_CLEANERS = (BLEACHBIT_CLEANERS + str(dlg.GetValue())).replace('Select more cleaners', '')
        print "To clean: " + str(TOTAL_CLEANERS)
        return TOTAL_CLEANERS
    else:
        print "To clean: " + str(BLEACHBIT_CLEANERS)
        return BLEACHBIT_CLEANERS
