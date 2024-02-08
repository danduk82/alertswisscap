import argparse as ap

from apiclient.client import DEFAULT_CAP_URL, CAPClient
from model.geometries import AlertSwissCapGeometryMultiPolygon


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

    cap_polygons = {}

    cap_polygons["polygons"] = alerts[0]["content"][0]["cap_info"][1]["cap_area"][0]["polygons"]
    cap_polygons["exclude_polygons"] = []
    for geocode in alerts[0]["content"][0]["cap_info"][1]["cap_area"][0]["geocodes"]:
        if geocode["valueName"] == "ALERTSWISS_EXCLUDE_POLYGON":
            cap_polygons["exclude_polygons"].append(geocode["value"])

    # print(cap_polygons)

    # note to self
    # in alerts[nb_alert]['content'][0]['cap_info'][np_cap_info]['cap_area'][0]['polygons']
    # sometimes there is no 'cap_area'
    # possibly sometimes there is no 'polygons'
    # nb_cap_info is equal to the number of languages, but all languages have the same exact 'cap_area' and 'polygons', so we can just take the first one

    mp = AlertSwissCapGeometryMultiPolygon(cap_polygons)
    print(mp._multiPolygon)


if __name__ == "__main__":
    main()
