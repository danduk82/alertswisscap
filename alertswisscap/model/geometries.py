import json
import logging
import re

from shapely.geometry import MultiPolygon, Point, Polygon

logging.basicConfig(level=logging.DEBUG)

log = logging.getLogger()


class Circle:
    def __init__(self, x_y_r: tuple) -> None:
        self.point = Point(x_y_r[0], x_y_r[1])
        self.radius = x_y_r[2]

    def as_dict(self):
        return {"point": self.point, "radius": self.radius}


class AlertSwissCapGeometryPoints:
    """
    Converts the points from the AlertSwissCap API
    to a shapely Point object with a radius attribute.

    parameters:
        cap_points: str
            The cap_point from the AlertSwissCap API
            in the format:
                "circles": [
                                "47.17511,8.49602 0.240069058",
                                "47.18116,8.52603 0.26664098",
                                "47.08692,8.57041 0.27024381599999997",
                                "47.29503,8.88693 0.370062386"
                            ]
            with the first two comma-separated numbers being the coordinates
            and the third number being the radius
    """

    def __init__(self, cap_points: list) -> None:
        self._points = []
        for cap_point in cap_points:
            self._points.append(Circle(self._parse_cap_point(cap_point)))

    def _parse_cap_point(self, cap_point):
        coord = cap_point.split(" ")[0].split(",")
        radius = float(cap_point.split(" ")[1])
        return tuple([float(i) for i in coord] + [radius])

    def points(self):
        return self._points


class AlertSwissCapGeometryMultiPolygon:
    """
    Convert the polygons and exclude polygons from the AlertSwissCap API
    to a shapely MultiPolygon object.

    parameters:
        cap_polygons: dict
            The cap_polygons dict from the AlertSwissCap API
            contains the polygons and exclude polygons
            in the format:
            {
                'polygons' : [
                        '47.123,8.123 47.123,8.123 47.123,8.123',
                        '47.123,8.123 47.123,8.123 47.123,8.123'
                    ],
                'exclude_polygons' : [
                        '1|47.113,8.113 47.122,8.122 47.123,8.123',
                        '2|47.123,8.123 47.123,8.123 47.123,8.123'
                    ]
            }
    """

    def __init__(self, cap_polygons: list, exclude_polygons=[]) -> None:
        self._exclude_polygon_pattern = re.compile(r"(\d+)\|(.*)")
        self._multiPolygon = MultiPolygon(self._parse_cap_polygons(cap_polygons, exclude_polygons))

    def _parse_cap_polygons(self, cap_polygons, exclude_polygons):
        polygons = []
        holes_dict = {}

        if exclude_polygons:
            for cap_exlude_polygon in exclude_polygons:
                matches = self._exclude_polygon_pattern.match(str(cap_exlude_polygon))
                key = int(matches.group(1)) - 1
                coord = self._coord_str_list_to_polygon(matches.group(2).split(" "))
                if not key in holes_dict.keys():
                    holes_dict[key] = []
                holes_dict[key].append(coord)

        for c in range(len(cap_polygons)):
            cap_polygon = str(cap_polygons[c])
            log.debug(f"cap_polygon: {cap_polygon}")
            exterior = self._coord_str_list_to_polygon(cap_polygon.split(" "))
            interiors = []
            if c in holes_dict.keys():
                interiors = holes_dict[c]
            polygons.append(Polygon(exterior, interiors))

        return polygons

    def _coord_str_list_to_polygon(self, coord_str_list):
        log.debug(f"coord_str_list: {coord_str_list}")
        return [self._coord_str_to_coord_tuple(coord_str) for coord_str in coord_str_list]

    def _coord_str_to_coord_tuple(self, coord_str):
        log.debug(f"coord_str: {coord_str}")
        return tuple([float(i) for i in coord_str.split(",")])

    def as_multipolygon(self):
        return self._multiPolygon


class CAPGeocodesDict(dict):
    def __init__(self, input_list=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.key_prefix = "valueName"
        self.value_prefix = "value"
        if input_list:
            self.deserialize(input_list)
        log.debug(self)

    def deserialize(self, input_list):
        for item in input_list:
            key = item[self.key_prefix]
            if self.value_prefix in item:
                try:
                    value = super().__getitem__(key)
                except KeyError:
                    value = []
                value.append(item[self.value_prefix])
            else:
                value = None
            super().__setitem__(key, value)

    def items(self):
        for key, value in super().items():
            for v in value:
                yield key, v

    def serialize(self):
        return [{self.key_prefix: key, self.value_prefix: value} for key, value in self.items()]

    def __repr__(self) -> str:
        return str(self.serialize())

    def __str__(self):
        return json.dumps(self.serialize())
