# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import requests, json
import threading, time

def tool_integration():
    register=tool_register()
    if register.status_code==200:
        t=threading.Thread(target=ping_alert_list)
        t.start()
    return register

def tool_register():
    url="http://194.2.241.244/measure/api/analysis/register"
    data=json.dumps({'configurationURL':'http://54.246.231.184/tool/','description':'Analysis and suggestion tool of software measurements', 'name':'SuggesterTool'})
    postJSON=json.loads(data)
    #headers={"content-type":"application/json"}
    content=requests.put(url,json=postJSON) #--> si besoin ajouter headers=headers
    return content

def tool_alert_list():
    url="http://194.2.241.244/measure/api/analysis/alert/list"
    param={'id':'SuggesterTool'}
    content=requests.get(url,params=param)
    return content

def ping_alert_list():
    while True:
        time.sleep(10)
        alerts=tool_alert_list()
        json_alerts=alerts.json()
        #print(json_alerts)
        #print(json_alerts['alerts'])
        for alert in json_alerts['alerts']:
            #print(alert)
            #print(alert['alertType'])
            if alert['alertType']=='ANALYSIS_ENABLE':
                for propertie in alert['properties']:
                    tool_configuration(propertie['value'])
    return None           
        
    
def tool_configuration(propertie):
    url="http://194.2.241.244/measure/api/analysis/configure"
    data_string={'cards': [{'cardUrl': 'http://54.246.231.184/tool/view/plans/form','label': 'Measurement_Plan_Form','preferedHeight': 400,'preferedWidth': 300},{'cardUrl': 'http://54.246.231.184/tool/view/suggestions','label': 'Suggestions','preferedHeight': 400,'preferedWidth': 300}],'configurationUrl': 'http://54.246.231.184/tool', 'projectAnalysisId':int(propertie),'viewUrl': 'http://54.246.231.184/tool'}
    data=json.dumps(data_string)
    postJSON=json.loads(data)
    content=requests.put(url,json=postJSON)
    return content


#pour être notifier si une nouvelle mesure a été ajoutée (par exemple)
#def tool_alert_subscribe():
    
