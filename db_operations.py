import psycopg2
from datetime import datetime
from typing import Union

from config import settings


conn = psycopg2.connect(dbname=settings.POSTGRES_DB, user=settings.POSTGRES_USER, password=settings.POSTGRES_PASSWORD, host=settings.POSTGRES_SERVER, port=settings.POSTGRES_PORT)
cursor = conn.cursor()


def get_legal_users() -> list[int]:
    cursor.execute(f"SELECT * FROM legal_users;")
    users = cursor.fetchall()
    legal_users_id = [int(user[1]) for user in users]
    return legal_users_id


def get_ip(ip_address: str) -> list:
    cursor.execute(f"SELECT * FROM ips WHERE ip_address = '{ip_address}';")
    record = cursor.fetchall()
    return record


def add_ip(ip: str, ban_reason: str, alert_source: str, ban_author: str) -> bool:
    if not get_ip(ip):
        cursor.execute(f"INSERT INTO ips (ip_address, ban_reason, alert_source, banned_on, ban_author) VALUES ('{ip}', '{ban_reason}', '{alert_source}', '{datetime.now().date()}', '{ban_author}');")
        conn.commit()
        return True
    return False


def get_ip_today():# -> Union[list[str], Exception]:
    try:
        cursor.execute(f"SELECT * FROM ips WHERE banned_on = '{datetime.now().date()}';")
        ip_addresses = cursor.fetchall()
        output = [ip_address[1].split("/")[0] for ip_address in ip_addresses]
        output.sort()
        return output
    except Exception as e:
        return e


def get_ip_by_date(date: datetime.date):# -> Union[list[str], Exception]:
    try:
        cursor.execute(f"SELECT * FROM ips WHERE banned_on = '{date}';")
        ip_addresses = cursor.fetchall()
        output = [ip_address[1].split("/")[0] for ip_address in ip_addresses]
        output.sort()
        return output
    except Exception as e:
        return e


def get_ip_by_period(date_1: datetime.date, date_2: datetime.date):# -> Union[list[str], Exception]:
    try:
        cursor.execute(f"SELECT * FROM ips WHERE banned_on >= '{date_1}' AND banned_on <= '{date_2}';")
        ip_addresses = cursor.fetchall()
        output = [ip_address[1].split("/")[0] for ip_address in ip_addresses]
        output.sort()
        return output
    except Exception as e:
        return e


def remove_ip(ip_address: str) -> bool:
    if get_ip(ip_address):
        cursor.execute(f"DELETE FROM ips WHERE ip_address = '{ip_address}';")
        conn.commit()
        return True
    return False


def get_alerts_by_date(date: datetime.date):
    try:
        cursor.execute(f"SELECT * FROM alerts WHERE alert_date = '{date}';")
        alerts = cursor.fetchall()
        output = [(alert[1], alert[2], f"@{alert[3]}", datetime.date(alert[4]).strftime("%d.%m.%Y")) for alert in alerts]
        return output
    except Exception as e:
        return e


def get_alerts_by_period(date_1: datetime.date, date_2: datetime.date):# -> Union[list[tuple()], Exception]:
    try:
        cursor.execute(f"SELECT * FROM alerts WHERE alert_date >= '{date_1}' AND alert_date <= '{date_2}';")
        alerts = cursor.fetchall()
        output = [(alert[1], alert[2], f"@{alert[3]}", datetime.date(alert[4]).strftime("%d.%m.%Y")) for alert in alerts]
        return output
    except Exception as e:
        return e
    

def create_file_ip_by_date(date: datetime.date):
    try:
        cursor.execute(f"SELECT * FROM ips WHERE banned_on = '{date}';")
        ip_addresses = cursor.fetchall()
        output = [("ip", "ban_reason", "source", "ban_author", "ban_date")]
        output.extend([(ip_address[1].split("/")[0], ip_address[2], ip_address[3], f"@{ip_address[4]}", datetime.date(ip_address[5]).strftime("%d.%m.%Y")) for ip_address in ip_addresses])
        return output
    except Exception as e:
        print(e)
        return e


def create_file_ip_by_period(date_1: datetime.date, date_2: datetime.date):
    try:
        cursor.execute(f"SELECT * FROM ips WHERE banned_on >= '{date_1}' AND banned_on <= '{date_2}';")
        ip_addresses = cursor.fetchall()
        output = [("ip", "ban_reason", "source", "ban_author", "ban_date")]
        output.extend([(ip_address[1].split("/")[0], ip_address[2], ip_address[3], f"@{ip_address[4]}", datetime.date(ip_address[5]).strftime("%d.%m.%Y")) for ip_address in ip_addresses])
        return output
    except Exception as e:
        print(e)
        return e


def create_file_alerts_by_date(date: datetime.date):
    try:
        cursor.execute(f"SELECT * FROM alerts WHERE alert_date = '{date}';")
        alerts = cursor.fetchall()
        output = [("alert_body", "alert_source", "alert_author", "alert_date")]
        output.extend((alert[1], alert[2], f"@{alert[3]}", datetime.date(alert[4]).strftime("%d.%m.%Y")) for alert in alerts)
        return output
    except Exception as e:
        return e


def create_file_alerts_by_period(date_1: datetime.date, date_2: datetime.date):
    try:
        cursor.execute(f"SELECT * FROM alerts WHERE alert_date >= '{date_1}' AND alert_date <= '{date_2}';")
        alerts = cursor.fetchall()
        output = [("alert_body", "alert_source", "alert_author", "alert_date")]
        output.extend((alert[1], alert[2], f"@{alert[3]}", datetime.date(alert[4]).strftime("%d.%m.%Y")) for alert in alerts)
        return output
    except Exception as e:
        return e


def add_alert(alert_body: str, source: str, alert_author: str) -> None:
    cursor.execute(f"INSERT INTO alerts (alert_text, alert_source, alert_author, alert_date) VALUES ('{alert_body}', '{source}', '{alert_author}', '{datetime.now().date()}');")
    conn.commit()
    return
