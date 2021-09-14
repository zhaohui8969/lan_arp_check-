# encoding=utf-8
import argparse
import json

encoding = 'utf-8'


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--log_json_file', default='check_ip_mac_up.json')
    parser.add_argument('--check_mac', default='None')
    return parser.parse_args()


state_map = {
    "Up": 1,
    "Down": 0,
}

if __name__ == '__main__':
    args = get_args()
    check_mac = args.check_mac
    with open(args.log_json_file, encoding=encoding) as fop:
        logs = json.loads(fop.read())
        timestamp = logs['timestamp']
        report_list = logs['report_list']
        state = 0
        for i in report_list:
            if i['mac'] == check_mac:
                state = state_map.get(i['state'], 0)
                break
        print(state)
