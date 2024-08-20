import smtplib
import datetime
from email.message import EmailMessage
from office365.runtime.auth.client_credential import ClientCredential
from office365.sharepoint.client_context import ClientContext
import os
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

#SharePoint global variables
site_url = "SHAREPOINT URL"
site_title = "SHAREPOINT TITLE"
client = ClientContext(site_url).with_credentials(ClientCredential(CLIENT_ID, CLIENT_SECRET))
target_list = client.web.lists.get_by_title(site_title)

#email global variables
server = smtplib.SMTP('SMTP SERVER')
email = '''Good {TIME_OF_DAY},

A scan is complete.  The scan report is attached to the request (ID #{ID}) on the "SHAREPOINT NAME" SharePoint.

https://SHAREPOINTSITENAME/WebAppSecScan/DispForm.aspx?ID={ID}

There were {HIGH} High and {MEDIUM} Medium vulnerabilities reported that must be remediated.

The next scan for this web application is scheduled on {DATE}.  Please let us know if that is an issue.

Best Regards,
SECURITY TEAM NAME
'''

#Functions
def get_time():
    current_time = datetime.datetime.now()
    if current_time.hour < 12:
        return 'morning'
    elif 12 <= current_time.hour < 18:
        return 'afternoon'
    else:
        return 'evening'

def get_user_email(id):
    users = client.web.site_users.get().execute_query()
    for user in users:
        if user.properties['Id'] == id:
            return user.properties['Email']

def get_user_input():
    print("Enter web scan ID:")
    scan_id = input()
    return scan_id
    
def send_email(target_list, id):
    print("How many emails are to be sent?")
    num = input()
    for i in range(1, int(num) + 1):
        id = get_user_input()

        item = target_list.items.get_by_id(id).get().execute_query()
        num_of_highs = item.properties['OData__x0023__x0020_of_x0020_Highs']
        num_of_mediums = item.properties['OData__x0023__x0020_of_x0020_Mediums']

        #this accounts for if there is more than one requestor
        requestors = []
        for value in item.properties['RequestorId'].values():
            requestors.append(get_user_email(value))
        requestors_to_string = ', '.join([str(requestor) for requestor in requestors])

        if item.properties['OData__x0023__x0020_of_x0020_Highs'] == None:
            num_of_highs = 0
        if item.properties['OData__x0023__x0020_of_x0020_Mediums'] == None:
            num_of_mediums = 0

        next_scan_date = item.properties['Scheduled_x0020_Next_x0020_Scan']
        #draft and send the email
        msg = EmailMessage()
        msg['Subject'] = 'Rescan Report for ID #{ID}'.format(ID=id)
        msg['From'] = 'SECURITY TEAM <SECURITYMAILBOX@SECURITY.COM'
        msg['To'] = requestors_to_string
        msg.set_content(email.format(TIME_OF_DAY=get_time(), ID=id, HIGH=num_of_highs, MEDIUM=num_of_mediums, DATE=next_scan_date))
        server.send_message(msg)

send_email(target_list, id)
