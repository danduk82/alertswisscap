import requests
import json
import xmltodict
from capparselib.parsers import CAPParser



class Client:
    def __init__(self, url):
        self.url = url
        
    def get_parsed_alerts(self):
        response = requests.get(self.url)
        if response.status_code != 200:
            raise Exception('Error while getting alerts')
        return self._parse_alerts(json.loads(response.content)['body']['alerts'])
    
    def get_alerts(self):
        response = requests.get(self.url)
        if response.status_code != 200:
            raise Exception('Error while getting alerts')
        return json.loads(response.content)['body']['alerts']
       
    def _parse_alerts(self, alerts):
        parsed_alerts = []
        for alert in alerts:
            parsed_alert = {}
            parsed_alert['reference'] = alert['reference']
            parsed_alert['content'] = CAPParser(alert['alert']).as_dict()
            parsed_alerts.append(parsed_alert)
        return parsed_alerts
    