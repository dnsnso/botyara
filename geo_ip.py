import ipinfo

from config import settings


def get_geo_ip(ip_address: str):# -> tuple(str, str):
    access_token = settings.GEOIP_TOKEN
    handler = ipinfo.getHandler(access_token)
    details = handler.getDetails(ip_address)
    return {"country_code": details.country, "country_name": details.country_name}
