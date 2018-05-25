import os
import base64
import email
#from apiclient import errors
#from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import mailfile_unzip
import malurlcontents_down
from multiprocessing import Pool
import time
import math


# Setup the Gmail API
SCOPES = 'https://mail.google.com/'
store = file.Storage('credentials.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_id.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('gmail', 'v1', http=creds.authorize(Http()))


#Make Directory
def MakeDir():
    if os.path.isdir('addfile_downzip') == 0:
        make_zipPath = os.mkdir('addfile_downzip')

    if os.path.isdir('addfile_json') == 0:
        make_JsonPath = os.mkdir('addfile_json')

    if os.path.isdir('addfile_contents') == 0:
        make_ContentsPath = os.mkdir('addfile_contents')

    else:
        print('Directory Make Exist')



#Make Directory Settings
current_path = os.getcwd()
storePath = os.path.join(current_path, 'addfile_downzip\\')
jsonPath = os.path.join(current_path, 'addfile_json\\')
contentsPath = os.path.join(current_path, 'addfile_contents\\')


# User Settings
user_id = "me"


# Specific Label & Unread Message List Function
def ListMessagesWithLabels(service, user_id):
    response = service.users().messages().list(userId=user_id,q="label:malwares_com is:unread has:attachment").execute()
    messages = []
    if 'messages' in response:
        messages.extend(response['messages'])
    while 'nextPageToken' in response:
        page_token = response['nextPageToken']
        response = service.users().messages().list(userId=user_id,labelIds=label_ids,pageToken=page_token).execute()
        messages.extend(response['messages'])
    return messages



# Attachments Download
def GetAttachments(service, user_id, msg_id, storePath):
    message = service.users().messages().get(userId=user_id, id=msg_id).execute()
    for part in message['payload']['parts']:
        newvar = part['body']
        if 'attachmentId' in newvar:
            att_id = newvar['attachmentId']
            att = service.users().messages().attachments().get(userId=user_id, messageId=msg_id, id=att_id).execute()
            data = att['data']
            file_data = base64.urlsafe_b64decode(data.encode('UTF-8'))
            print(part['filename'])
            path = ''.join([storePath, part['filename']])
            f = open(path, 'wb')
            f.write(file_data)
            f.close()



def AttachDownload():
    mail_list_result = ""
    for i in range(0, len(mail_list)):
        mail_list_result = mail_list[i]['id']
        service.users().messages().modify(userId=user_id, id=mail_list_result,body={'removeLabelIds': ['UNREAD']}).execute()
        GetAttachments(service, user_id, mail_list_result, storePath)


   
if __name__ == "__main__":
    startTime = int(time.time())
    print(" ############### Make Directory ############### ")
    MakeDir()
    print(" ############### Gmail List Out ############### ")
    mail_list = ListMessagesWithLabels(service, user_id)
    print(" ############### Gmail Attachment File Download ############### ")
    AttachDownload()
    print(" ############### Gmail Attachment File Unzip ############### ")
    mailfile_unzip.unzip(storePath, jsonPath)
    print(" ############### Gmail Attachment File Delete ############### ")
    mailfile_unzip.del_zip_file(storePath)
    print(" ############### Malicious Contents File Download ############### ")
    malurlcontents_down.malurlContensDownloadExcute()
    endTime = int(time.time())
    print("Processing Start Time : ",(startTime),"Sec")
    print("Processing End Time : ",(endTime - startTime),"Sec")
    print("Processing Progress Time : ",(endTime - startTime),"Sec")

