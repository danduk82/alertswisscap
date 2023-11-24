from apiclient.client import CAPClient
from model.geometries import AlertSwissCapGeometryMultiPolygon

client = CAPClient()
alerts = client.get_parsed_alerts()

cap_polygons = {}

cap_polygons['polygons'] = alerts[0]['content'][0]['cap_info'][1]['cap_area'][0]['polygons']
cap_polygons['exclude_polygons'] = []
for geocode in  alerts[0]['content'][0]['cap_info'][1]['cap_area'][0]['geocodes']:
        if geocode['valueName'] == 'ALERTSWISS_EXCLUDE_POLYGON':
            cap_polygons['exclude_polygons'].append(geocode['value'])

#print(cap_polygons)

mp = AlertSwissCapGeometryMultiPolygon(cap_polygons)
print(mp._multiPolygon)