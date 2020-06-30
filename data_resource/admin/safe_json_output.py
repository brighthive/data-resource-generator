import json
import datetime
import decimal


def unknown_field_json_converter(o):
    if isinstance(o, datetime.datetime) or isinstance(o, datetime.time):
        return str(o.isoformat()) + "Z"
    if isinstance(o, datetime.date):
        return str(o.isoformat())
    if isinstance(o, decimal.Decimal):
        return float(o)


def safe_json_dumps(json_dict):
    """This will add explicit conversions for types to json.dumps."""
    return json.dumps(json_dict, default=unknown_field_json_converter)
