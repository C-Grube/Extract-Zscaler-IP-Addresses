#!/usr/bin/env python3

'''
[X] Author: Chris Grube
[X] Description: Retrives the list of Zscaler CIDR ranges from https://api.config.zscaler.com/zscaler.net/cenr/json
    and extracts each individual IP address. 
'''

import requests
import ipaddress

# Returns a list of CIDR ranges from Zscaler's website
def get_cidr():
    raw_ip_data = requests.get('https://api.config.zscaler.com/zscaler.net/cenr/json', verify=False).json()
    continents = raw_ip_data['zscaler.net']
    cidr_list = []
    # Nested loops to extract the cidr ranges from the underlying dictionaries
    for k,v in continents.items():
        for k2,v2 in v.items():
            for entry in v2:
                if "::" not in entry['range']: # Removes IPV6 ranges
                    cidr_list.append(entry['range'])
    cidr_list = list(set(cidr_list)) # De-Dups
    return(cidr_list)


# Takes a list of CIDR ranges and extracts the individual ips from each range
def extract_ips(list_of_cidr_ranges):
    ip_list = []
    for cidr_range in list_of_cidr_ranges:
        for ip in ipaddress.IPv4Network(cidr_range):
            ip_list.append(str(ip))
    return(ip_list)


def main():
    cidr_list = get_cidr()
    ip_list  = extract_ips(cidr_list)
    print(ip_list)


if __name__ == "__main__":
    main()