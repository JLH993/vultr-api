#!/usr/bin/python
# A python port of vapi, a program that interacts with the Vultr API. https://github.com/JLH993/vapi
# For usage, see help funtion below, or run vapi with the help option.
# Maintained by https://github.com/JLH993/

import sys
import json
import requests

# Global Variables
API_URL = "https://api.vultr.com/v1"
API_KEY = "<apikeyhere>"

# Begin Functions...

###################
# Firewall Rules: #
###################
def GetFirewallGroups ():
    head = {"Content-type": "application/json", "API-Key": API_KEY}
    ret = requests.get(API_URL + "/firewall/group_list", headers=head)
    rjson = ret.json()
    for group in rjson.keys():
        print(rjson[group]['FIREWALLGROUPID'] + "\t" + rjson[group]['description'])


def CreateFirewallGroup (groupDesc):
    head = {"API-Key": API_KEY}
    reqdata = {'description': groupDesc}
    ret = requests.post(API_URL + "/firewall/group_create", reqdata, headers=head)
    if ret.status_code == 200:
        print(ret.json()['FIREWALLGROUPID'])
    else:
        print("ERROR: " + ret.text + " (HTTP " + str(ret.status_code) + ")")


def DeleteFirewallGroup (fwGID):
    head = {"API-Key": API_KEY}
    reqdata = {'FIREWALLGROUPID': fwGID}
    ret = requests.post(API_URL + "/firewall/group_delete", reqdata, headers=head)
    if ret.status_code == 200:
        print("Firewall Group succeessfully deleted.")
    else:
        print("ERROR: " + ret.text + " (HTTP " + str(ret.status_code) + ")")


def GetFirewallRules (fwID):
    head = {"Content-type": "application/json", "API-Key": API_KEY}
    parameters = {'FIREWALLGROUPID': fwID, 'ip_type': 'v4', 'direction': 'in'}
    ret = requests.get(API_URL + "/firewall/rule_list",params=parameters, headers=head)
    rjson = ret.json()
    for group in rjson.keys():
        print(str(rjson[group]['rulenumber']) + "\t" + rjson[group]['action'] + "\t" + rjson[group]['protocol'] + "\t" + rjson[group]['port'] + "\t" + rjson[group]['subnet'] + "/" + str(rjson[group]['subnet_size']))


def CreateFirewallRule(fwID, rData):
    head = {"API-Key": API_KEY}
    reqdata = {'FIREWALLGROUPID': fwID, 'ip_type': 'v4', 'direction': 'in', 'protocol': rData['protocol'],
               'port': rData['port'], 'subnet': rData['subnet'], 'subnet_size': rData['subnet_size']}
    ret = requests.post(API_URL + "/firewall/rule_create", reqdata, headers=head)
    if ret.status_code == 200:
        print(ret.json()['rulenumber'])
    else:
        print("ERROR: " + ret.text + " (HTTP " + str(ret.status_code) + ")")


def DeleteFirewallRule(fwID, ruleNumber):
    head = {"API-Key": API_KEY}
    reqdata = {'FIREWALLGROUPID': fwID, 'rulenumber': ruleNumber}
    ret = requests.post(API_URL + "/firewall/rule_delete", reqdata, headers=head)
    if ret.status_code == 200:
        print("Rule deleted successfully.")
    else:
        print("ERROR: " + ret.text + " (HTTP " + str(ret.status_code) + ")")


###################
# Server Actions: #
###################
def ShowServerList ():
    head = {"Content-type": "application/json", "API-Key": API_KEY}
    ret = requests.get(API_URL + "/server/list", headers=head)
    rjson = ret.json()
    print("Server List:" + "\n")
    for server in rjson.keys():
        print(rjson[server]['label'] + "\t" + rjson[server]['os'])


def ShowServerInfo ():
    head = {"Content-type": "application/json", "API-Key": API_KEY}
    ret = requests.get(API_URL + "/server/list", headers=head)
    rjson = ret.json()
    print("Server Information:" + "\n")
    for server in rjson.keys():
        print("Name:" + "\t\t" + rjson[server]['label'] + "\n" + "Tags:" + "\t\t" + rjson[server]['tag'] + "\n" + "Location:" + "\t" + rjson[server]['location'] + "\n" + "IP Address: " + "\t" + rjson[server]['main_ip'] + "\n" + "OS:" + "\t\t" + rjson[server]['os'] + "\n" + "CPU: " + "\t\t" + rjson[server]['vcpu_count'] + "\n" + "RAM: " + "\t\t" + rjson[server]['ram'] + "\n" + "Status:" + "\t\t" + rjson[server]['status'] + "\n" + "Power:" + "\t\t" + rjson[server]['power_status'] + "\n")

