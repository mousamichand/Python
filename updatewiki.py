import requests

def upload_report_to_morpheus(report_file):
    """
    Uploads the generated Weblogic IQ/OQ report as a wiki page in Morpheus under the WebLogic section.
    """
    url = "https://stage.morpheusdata.com//api/wiki/pages"
    headers = {
        "accept": "application/json",
        "content-type": "application/json"
       "authorization": "Bearer "+
    }
    with open(report_file, "r") as rf:
        wiki_body = rf.read()
    payload = {
        "page": {
            "name": "Weblogic IO/OQ",
            "category": "WebLogic",
            "body": wiki_body
        }
    }

    response = requests.post(url, json=payload, headers=headers)
    print(response.text)
