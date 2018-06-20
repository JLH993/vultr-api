#!/usr/bin/python

import requests
import sys
import json

## Global Variables
API_URL = "https://api.vultr.com/v1"
API_KEY = "NVFCFJTGJSEPZ3ZZFGHHZEC7WPEHZEGDCN4Q"

## Begin Functions
def GetFirewallGroups ():
	head = {"Content-type": "application/json", "API-Key": API_KEY}
	ret = requests.get(API_URL + "/firewall/group_list", headers=head)
	rjson = ret.json()
	for group in rjson.keys():
		print rjson[group]['FIREWALLGROUPID'] + "\t" + rjson[group]['description']

def GetFirewallRules (fwID):
	head = {"Content-type": "application/json", "API-Key": API_KEY}
	parameters = {'FIREWALLGROUPID': fwID, 'ip_type': 'v4', 'direction': 'in'}
	ret = requests.get(API_URL + "/firewall/rule_list",params=parameters, headers=head)
	rjson = ret.json()
	for group in rjson.keys():
		print str(rjson[group]['rulenumber']) + "\t" + rjson[group]['action'] + "\t" + rjson[group]['protocol'] + "\t" + rjson[group]['port'] + "\t" + rjson[group]['subnet'] + "/" + str(rjson[group]['subnet_size'])
	
def CreateFirewallRule (fwID, rData):
	head = {"API-Key": API_KEY}
	reqdata = {'FIREWALLGROUPID': fwID, 'ip_type': 'v4', 'direction': 'in', 'protocol': rData['protocol'], 'port': rData['port'], 'subnet': rData['subnet'], 'subnet_size': rData['subnet_size']}
	ret = requests.post(API_URL + "/firewall/rule_create", reqdata, headers=head)
	if ret.status_code == 200:
		print ret.json()['rulenumber']
	else:
		print "ERROR: " + ret.text + " (HTTP " + str(ret.status_code) + ")"

def deleteFWRule (fwID, ruleNumber):
	head = {"API-Key": API_KEY}
	reqdata = {'FIREWALLGROUPID': fwID, 'rulenumber': ruleNumber}
        ret = requests.post(API_URL + "/firewall/rule_delete", reqdata, headers=head)
        if ret.status_code == 200:
		print "Rule deleted successfully."
	else:
		print "ERROR: " + ret.text + " (HTTP " + str(ret.status_code) + ")"

def showServerList ():
	head = {"Content-type": "application/json", "API-Key": API_KEY}
	ret = requests.get(API_URL + "/server/list", headers=head)
	rjson = ret.json()
	print "Server List:" + "\n"
	for server in rjson.keys():
		print rjson[server]['label'] + "\t" + rjson[server]['os']

def showServerInfo ():
	head = {"Content-type": "application/json", "API-Key": API_KEY}
	ret = requests.get(API_URL + "/server/list", headers=head)
	rjson = ret.json()
	print "Server Information:" + "\n"
	for server in rjson.keys():
		print "Name:" + "\t\t" + rjson[server]['label'] + "\n" + "Tags:" + "\t\t" + rjson[server]['tag'] + "\n" + "Location:" + "\t" + rjson[server]['location'] + "\n" + "IP Address: " + "\t" + rjson[server]['main_ip'] + "\n" + "OS:" + "\t\t" + rjson[server]['os'] + "\n" + "CPU: " + "\t\t" + rjson[server]['vcpu_count'] + "\n" + "RAM: " + "\t\t" + rjson[server]['ram'] + "\n" + "Status:" + "\t\t" + rjson[server]['status'] + "\n" + "Power:" + "\t\t" + rjson[server]['power_status'] + "\n"

def showHelp():
	helptext = "Error: not enough arguments, see usage below...\n\n" + sys.argv[0] + " <command> [args]\n\nCommands:\n\nfirewall-list\t\t\t\t\tlist firewalls\nfirewall-rules <fwid>\t\t\t\tlist rules for firewall specified\nfirewall-ssh <fwid> <ipaddr>\t\t\tadd SSH rule for specified IP Addr\nfirewall-http <fwid> <ipaddr>\t\t\tadd HTTP rule for specified IP Addr\nfirewall-https <fwid> <ipaddr>\t\t\tadd HTTPS rule for specified IP Addr"
	print helptext
	print "firewall-add <fwid> <ip/cidr> <port/proto>\tadd manually specified rule"
	print "firewall-delete <fwid> <rulenumber>\t\tdelete firewall rule"
	print "server-list\t\t\t\t\tprint high level list of servers"
	print "server-info\t\t\t\t\tprint detailed list of server information" 
	print ""

## Help me
if len(sys.argv) < 2 or sys.argv[1] == "help":
	showHelp()
	quit()

## List all firewall groups.
if sys.argv[1] == "firewall-list":
	GetFirewallGroups()

## List all rules for specified groups.
if sys.argv[1] == "firewall-rules":
	GetFirewallRules(sys.argv[2])

## Add firewall rule for SSH connectivity to specified group.
if sys.argv[1] == "firewall-ssh":
	rData = {'protocol': 'tcp', 'port': '22', 'subnet': sys.argv[3], 'subnet_size': 32}
	CreateFirewallRule(sys.argv[2], rData)

## Add firewall rule for HTTP traffic to specified group.
if sys.argv[1] == "firewall-http":
	rData = {'protocol': 'tcp', 'port': '80', 'subnet': sys.argv[3], 'subnet_size': 32}
	CreateFirewallRule(sys.argv[2], rData)

## Add firewall rule for HTTPS traffic to specified group.
if sys.argv[1] == "firewall-https":
	rData = {'protocol': 'tcp', 'port': '443', 'subnet': sys.argv[3], 'subnet_size': 32}
	CreateFirewallRule(sys.argv[2], rData)

## Add manually specified firewall rule to group.
if sys.argv[1] == "firewall-add" and len(sys.argv) > 4:
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
	
## Delete firewall rule from specified group.
if sys.argv[1] == "firewall-delete":
	deleteFWRule(sys.argv[2], sys.argv[3])

## Show server list with OS information
if sys.argv[1] == "server-list":
        showServerList()

if sys.argv[1] == "server-info":
	showServerInfo()
