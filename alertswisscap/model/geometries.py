from shapely.geometry import Polygon, MultiPolygon
import re

import logging

logging.basicConfig(level=logging.DEBUG)

log = logging.getLogger()

class AlertSwissCapGeometryPoint():
    pass

class AlertSwissCapGeometryMultiPolygon():
    """ Convert the polygons and exclude polygons from the AlertSwissCap API to a shapely MultiPolygon object
    parameters:
        cap_polygons: dict
            The cap_polygons dict from the AlertSwissCap API
            contains the polygons and exclude polygons
            in the format:
            { 
                'polygons' : [ '47.123,8.123 47.123,8.123 47.123,8.123',  '47.123,8.123 47.123,8.123 47.123,8.123'],
                'exclude_polygons' : [ '1|47.113,8.113 47.122,8.122 47.123,8.123',  '2|47.123,8.123 47.123,8.123 47.123,8.123']
            }
    """
    def __init__(self, cap_polygons: dict) -> None:
        self._exclude_polygon_pattern = re.compile(r'(\d+)\|(.*)')
        self._multiPolygon = MultiPolygon(self._parse_cap_polygons(cap_polygons))
        
    def _parse_cap_polygons(self, cap_polygons):
        polygons = []
        holes_dict = {}
        
        for cap_exlude_polygon in cap_polygons['exclude_polygons']:
            matches = self._exclude_polygon_pattern.match(str(cap_exlude_polygon))
            key = int(matches.group(1)) - 1
            coord = self._coord_str_list_to_polygon(matches.group(2).split(' '))
            if not key in holes_dict.keys():
                holes_dict[key] = []
            holes_dict[key].append(coord)
        
        for c in range(len(cap_polygons['polygons'])):
            cap_polygon = str(cap_polygons['polygons'][c])
            log.debug('cap_polygon: {}'.format(cap_polygon))
            exterior = self._coord_str_list_to_polygon(cap_polygon.split(' '))
            interiors = []
            if c in holes_dict.keys():
                interiors = holes_dict[c]
            polygons.append(Polygon(exterior, interiors))
        
        return polygons
    
    def _coord_str_list_to_polygon(self, coord_str_list):
        log.debug('coord_str_list: {}'.format(coord_str_list))
        return [self._coord_str_to_coord_tuple(coord_str) for coord_str in coord_str_list]
    
    def _coord_str_to_coord_tuple(self, coord_str):
        log.debug('coord_str: {}'.format(coord_str))
        return tuple([float(i) for i in coord_str.split(',')])
    
    def as_multipolygon(self):
        return self._multiPolygon
    
class AlertSwissCapGeometryMultiLine():
    pass