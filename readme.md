# LAN device online check by MAC address
# Usage

```bash
$ python ./lan_arp_check.py

$ python ./zabbix_check_mac_online.py --check_mac "08:31:8b:43:3e:c0"
Up

$ python ./zabbix_get_ip_by_mac.py --check_mac "08:31:8b:43:3e:c0"
192.168.3.115

$ python ./zabbix_check_mac_online.py --check_mac "02:42:ac:10:ee:03"
Down

$ python ./zabbix_check_mac_delay.py --check_mac "3c:cd:57:3a:46:e9"
10.3
```

## zabbix

```bash
$ more /usr/local/etc/zabbix_agentd.conf.d/check_device_online_by_mac.conf
UserParameter=lan_mac_check[*],python /usr/local/etc/zabbix_scripts/zabbix_check_mac_online.py --log_json_file /usr/local/etc/zabbix_scripts/check_ip_mac_up.json --check_mac $1
UserParameter=lan_get_ip_by_mac[*],python /usr/local/etc/zabbix_scripts/zabbix_get_ip_by_mac.py --log_json_file /usr/local/etc/zabbix_scripts/check_ip_mac_up.json --check_mac $1
UserParameter=zabbix_check_mac_delay[*],python /usr/local/etc/zabbix_scripts/zabbix_check_mac_delay.py --log_json_file /usr/local/etc/zabbix_scripts/check_ip_mac_up.json --check_mac $1
UserParameter=fping.delay[*],fping -p 50 -c 10 $1 2>&1| tail -n 1 | awk '{print $NF}' | cut -d '/' -f2

$ sudo chmod 777 /usr/local/etc/zabbix_scripts/check_ip_mac_up.json
$ zabbix_get -s 192.168.3.9 -p 10050 -k "lan_mac_check[08:31:8b:43:3e:c0]"
Up
$ zabbix_get -s 192.168.3.9 -p 10050 -k "lan_get_ip_by_mac[08:31:8b:43:3e:c0]"
192.168.3.115
$ zabbix_get -s 192.168.3.9 -p 10050 -k "fping.delay[192.168.3.1]"
1.04
$ zabbix_get -s 192.168.3.9 -p 10050 -k "zabbix_check_mac_delay[3c:cd:57:3a:46:e9]"
8.74
```

# crontab deploy

```bash
# update every minutes
* * * * * cd /usr/local/etc/zabbix_scripts && python ./lan_arp_check.py
```