import argparse
import requests
import json
import urllib3
urllib3.disable_warnings()

# 定义四个URL和对应的API_TOKEN
URLS_API_TOKENS = {
    "https://172.18.14.7/api/FilterV2API": "TyppcjrQiVqba085mCIMnT2HptK9CSKGxzfbKqpI",
    "https://172.20.14.13/api/FilterV2API": "jQJqHc2thVusI6QGg74Qt2nD1jItNbC4tlTQR2Bh",
    "https://172.20.14.7/api/FilterV2API": "bCWP2vJU5fGNtMm1IEemQtt3YLIRszbNoNYcRjW8",
    "https://172.18.14.8/api/FilterV2API": "ckohORVNNJAEewFLuGRo92A5kTSbgmMauICWvPuT",
}


def get_ip_id(ip):
    ids = []
    for url, api_token in URLS_API_TOKENS.items():
        headers = {"API-TOKEN": api_token, "Content-type": "application/json"}
        get_id_url_auto = f"{url}?count=10&offset=0&target__iexact={ip}&scope=detect%3Arule_template%3Arule%3Aauto"
        try:
            rsp_auto = requests.get(url=get_id_url_auto, headers=headers, verify=False).json()
            if rsp_auto.get('data') and rsp_auto['data']['total'] != 0:
                ids.append(rsp_auto['data']['items'][0]['id'])
        except Exception as e:
            print(f"Error retrieving data from {url}: {str(e)}")
    return ids


def delete_ip(ip):
    count = 0
    id = []
    ids = get_ip_id(ip)
    if not ids:
        print(f"No matching records found for IP: {ip}")
        return
    for url, api_token in URLS_API_TOKENS.items():
        id.append(str(ids[count]))
        headers = {"API-TOKEN": api_token, "Content-type": "application/json"}
        data = {"id__in": list(map(str,id)), "scope": "detect:rule_template:rule:auto"}
        id.clear()
        try:
            rsp = requests.delete(url=url, headers=headers, data=json.dumps(data), verify=False)
            print(f"Deleting banned IP {ip} from {url}: {rsp.json()}")
        except Exception as e:
            print(f"Error sending delete request to {url}: {str(e)}")
        count = count + 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Delete banned IP")
    parser.add_argument("ip", type=str, help="IP address to be deleted from ban list")
    args = parser.parse_args()

    delete_ip(args.ip)