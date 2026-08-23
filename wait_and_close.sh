#!/bin/bash
while ps aux | grep -v grep | grep "loaddata local_backup.json" > /dev/null; do
    sleep 5
done
echo "loaddata finished! Closing public port..."
python3 -c '
import urllib.request
import json
URL = "http://64.227.167.223:8000/api/v1/databases/vzykz87urne7bosgh6f5nhr6"
TOKEN = "1|Us5OxMGJQtBNTiHbbhJMnOXshCQxXBEAMdWLHbn024ec9c7f"
data = json.dumps({"is_public": False}).encode("utf-8")
req = urllib.request.Request(URL, data=data, headers={"Authorization": f"Bearer {TOKEN}", "Accept": "application/json", "Content-Type": "application/json"}, method="PATCH")
try:
    response = urllib.request.urlopen(req)
    print(json.loads(response.read().decode()))
except Exception as e:
    print("Error:", e.read().decode() if hasattr(e, "read") else e)
'
