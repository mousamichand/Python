import requests
import json
import urllib3
from prettytable import PrettyTable

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) 

def apiHeader(url):
 
  token=morpheus['morpheus']['apiAccessToken'] 
  
  
 applianceUrl = morpheus['morpheus']['applianceUrl']
  url =    applianceUrl + url
  headers = {"Content-Type":"application/json","Accept":"application/json","Authorization": "BEARER " + (token)}
  response = requests.get(url,headers=headers,verify=False)
  data = json.loads(response.text)
  return (data) 

def  printoptionlist():
 #function to list all inputs.
 url = "api/library/option-types?max=1000&offset=0"
 data = apiHeader(url)
 return(data['optionTypes'])
  
def workflowInputs():
  #function to list all operational workflow.
  url = "api/task-sets?type=operation&max=1000&offset=0"
  data = apiHeader(url)
  return(data['taskSets'])
     
def  layoutInputs():
  #function to list all layouts.
  url = "api/library/layouts??max=1000&offset=0"
  data = apiHeader(url)
  return(data['instanceTypeLayouts'])

def AllInstanceTypes():
  #function to return all instancestypes.
  url = "api/library/instance-types?max=1000&offset=0"
  data = apiHeader(url)
  return(data['instanceTypes'])

def instanceInputs():
  instanceList=AllInstanceTypes()
  instanceDetails =[]
 # ind1=0
  for i in range(len(instanceList)):
    url = "api/library/instance-types/" + str(instanceList[i]['id'])
    data = apiHeader(url)
    instanceDetails.append(data['instanceType'])
  #  ind1=ind1+1
  return(instanceDetails)  
   
def main(): 
 allInputList= printoptionlist() #get all inputs
 workFlowInputList = workflowInputs() #get allinputs attached to opeartional workflow
 layoutInputList= layoutInputs()  #get all inputs attached to layout 
 testList = instanceInputs() 
 table = PrettyTable(["OPTION ID", "OPTION NAME", "ENDPOINT","ENDPOINT ID","ENDPOINT NAME"])
  
 for i in range(len(allInputList)):
   flag = 0
   for j in range (len(workFlowInputList)):
    for k in range (len(workFlowInputList[j]['optionTypes'])):
       if (allInputList[i]['id']==workFlowInputList[j]['optionTypes'][k]['id']):
          #print (str(allInputList[i]['id']) + "\t" + allInputList[i]['name'] +"\t Workflow \t " + str(workFlowInputList[j]['id'])+"\t \t" +str(workFlowInputList[j]['name']))
          rowdata =  str(allInputList[i]['id'])  + ","  + allInputList[i]['name'] + ", Workflow ," + str(workFlowInputList[j]['id']) + "," + str(workFlowInputList[j]['name']) 
          table.add_row(rowdata.split(","))
          flag = 1
          break
   for ind1 in range (len(layoutInputList)):
     for ind2 in  range (len(layoutInputList[ind1]['optionTypes'])):
       if (allInputList[i]['id']==layoutInputList[ind1]['optionTypes'][ind2]['id']):
          #print (str(allInputList[i]['id']) + "\t" + allInputList[i]['name'] +"\t Layout  \t" +str(layoutInputList[ind1]['id'])+"\t" +str(layoutInputList[ind2]['name']))
          rowdata =  str(allInputList[i]['id']) + "," +  allInputList[i]['name'] + ", Layout ," + str(layoutInputList[ind1]['id']) + "," + str(layoutInputList[ind1]['name']) 
          table.add_row(rowdata.split(","))
          flag = 1
          break
   for ind3 in range(len(testList )): 
      for ind4 in  range (len(testList [ind3]['optionTypes'])):
        if (allInputList[i]['id']==testList [ind3]['optionTypes'][ind4]['id']):
           rowdata =  str(testList [ind3]['optionTypes'][ind4]['id']) + "," +testList [ind3]['optionTypes'][ind4]['name'] +" , Instance ,"+ str(testList[ind3]['id'])+ "," + testList [ind3]['name'] 
           #print(str(testList [ind3]['optionTypes'][ind4]['id']) +"\t" + testList [ind3]['optionTypes'][ind4]['name'] +"\t Instance "+ str(testList[ind3]['id'])+ "\t" + testList [ind3]['name'])
           table.add_row(rowdata.split(","))
           break
   if (flag==0):
       #print(str(allInputList[i]['id']) + "\t" + allInputList[i]['name']  +"\t not in use \t - \t - \t")
       rowdata = str(allInputList[i]['id']) + "," + allInputList[i]['name']  + "," +  "Not in use ," + " - ," + "-" 
       table.add_row(rowdata.split(","))
 print(table)

main()
