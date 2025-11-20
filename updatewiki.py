import requests
import urllib3

# Disable SSL warnings (optional)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

token = morpheus['morpheus']['apiAccessToken']
url = "https://stage.morpheusdata.com/api/wiki/pages"

headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Authorization": "Bearer " + token
}

wiki_body = (
"**A) REQUEST DETAILS**\n"
"---------------\n\n"
"**REQUEST INFO**\n"
"| **KEY** | **VALUE** |\n"
"| ------- | --------- |\n"
"| **REQUESTOR:** | Ximena Rodriguez / <anaximena.rodriguez@abc.om> |\n"
"| **IDMD:** | POC |\n"
"| **BUSINESS SERVICE:** | ECS AUTOMATION SERVICE |\n"
"| **APPLICATION:** | MORPHEUS (PRD) |\n\n"
"**SERVER INFO**\n"
"| **KEY** | **VALUE** |\n"
"| ------- | --------- |\n"
"| **SERVER NAME:** | bss7b1.abc.com |\n"
"| **SERVER LOCATION:** | Americas/BR/Cotia |\n"
)

payload = {
    "page": {
        "name": "Weblogic IO/OQ",
        "category": "WebLogic",
        "format": "markdown",
        "body":  wiki_body
    }
}

response = requests.post(url, json=payload, headers=headers, verify=False)

print(response.status_code)
print(response.text)

