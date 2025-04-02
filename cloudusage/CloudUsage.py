import requests # type: ignorec
import smtplib
from email.mime.text import MIMEText
from prettytable import PrettyTable # type: ignore
import urllib3 # type: ignore
from urllib.parse import urlparse
from pyVim.connect import SmartConnect, Disconnect # type: ignore
from pyVmomi import vim # type: ignore
import ssl
from morpheuscypher import Cypher

c = Cypher(morpheus=morpheus)

vcenteruser=str(c.get("secret/vcenteruser"))
print(vcenteruser)
vcenterpassword=str(c.get("secret/vcenterpassword"))
print(vcenterpassword)
vcenterhost=str(c.get("secret/vcenterhost"))
print(vcenterhost)
#define vars for API

morphhost=morpheus['morpheus']['applianceHost']
token=morpheus['morpheus']['apiAccessToken']




# Disable SSL certificate verification for self-signed certificates
context = ssl._create_unverified_context()

# Connect to vCenter or ESXi server
si = SmartConnect(host=vcenterhost, user=vcenteruser, pwd=vcenterpassword, sslContext=context)

# Retrieve content from the vCenter or ESXi server
content = si.RetrieveContent()

# Retrieve all hosts in the environment
host_view = content.viewManager.CreateContainerView(content.rootFolder, [vim.HostSystem], True)




urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) 



mainheaders = {"Content-Type":"application/json","Accept":"application/json","Authorization": "BEARER " + (token)}

CloudTable =PrettyTable(["Cloud ID","Cloud Name"]) # List of all vmware cloud exist in Morpheus.
CloudStatsTable = PrettyTable(["Cloud Id", "Cloud Name", "Allocated Memory","Used Memory","Allocated Storage","UsedStorage","Allocated Cpu","Used Cpu"]) # Cloud Level stats.
Hosttable = PrettyTable(["Host ID", "Host NAME", "Allocated Memory","UsedMemory","Allocated Storage","UsedStorage","Allocated CPU ghz","Used Cpu Ghz"]) #Host Level stats   

Gbvar=1024*1024*1024  # var to convert bytes to GB.
Tbvar=1024*1024*1024*1024 # var to convert bytes to TB.


def emailConfig(emailBody):
# Email configuration
    smtp_server = "smtp.postmarkapp.com"
    smtp_port = 2525
    smtp_username = "xxxxxxxxx"
    smtp_password = "xxxxxxb"
    sender_email = "info@morpheus.com"
    recipient_email = "cloudteam@morpheusdata.com"
    msg = MIMEText(emailBody, 'html')
    msg['Subject'] = "Cloud  Status Notification"
    msg['From'] = sender_email
    msg['To'] = recipient_email
       # Establish a secure session with the SMTP server
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, [recipient_email], msg.as_string())

def getCloudUrl(morphhost): # retrive all vmware cloud  from morpheus .
    apiUrl = 'https://%s/api/zones/?type=vmware'%(morphhost)
    url=str(apiUrl)
    r = requests.get(url, headers=mainheaders, verify=False)
    if(int(r.status_code)==200):
        data = r.json()
        return data


