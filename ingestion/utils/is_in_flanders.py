
def is_in_flanders(lon, lat, bbox):
    return (
        bbox["min_lon"] <= lon <= bbox["max_lon"] and
        bbox["min_lat"] <= lat <= bbox["max_lat"]
    )