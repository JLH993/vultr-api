# vultr-api
Using Python to interact with the Vultr API. Initially written by https://github.com/grassymeadow... Being modified to include more options and usage. 

# Examples:
./vultr-api.py <command> [args]

Commands:

firewall-list					list firewalls
firewall-rules <fwid>				list rules for firewall specified
firewall-ssh <fwid> <ipaddr>			add SSH rule for specified IP Addr
firewall-http <fwid> <ipaddr>			add HTTP rule for specified IP Addr
firewall-https <fwid> <ipaddr>			add HTTPS rule for specified IP Addr
firewall-add <fwid> <ip/cidr> <port/proto>	add manually specified rule
firewall-delete <fwid> <rulenumber>		delete firewall rule
server-list					print high level list of servers
server-info					print detailed list of server information
