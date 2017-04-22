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
anon_spoof_options = ['Yes', 'No', 'Ask me every time']
kill_options = (['google-chrome', 'firefox', 'thunderbird', 'pidgin', 'xchat', 'Select more...'])
anon_bleachbit_options = (['bash.history', 'system.cache', 'system.clipboard', 'system.custom',
                           'system.recent_documents', 'system.rotated_logs', 'system.tmp',
                           'system.trash', 'Select more...'])

netIfaces = netifaces.interfaces()[:]
netIfaces.remove('lo')


def error_handler(message, typ):
    if message.ShowModal() == wx.ID_CANCEL:
        sys.exit('User canceled configuration.')

    if typ == 'text':
        if (message.GetValue()).strip():
            return (message.GetValue()).strip()
    elif typ == 'multi':
        if message.GetSelections():
            return message.GetSelections()
    elif typ == 'single':
        return message.GetStringSelection().partition(' ')[0]

    sys.exit('Empty value.')


def anon_hostname():
    Msg = wx.TextEntryDialog(None,
                             'What is your default Hostname?',
                             'Anonymous [1/9]',
                             socket.gethostname())

    HOSTNAME = error_handler(Msg, 'text')
    print "[1] Default Hostname: " + str(HOSTNAME)
    return HOSTNAME


def anon_random_hostname():
    Msg = wx.SingleChoiceDialog(None,
                                'Do you want to randomize your Hostname on start?',
                                'Anonymous [2/9]',
                                anon_random_hostname_options,
                                wx.CHOICEDLG_STYLE)

    RANDOM_HOSTNAME = error_handler(Msg, 'single')
    print "[2] Randomize Hostname: " + str(RANDOM_HOSTNAME)
    return RANDOM_HOSTNAME


def anon_nameserver():
    Msg = wx.TextEntryDialog(None,
                             'Nameserver IP:\n' +
                             '(Leave Localhost IP by default.)',
                             'Anonymous [3/9]',
                             '127.0.0.1')

    NAMESERVER = error_handler(Msg, 'text')
    print "[3] Nameserver IP: " + str(NAMESERVER)
    return NAMESERVER


def anon_spoof_interace():
    Msg = wx.SingleChoiceDialog(None,
                                'Do you want to Spoof MAC address?',
                                'Anonymous [4/9]',
                                anon_spoof_options,
                                wx.CHOICEDLG_STYLE)

    SPOOF_OPTION = error_handler(Msg, 'single')
    print "[4] Spoof: " + str(SPOOF_OPTION)

    if str(SPOOF_OPTION) == 'Yes':
        Msg = wx.MultiChoiceDialog(None,
                                   'Select which interface(s) to Spoof:',
                                   'Anonymous [4/9]',
                                   netIfaces)

        SPOOF_INTERFACES = error_handler(Msg, 'multi')

        opt = ' '.join([netIfaces[x] for x in Msg.GetSelections()])

        print "[4.1] Spoof interface(s): " + str(SPOOF_INTERFACES)
        return SPOOF_INTERFACES


def anon_tor_uid():
    Msg = wx.TextEntryDialog(None, 'What is your Tor UID?\n' +
                             '(On Debian/Ubuntu distros it\'s: debian-tor)',
                             'Anonymous [5/9]',
                             'debian-tor')

    TOR_UID = error_handler(Msg, 'text')
    print "[5] Tor UID: " + str(TOR_UID)
    return TOR_UID


def anon_non_tor():
    Msg = wx.TextEntryDialog(None,
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

    NON_TOR = error_handler(Msg, 'text')
    print "[6] Non Tor IP Address(es): " + str(NON_TOR)
    return NON_TOR


def anon_to_kill():
    Msg = wx.MultiChoiceDialog(None,
                               'To prevent DNS leaks, script needs to kill all active internet applications.\n' +
                               'Please select applications you wish to kill before script runs.',
                               'Anonymous [7/9]',
                               kill_options)

    TO_KILL1 = error_handler(Msg, 'multi')
    print TO_KILL1
    if "Select more..." in str(TO_KILL1):
        print "petlja"
        Msg = wx.TextEntryDialog(None,
                                 'Enter more applications that you wish to kill.\n' +
                                 'Separate applications with spaces!\n\n' +
                                 'Example: app1 app2 app3',
                                 'Anonymous [7/9]')

        error_handler(Msg, 'text')

        TO_KILL2 = (TO_KILL1 + str(Msg.GetValue())).replace('Select more...', '')

        print "To kill: " + str(TO_KILL2)
        return TO_KILL2
    else:
        print "To kill: " + str(TO_KILL1)
        return TO_KILL1


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
