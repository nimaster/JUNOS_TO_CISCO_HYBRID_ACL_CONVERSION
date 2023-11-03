# JUNOS_TO_CISCO_HYBRID_ACL_CONVERSION
Scripts to convert JUNOS inbound filters into Cisco IOS-XR hybrid ACLs

ipv4junos-to-hybridACL.py converts inbound IPv4 Junos filters in a into an Cisco IOS-XR ipv4 hybrid ACL.
Copy the inbound IPv4 Junos filter configuration into a text file called aclv4-inbound-original and then run the script.

ipv6junos-to-hybridACL.py converts inbound IPv6 Junos filters in a into an Cisco IOS-XR ipv6 hybrid ACL.
Copy the inbound IPv4 Junos filter configuration into a text file called aclv6-inbound-original and then run the script.

Both of the scripts create some files with the filter terms. These can be cleaned up after the conversion using the cleanup.py script

CAVEATS:
 - The scripts currently don't the JUNOS "except" keyword in filter terms
