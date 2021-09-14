# LAN device online check by MAC address
# Usage

```bash
# natas @ natas-pc in ~/usr/lan_arp_check [11:16:21] C:130
$ python ./lan_arp_check.py

# natas @ natas-pc in ~/usr/lan_arp_check [11:15:14]
$ python ./zabbix_check_mac_online.py --check_mac "08:31:8b:43:3e:c0"
Up

# natas @ natas-pc in ~/usr/lan_arp_check [11:15:20]
$ python ./zabbix_check_mac_online.py --check_mac "02:42:ac:10:ee:03"
Down
```

## zabbix

```bash
$ more /usr/local/etc/zabbix_agentd.conf.d/check_device_online_by_mac.conf
UserParameter=lan_mac_check[*],python /usr/local/etc/zabbix_scripts/zabbix_check_mac_online.py --log_json_file /usr/local/etc/zabbix_scripts/check_ip_mac_up.json --check_mac $1

$ sudo chmod 777 /usr/local/etc/zabbix_scripts/check_ip_mac_up.json
$ zabbix_get -s 192.168.3.9 -p 10050 -k "lan_mac_check[08:31:8b:43:3e:c0]"
Up
```

# crontab deploy

```bash
# update every minutes
* * * * * cd /usr/local/etc/zabbix_scripts && python ./lan_arp_check.py
```