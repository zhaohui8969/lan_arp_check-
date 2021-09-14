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
