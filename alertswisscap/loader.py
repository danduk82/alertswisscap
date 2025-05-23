import argparse as ap
import logging

from alertswisscap.apiclient.client import DEFAULT_CAP_URL, CAPClient
from alertswisscap.controller.pgcontroller import CapPgController
from alertswisscap.model.geometries import AlertSwissCapGeometryMultiPolygon

logger = logging.getLogger(__name__)


def parser():
    parser = ap.ArgumentParser(description="AlertSwiss CAP Client")
    parser.add_argument(
        "-u",
        "--url",
        default=DEFAULT_CAP_URL,
        help="url of api or input file",
        required=False,
    )
    return parser.parse_args()


def main():
    args = parser()
    client = CAPClient(url=args.url)
    alerts = client.get_parsed_alerts()

    cap_polygons = alerts[0]["content"][0]["cap_info"][1]["cap_area"][0]["polygons"]
    exclude_polygons = []
    for geocode in alerts[0]["content"][0]["cap_info"][1]["cap_area"][0]["geocodes"]:
        if geocode["valueName"] == "ALERTSWISS_EXCLUDE_POLYGON":
            exclude_polygons.append(geocode["value"])

    # print(cap_polygons)

    # note to self
    # in alerts[nb_alert]['content'][0]['cap_info'][np_cap_info]['cap_area'][0]['polygons']
    # sometimes there is no 'cap_area'
    # possibly sometimes there is no 'polygons'
    # nb_cap_info is equal to the number of languages, but all languages have the same exact 'cap_area' and 'polygons', so we can just take the first one

    mp = AlertSwissCapGeometryMultiPolygon(cap_polygons, exclude_polygons)
    print(mp._multiPolygon)

    pg_url = "postgresql://naz_user:password@localhost:5432/neoc_basics"
    cap_pg_controller = CapPgController(pg_url)
    with open("/tmp/parsed_alerts_2.json", "w") as f:
        import json

        f.write(json.dumps(alerts, indent=2))
    # a, i = cap_pg_controller.load_alerts()
    # logger.debug(f"alerts: {a[0].cap_info[0].cap_language}")
    # logger.debug(f"infos: {i[0].cap_alert_cap_id}")
    cap_pg_controller.put_alerts(alerts)


if __name__ == "__main__":
    main()
