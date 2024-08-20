#gets all ignored vulnerabilities and adds them to a list
#also mass comments on all ignored vulnerabilities

import requests
import json
import csv

api_url = "https://us.api.insight.rapid7.com/ias/v1/"
api_key = "API KEY"

def get_all_ignored_vulnerabilities():
    ignored_vulnerabilities = []
    api_path = "search"
    full_url = api_url + api_path

    headers = {"X-Api-Key": api_key, "Content-Type": "application/json"}

    body = {
        "type": "VULNERABILITY",
        "query": "vulnerability.status = 'IGNORED'"
    }

    data = []
    cont = True

    while cont:
        response = requests.post(full_url, headers=headers, data=json.dumps(body))
        response_dict = response.json()
        data.extend(response_dict['data'])
        if len(data) >= response_dict.get("metadata").get("total_data"):
            cont = False
        else:
            for x in response_dict.get("links"):
                if x.get("rel") == "next":
                    full_url = x.get("href")
                    break

    for vuln in data:
        ignored_vulnerabilities.append({
            'ID': vuln['id'],
            'Severity': vuln['severity'],
            'Status': vuln['status'],
            'Root Cause URL': vuln['root_cause']['url'],
            'Link': 'https://us.appsec.insight.rapid7.com/op/6B621519A4C63B28E041/#/vulnerabilities?displayText=vulnerability.id%20%3D%20%22{0}%22&filterText=vulnerability.id%20%3D%20%27{0}%27&showVulnDetails=true'.format(vuln['id']),
        })
    return ignored_vulnerabilities

def convert_to_csv(vuln_list):
    #take the ignored_vulnerabilities list and export it to a csv file
    keys = vuln_list[0].keys()

    with open('ignored_vulnerabilities.csv', 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(vuln_list)

def add_comment_to_vulnerability(vuln_id, comment):
    api_path = "vulnerabilities/" + vuln_id + "/comments"
    full_url = api_url + api_path

    headers = {"X-Api-Key": api_key, "Content-Type": "application/json"}
    body = {
        "content": comment
    }

    response = requests.post(full_url, headers=headers, data=json.dumps(body))
    print(response)

def __main__():
    print("Please select an option:\n1) Download all false positives to a CSV\n2) Add a comment to each false positive stating it was reviewed")
    option = input()

    if option == "1":
        print("Downloading all false positives to a CSV...")
        convert_to_csv(get_all_ignored_vulnerabilities())
        print("Done")
    elif option == "2":
        print("Please enter the comment you would like to add to each false positive: ")
        comment = input()
        for vuln in get_all_ignored_vulnerabilities():
            print("Adding comment to vulnerability " + vuln['ID'])
            add_comment_to_vulnerability(vuln['ID'], comment)
        print("All comments added")

__main__()