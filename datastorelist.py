from asyncio.windows_events import NULL
import requests
# define vars for API
host="10.32.23.97"
token="c77605e3-f303-4d64-911c-818b12f12b6b"
headers = {"Content-Type":"application/json","Accept":"application/json","Authorization": "BEARER " + (token)}
def listDatastores():
    url = "https://10.32.21.180/rest/vcenter/datastore"
    payload={}
    headers = {
  'Cookie': 'vmware-api-session-id=312cb11a403e9603e85b07222100c366'
    }
    response = requests.request("GET", url, headers=headers, data=payload,verify=False)
    data=response.json()
    print("Vcenter data stores details")
    #print("Datastoreid\t DatatstoreName\t Freespace\t Capacity")
  
    datastoredetails=data['value']  
    for i in range(0, len(datastoredetails)):
        print(datastoredetails[i]['datastore'] +"\t"+datastoredetails[i]['name'] +"\t"+str(datastoredetails[i]['free_space'])+"\t"+str(datastoredetails[i]['capacity']))
     #   print(data[i]['datastore'])


gid=2  # vmware clous id is 2 in  my lab
# Write a function to get the cloudId
def getCloudId(gid):
    apiUrl = 'https://%s/api/zones?groupId=%s'% (host, gid)
    url=str(apiUrl)
    r = requests.get(url, headers=headers, verify=False)
    data = r.json()
    cloudId = data['zones'][0]['id']
    return cloudId
# Get DatatoreID
#def getDatastoreId(cloudId,datastoreName):
 #   apiUrl = 'https://%s/api/zones/%s/data-stores?name=%s' % (host, cloudId, datastoreName)
 #   url=str(apiUrl)
  #  r = requests.get(url, headers=headers, verify=False)
 #   data = r.json()
    #print(data)
 #   dsid = data['datastores'][0]['id']
 #   return int(dsid)#

def getDatastores(cloudId):
    apiUrl = 'https://%s/api/zones/%s/data-stores'% (host,cloudId)
    url=str(apiUrl)
    r = requests.get(url, headers=headers, verify=False)
    data = r.json()
   #print("le2n="+str(len(data)))
    datastoredetails=data['datastores']
    print("Datastoreid\t DatatstoreName\t Freespace")
    for i in range(0, len(datastoredetails)):
        print(str(datastoredetails[i]['id']) +"\t"+ datastoredetails[i]['name'] +"\t"+ str(datastoredetails[i]['freeSpace']))
       
  

listDatastores()
getDatastores(2)