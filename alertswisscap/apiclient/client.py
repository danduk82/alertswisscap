import json
import logging

import requests
import xmltodict
from capparselib.parsers import CAPParser

# DEFAULT_CAP_URL = "https://alertswiss.poatest.ch/alertswiss/v2/alerts?scope=Public"
# DEFAULT_CAP_URL = "https://alertswiss.poatest.ch/alertswiss/v2/alerts?scope=Restricted"
# DEFAULT_CAP_URL = "https://alertswiss.poatest.ch/alertswiss/v2/alerts?scope=All"
DEFAULT_CAP_URL = "https://alertswiss.poatest.ch/alertswiss/v1/alerts"

logger = logging.getLogger(__name__)
from lxml.objectify import BoolElement, FloatElement, IntElement, StringElement


class CAPClient:
    def __init__(self, url=DEFAULT_CAP_URL):
        logger.debug(f"initializing CAPClient with url: {url}")
        self.url = url

    def strip_url(self):
        if self.url.startswith("file://"):
            return self.url[7:]
        else:
            return self.url

    def _get_raw_alerts(self):
        logger.debug(f"getting alerts from {self.url}")
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
            logger.debug(f"alert to be parsed: {alert}")
            parsed_alert = {}
            parsed_alert["reference"] = alert["reference"]
            parsed_alert["content"] = CAPParser(alert["alert"]).as_dict()
            logger.debug(f"parsed_alert: {parsed_alert}")
            parsed_alerts.append(parsed_alert)
        with open("/tmp/parsed_alerts.json", "w") as f:
            f.write(json.dumps(CAPClient.cleanup_xml2dict_classes(parsed_alerts), indent=4))
        return CAPClient.cleanup_xml2dict_classes(parsed_alerts)

    @staticmethod
    def cleanup_xml2dict_classes(obj):
        if isinstance(obj, StringElement):
            return str(obj)
        elif isinstance(obj, BoolElement):
            return bool(obj)
        elif isinstance(obj, IntElement):
            return int(obj)
        elif isinstance(obj, FloatElement):
            return float(obj)
        elif isinstance(obj, dict):
            return {key: CAPClient.cleanup_xml2dict_classes(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [CAPClient.cleanup_xml2dict_classes(item) for item in obj]
        else:
            return obj

    def __str__(self) -> str:
        return json.dumps(self.get_parsed_alerts(), indent=4)
