import re

from reg_exp import ip_address_re, remove_command_re, remove_nickname_re


def make_shield(input_string: str) -> str:
    output_string = input_string
    for symbol in ["-", "_"]:
        if symbol in output_string:
            output_string = output_string.replace(symbol, "\\" + symbol)
    return output_string


def parse_ip(input_string: str) -> str:
    try:
        return re.findall(ip_address_re, input_string)[0]
    except Exception as e:
        return re.findall(ip_address_re, input_string)


def remove_nickname(input_string: str) -> str:
    if "@" in input_string:
        output_string = ''.join(remove_nickname_re.split(input_string)).strip()
    else:
        output_string = input_string.strip()
    return output_string


def remove_command(input_string: str) -> str:
    output_string = ''.join(remove_command_re.split(input_string)).strip()
    return output_string


def make_pretty_alerts(input_alerts: list) -> str:
    pretty_alerts = ""
    if input_alerts:
        counter = 1
        for alert in input_alerts:
            body = alert[0]
            author = alert[2]
            source_response = ""
            if alert[1] != "":
                source_response = f"source: {alert[1]}\n"
            pretty_alerts += f"{counter}.\n`{body}`\nalert_date: {alert[3]}\n{source_response}alert_author: {author}\n\n"
            counter += 1
        pretty_alerts = make_shield(pretty_alerts)
    else:
        pretty_alerts = "there is no data"
    return pretty_alerts