def getHostList(): #  retrive  host level stats for all  the hosts exist in a cloud.
    emailText="Hi Team <br> Here is your current Cloud Status : <br>"
    CloudList= getCloudUrl(morphhost)
    CloudList=CloudList['zones']
    
    
    for j in range(0,len(CloudList)):  
        
        clusterTotalUsedMem=0
        clusterTotalUsedStorage=0
        clusterTotalAllocatedMem=0
        clusterTotalAllocatedStorage=0
        clusterTotalCpuUsage=0
        total_cpu_capacity_ghz=0
        total_cpu_usage_ghz=0
        
        
        clusterTotalFreeMem=0
        clusterTotalFreeStorage=0
        clusterTotalFreeCpu=0
        rowData=str(CloudList[j]['id'])+","+str(CloudList[j]['name'])
        serverUrl = "https://%s/api/servers?zoneId=%s&serverType=vmwareHypervisor"%(morphhost,CloudList[j]['id'])  # api call to retrieve host data from morpheus .
        url=str(serverUrl)
        response = requests.get(url, headers=mainheaders, verify=False)
        hostStats = response.json()
             
            
        if(int(response.status_code)==200):
            for ind2 in range(0,len(hostStats['servers'])): 
                maxMemory=round(hostStats['servers'][ind2]['stats']['maxMemory']/Gbvar,2) #maxmemory is same as   allocated memory in vcenter.It  is in bytes so converted  to GB.
                usedMemory=round(hostStats['servers'][ind2]['stats']['usedMemory']/Gbvar,2) #consumed memory .converted to GB.
                maxStorage=round(hostStats['servers'][ind2]['stats']['maxStorage']/Tbvar,2) #maxstorage is same as  allocated storage in vcenter .It is  is in bytes so converted  to TB.
                usedStorage=round(hostStats['servers'][ind2]['stats']['usedStorage']/Tbvar,2) #consumed storage .converted to TB.
                
                clusterTotalAllocatedMem += maxMemory 
                clusterTotalAllocatedStorage+=maxStorage
                clusterTotalUsedMem += usedMemory
                clusterTotalUsedStorage +=usedStorage
                


                for host in host_view.view:
                          

                 if(hostStats['servers'][ind2]['name']==host.name):
                 # CPU Usage
                    num_logical_cpus = host.hardware.cpuInfo.numCpuThreads #logical cpu.
                    #print("logical cpu%s",num_logical_cpus)
                    cpu_speed_ghz = host.hardware.cpuInfo.hz / 1000000000  # Convert Hz to GHz.
                    #print("cpu speed ghz %s",cpu_speed_ghz)
                    host_cpu_capacity_ghz = num_logical_cpus * cpu_speed_ghz  # Total CPU capacity.
                    host_cpu_usage_ghz = host.summary.quickStats.overallCpuUsage /1000 # Current CPU usage(convert mhz to ghz).
                    total_cpu_capacity_ghz += host_cpu_capacity_ghz
                    total_cpu_usage_ghz += host_cpu_usage_ghz
                    break
                rowData3= str(hostStats['servers'][ind2]['id'])+","+str(hostStats['servers'][ind2]['name'])+","+str(maxMemory)+","+ str(usedMemory)+","+str(maxStorage)+","+str(usedStorage)+","+str(round(host_cpu_capacity_ghz,2)) +","+str(round(host_cpu_usage_ghz,2))
                Hosttable.add_row(rowData3.split(","))
  
                    

               
        
        clusterTotalAllocatedMem= round(clusterTotalAllocatedMem,2)
        clusterTotalAllocatedStorage=round(clusterTotalAllocatedStorage,2)
        clusterTotalUsedMem=round( clusterTotalUsedMem,2)
        clusterTotalUsedStorage=round(clusterTotalUsedStorage,2)
        total_cpu_capacity_ghz=round(total_cpu_capacity_ghz,2)
        total_cpu_usage_ghz=round(total_cpu_usage_ghz,2)
       
        clusterTotalFreeMem =round((clusterTotalAllocatedMem - clusterTotalUsedMem),2)
        clusterTotalFreeStorage =round(( clusterTotalAllocatedStorage - clusterTotalUsedStorage),2)
        #clusterTotalCpuUsage = round((total_cpu_usage_ghz/total_cpu_capacity_ghz),2) 
        clusterTotalFreeCpu=round((total_cpu_capacity_ghz-total_cpu_usage_ghz),2)
        
           
        rowData2=str(CloudList[j]['id'])+","+str(CloudList[j]['name'])+","+str(clusterTotalAllocatedMem)+","+ str(clusterTotalUsedMem)+","+str( clusterTotalAllocatedStorage)+","+str(clusterTotalUsedStorage)+","+str(total_cpu_usage_ghz) +","+str(total_cpu_usage_ghz)        
        CloudStatsTable.add_row(rowData2.split(","))
        CloudTable.add_row(rowData.split(","))
        
        
        # check if stats at cloud level are  less than 80 ,75 or 60 . Send the email notification.
        if(clusterTotalUsedMem!=0):
            if((clusterTotalUsedMem/clusterTotalAllocatedMem )*100 > 80 ):
                
                emailText= str(emailText) + "<b>Cloud "+ str(CloudList[j]['name']) + " Available Memory is less than 80 %<br>" 
                emailText =str(emailText) + "Total Free Memory available is " + str(clusterTotalFreeMem ) +"GB out of "+str(clusterTotalAllocatedMem)+ " <br> <br><br></b>"
            elif((clusterTotalUsedMem/clusterTotalAllocatedMem )*100 > 75 ): 
                 emailText= str(emailText) + "Cloud"+ str(CloudList[j]['name']) + " Available Memory is less than 75 %<br>" 
                 emailText =str(emailText) + "Total Free Memory available is " + str(clusterTotalFreeMem ) +"GB <br><br><br>"
            elif((clusterTotalUsedMem/clusterTotalAllocatedMem )*100 >60 ): 
                 emailText= str(emailText) + "Cloud"+ str(CloudList[j]['name']) + " Available Memory is less than 60 % <br>" 
                 emailText =str(emailText) + "Total Free Memory available is " + str(clusterTotalFreeMem ) +"GB <br><br><br>"
        if (clusterTotalUsedStorage!=0):
            if((clusterTotalUsedStorage/clusterTotalAllocatedStorage)*100 >80):
                #print("send notification  email storage qutoa is too low")
                emailText= str(emailText) + "Cloud "+ str(CloudList[j]['name']) + " Available Storage is less than 80% <br>"
                emailText= str(emailText) + "Total Free storage Available " + str(clusterTotalFreeStorage) +"TB <br><br><br>"
            elif((clusterTotalUsedStorage/clusterTotalAllocatedStorage )*100 > 75 ): 
                 emailText= str(emailText) + "Cloud"+ str(CloudList[j]['name']) + " Available Storage is less than 75 %<br>" 
                 emailText =str(emailText) + "Total Free Memory available is " + str(clusterTotalFreeStorage ) +"GB <br><br><br>"
            elif((clusterTotalUsedStorage/clusterTotalAllocatedStorage)*100 > 60 ): 
                 emailText= str(emailText) + "Cloud"+ str(CloudList[j]['name']) + " Available Storage is less than 60 % <br>" 
                 emailText =str(emailText) + "Total Free Memory available is " + str(clusterTotalFreeStorage ) +"GB <br><br><br>"    
        if (total_cpu_usage_ghz!=0):
           if((total_cpu_usage_ghz/total_cpu_capacity_ghz)*100  >80):
                #print("send notification  email storage qutoa is too low")
                emailText= str(emailText) + "Cloud "+ str(CloudList[j]['name']) + " Available CPU is less than 80% <br>"
                emailText= str(emailText) + "Total Free CPU % " + str(clusterTotalFreeCpu) +"GHZ<br><br><br>"
           elif((total_cpu_usage_ghz/total_cpu_capacity_ghz)*100  > 75 ): 
                 emailText= str(emailText) + "Cloud "+ str(CloudList[j]['name']) + " Available CPU is less than 75% <br>"
                 emailText= str(emailText) + "Total Free CPU % " + str(clusterTotalFreeCpu) +"Ghz<br><br><br>"
           elif((total_cpu_usage_ghz/total_cpu_capacity_ghz)*100 > 60 ): 
                 emailText= str(emailText) + "Cloud "+ str(CloudList[j]['name']) + " Available CPU is less than 60% <br>"
                 emailText= str(emailText) + "Total Free CPU % " + str(clusterTotalFreeCpu)  +"Ghz<br><br><br>"   
    emailConfig(emailText)       
      
       
#call functions

getHostList()
Disconnect(si)
print(CloudTable)  # this table stores all vmware cloud id and cloud name that exist in  morpheus .
print(CloudStatsTable) # this table stores cloud level stats like total  allocated memeory ,total consumed memory etc.
print(Hosttable) # this  table stores host level stats like total cluster allocated memory ,used memory etc.
