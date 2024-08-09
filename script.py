from time import sleep
import requests

# Cloudflare API credentials
WAIT_TIME = 10 # Seconds
API_TOKEN = 'COPY_FROM_COUDFLARE'
ZONE_ID = 'COPY_FROM_COUDFLARE'

def cf_get(url: str, body={}):
    resp = requests.get(url, params=body, headers={
        'Authorization': f'Bearer {API_TOKEN}',
        'Content-Type': 'application/json'
    })
    ret = resp.json()
    if resp.status_code != 200:
        print(f'Response ({resp.status_code}): {ret["errors"][0]["code"]} - {ret["errors"][0]["message"]}')
        exit(0)
    return ret

def cf_put(url: str, body={}):
    resp = requests.put(url, json=body, headers={
        'Authorization': f'Bearer {API_TOKEN}',
        'Content-Type': 'application/json'
    })
    ret = resp.json()
    if resp.status_code != 200:
        print(f'Response ({resp.status_code}): {ret["errors"][0]["code"]} - {ret["errors"][0]["message"]}')
        print(body)
        exit(0)
    return ret
    
def get_dns_records(filter={}):
    return cf_get(f'https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records', filter)

def update_dns_record(rec_id, body):
    return cf_put(f'https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records/{rec_id}', body)

def update_with_ip(ip):
    for id, rec in records.items():
        rec['content'] = ip
        update_dns_record(id, rec)


records = {}
def init_automated_records():
    
    resp = get_dns_records({'comment.startswith': 'autoupdate'})['result']
    needs_update = False
    current_ip = get_public_ip()
    for rec in resp:
        del rec['created_on']
        del rec['modified_on']
        del rec['zone_id']
        del rec['zone_name']
        del rec['proxiable']
        del rec['meta']
        del rec['tags']
        records[rec['id']] = rec
        if rec['content'] != current_ip:
            needs_update = True
        print(f"{rec['id']}\t{rec['type']}\t{rec['name']}  \t{rec['content']}")
    if needs_update:
        print("Needs update on initial")
        update_with_ip(current_ip)


def get_public_ip():
    return requests.get('https://api64.ipify.org').text

public_ip = get_public_ip()
init_automated_records()
print(f"Started working ({public_ip})")
while True:
    new_ip = get_public_ip()
    if new_ip != public_ip:
        print("IP have been changed")
        public_ip = new_ip
        update_with_ip(public_ip)
    sleep(WAIT_TIME)