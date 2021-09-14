# encoding=utf-8
import argparse
import json
import re
import subprocess
from datetime import datetime
from typing import List, Dict

encoding='utf-8'

class ReportItem(object):
    def __init__(self):
        self.ip = None
        self.mac = None
        self.nic = None
        self.name = None
        self.state = None

    def to_dict(self):
        return {
            "ip": self.ip,
            "mac": self.mac,
            "nic": self.nic,
            "name": self.name,
            "state": self.state
        }

    def from_dict(self, a_dict):
        self.ip = a_dict['ip']
        self.mac = a_dict['mac']
        self.nic = a_dict['nic']
        self.name = a_dict['name']
        self.state = a_dict['state']


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cidr', default='192.168.3.0/24')
    # parser.add_argument('--cidr', default='172.22.195.0/24')
    parser.add_argument('--mac_friend_name_file', default='mac_friend_name_file.json')
    parser.add_argument('--log_json_file', default='check_ip_mac_up.json')
    return parser.parse_args()


def get_up_host_ip(cidr) -> List[ReportItem]:
    ip_regex = r"Host:\s+(\d+\.\d+\.\d+\.\d+)\s+\(.*\)\s+Status:\s+(.*)"
    nmap_result = subprocess.check_output(['nmap', '-sP', cidr, '-oG', '-']).decode(encoding)
    up_host_list = []
    matches = re.finditer(ip_regex, nmap_result, re.MULTILINE)
    for matchNum, match in enumerate(matches, start=1):
        groups = match.groups()
        host = groups[0]
        status = groups[1]
        if status == 'Up':
            item = ReportItem()
            item.state = "Up"
            item.ip = host
            up_host_list.append(item)
    return up_host_list


def get_mac_by_ip(report_list: List[ReportItem]) -> List[ReportItem]:
    ip_map = {i.ip: None for i in report_list}
    arp_result = subprocess.check_output(['arp', '-a']).decode(encoding)
    arp_regex = r"(.+) \((.*)\) at (.*) \[.*\] on (.*)"
    matches = re.finditer(arp_regex, arp_result, re.MULTILINE)
    for matchNum, match in enumerate(matches, start=1):
        groups = match.groups()
        host_name = groups[0]
        host_ip = groups[1]
        host_mac = groups[2]
        nic = groups[3]
        if host_ip in ip_map:
            ip_map[host_ip] = host_mac
    for i in report_list:
        if i.ip in ip_map:
            i.mac = ip_map.get(i.ip)
    return report_list


def pad_mac_friend_name(report_list: List[ReportItem], mac_friend_name_file: str) -> List[ReportItem]:
    with open(mac_friend_name_file, 'r', encoding=encoding) as fop:
        mac_friend_name_map: Dict[str, str] = json.loads(fop.read())
    not_online_mac_list = set(mac_friend_name_map.keys())
    for i in report_list:
        i.name = mac_friend_name_map.get(i.mac, None)
        if i.name:
            not_online_mac_list.remove(i.mac)
    for i in not_online_mac_list:
        item = ReportItem()
        item.mac = i
        item.name = mac_friend_name_map.get(i)
        item.state = "Down"
        report_list.append(item)
    return report_list


if __name__ == '__main__':
    args = get_args()
    timestamp = datetime.now().strftime("%y%m%d_%H%M%S")
    report_list = get_up_host_ip(args.cidr)
    report_list = get_mac_by_ip(report_list)
    report_list = pad_mac_friend_name(report_list, args.mac_friend_name_file)
    json_dumps = json.dumps({
        "report_list": [i.to_dict() for i in report_list],
        "timestamp": timestamp
    }, ensure_ascii=False, indent=4)
    print(json_dumps)
    with open(args.log_json_file, 'w', encoding=encoding) as fop:
        fop.write(json_dumps)
