import json

import requests
import xmltodict
from capparselib.parsers import CAPParser

# DEFAULT_CAP_URL = "https://alertswiss.poatest.ch/alertswiss/v2/alerts?scope=Public"
# DEFAULT_CAP_URL = "https://alertswiss.poatest.ch/alertswiss/v2/alerts?scope=Restricted"
# DEFAULT_CAP_URL = "https://alertswiss.poatest.ch/alertswiss/v2/alerts?scope=All"
DEFAULT_CAP_URL = "https://alertswiss.poatest.ch/alertswiss/v1/alerts"


class CAPClient:
    def __init__(self, url=DEFAULT_CAP_URL):
        self.url = url

    def strip_url(self):
        if self.url.startswith("file://"):
            return self.url[7:]
        else:
            return self.url

    def _get_raw_alerts(self):
        if self.url.startswith("http"):
            response = requests.get(self.url)
            if response.status_code != 200:
                raise Exception("Error while getting alerts")
            return json.loads(response.content)["body"]["alerts"]
        elif self.url.startswith("file"):
            with open(self.strip_url()) as f:
                return json.loads(f.read())["body"]["alerts"]

    def get_parsed_alerts(self):
        return self._parse_alerts(self._get_raw_alerts())

    def get_alerts(self):
        return self._get_raw_alerts()

    def _parse_alerts(self, alerts):
        parsed_alerts = []
        for alert in alerts:
            parsed_alert = {}
            parsed_alert["reference"] = alert["reference"]
            parsed_alert["content"] = CAPParser(alert["alert"]).as_dict()
            parsed_alerts.append(parsed_alert)
        return parsed_alerts