###################
# Help options:   #
###################
def ShowHelp():
    helptext = "Error: not enough arguments, see usage below...\n\n" + sys.argv[
            0] + " <command> [args]\n\nCommands:\n\nfirewall-group-list\t\t\t\t\tlist firewall groups.\nfirewall-rules-list <fwgid>\t\t\t\tlist rules for firewall group specified\nfirewall-add-ssh <fwgid> <ipaddr>\t\t\tadd SSH rule for specified IP address\nfirewall-add-http <fwgid> <ipaddr>\t\t\tadd HTTP rule for specified IP address\nfirewall-add-https <fwgid> <ipaddr>\t\t\tadd HTTPS rule for specified IP address"
    print(helptext)
    print("firewall-group-list\t\t\t\t\t\tlist firewall groups")
    print("firewall-group-create <fwgid>\t\t\tcreate firewall group")
    print("firewall-group-delete <fwgid>\t\t\tdelete firewall group")
    print("firewall-rules-list <fwgid>\t\t\tlist firewall rules for specified group")
    print("firewall-rule-add <fwgid> <ip/cidr> <port/proto>\tadd manually specified firewall rule")
    print("firewall-rule-delete <fwgid> <rulenumber>\t\tdelete firewall rule")
    print("server-list\t\t\t\t\tprint high level list of servers")
    print("server-info\t\t\t\t\tprint detailed list of server information")


# Begin doing the thing...

# Help me... Or tell me what I am doing wrong.
if len(sys.argv) < 2 or sys.argv[1] == "help":
    ShowHelp()
    quit()

# Firewall groups: list/create/destroy
if sys.argv[1] == "firewall-group-list":
    GetFirewallGroups()

if sys.argv[1] == "firewall-group-create":
    CreateFirewallGroup(sys.argv[2])

if sys.argv[1] == "firewall-group-delete":
    DeleteFirewallGroup(sys.argv[2])

# Firewall rules: list/create/destroy/https/ssh
if sys.argv[1] == "firewall-rules-list":
    GetFirewallRules(sys.argv[2])

if sys.argv[1] == "firewall-rule-create" and len(sys.argv) > 4:
    ip = sys.argv[3].split('/')[0]
    cidr = sys.argv[3].split('/')[1]
    if sys.argv[4].find('/') != -1:
        port = sys.argv[4].split('/')[0]
        proto = sys.argv[4].split('/')[1]
    else:
        port = '0'
        proto = sys.argv[4]
    if proto != "tcp" and proto != "udp" and proto != "icmp":
        quit("Error: Valid protocol not specified. Example of valid protocol: tcp/udp/icmp")
    if int(cidr) > 32 or int(cidr) < 0:
        quit("Error: Invalid CIDR specified.")
    rData = {'protocol': proto, 'port': port, 'subnet': ip, 'subnet_size': cidr}
    CreateFirewallRule(sys.argv[2], rData)

if sys.argv[1] == "firewall-rule-delete":
    DeleteFirewallRule(sys.argv[2], sys.argv[3])

if sys.argv[1] == "firewall-add-https":
    rData = {'protocol': 'tcp', 'port': '443', 'subnet': sys.argv[3], 'subnet_size': 32}
    CreateFirewallRule(sys.argv[2], rData)

if sys.argv[1] == "firewall-add-http":
    rData = {'protocol': 'tcp', 'port': '80', 'subnet': sys.argv[3], 'subnet_size': 32}
    CreateFirewallRule(sys.argv[2], rData)

if sys.argv[1] == "firewall-add-ssh":
    rData = {'protocol': 'tcp', 'port': '22', 'subnet': sys.argv[3], 'subnet_size': 32}
    CreateFirewallRule(sys.argv[2], rData)

# Server Information: list/info [to be cont]
if sys.argv[1] == "server-list":
    ShowServerList()

if sys.argv[1] == "server-info":
    ShowServerInfo()
