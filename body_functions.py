from datetime import datetime
import pandas as pd
import flag

from secondary_functions import remove_nickname, remove_command, parse_ip, make_shield, make_pretty_alerts

from db_operations import get_ip, add_ip, remove_ip, get_ip_today, get_ip_by_date, get_ip_by_period
from db_operations import add_alert, get_alerts_by_date, get_alerts_by_period
from db_operations import create_file_ip_by_date, create_file_ip_by_period
from db_operations import create_file_alerts_by_date, create_file_alerts_by_period

from check_ip import is_valid, is_local, is_our

from geo_ip import get_geo_ip

from reg_exp import parse_ip_re

from config import settings


def help_bot() -> str:
    ip = "`/ip`\n—`/ip` - заблокированные IP за сегодня\n—`/ip X.X.X.X` - проверка IP адреса\n—`/ip date` - заблокированные IP за date\n—`/ip date_1-date_2` - заблокированные IP за промежуток date\\_1-date\\_2\n—`/file` - экспорт в файл; добавляется в конце запроса\n\n"
    ban = "`/ban`\n—`/ban X.X.X.X` - блокировка IP\n—`/ban X.X.X.X ban_reason` - блокировка IP с указанием причины\n—`/ban X.X.X.X /source` - блокировка IP с указанием источника\n`/ban X.X.X.X x_reason /x_source`\n`Y.Y.Y.Y y_reason /y_source` - блокировка нескольких IP\n\n"
    unban = "`/unban`\n—`/unban X.X.X.X` - разблокировка IP\n`/unban X.X.X.X`\n`Y.Y.Y.Y` - разблокировка нескольких IP\n\n"
    alert = "`/alert`\n—`/alert` - алерты за сегодня\n—`/alert date` - алерты за date\n—`/alert date_1-date_2` - алерты за промежуток date\\_1-date\\_2\n—`/file` - экспорт в файл; добавляется в конце запроса\n\n"
    add_alert = "`/addalert`\n`/addalert alert_body` - добавление алерта\n`/addalert alert_body /alert_source` - добавление алерта с указанием источника\n\n"
    contact = "*for any issues contact @deen3s*"
    response = ip + ban + unban + alert + add_alert + contact
    return response


def ban_bot(input_text: str, ban_author: str) -> str:
    total_response = ""
    input_text = remove_nickname(input_text)
    without_command = remove_command(input_text)
    splitted_text = without_command.split("\n")
    for record in splitted_text:
        bot_response = ""
        ip_address = parse_ip(record)
        try:
            if is_valid(ip_address):
                if is_local(ip_address):
                    bot_response = f"{ip_address} - is actually local🤷‍♂️"
                    # bot.send_sticker(message.chat.id, stickers.STICKER_GENIALNO)
                else:
                    if is_our(ip_address):
                        # local_stickers = [stickers.STICKER_DURKA, stickers.STICKER_PUTIN, stickers.STICKER_KIT_NAH, stickers.STICKER_PESIK, stickers.STICKER_CHEL, stickers.STICKER_NAH]
                        # bot.send_sticker(message.chat.id, choice(local_stickers))
                        bot_response = f"{ip_address} - is actually our public🤷‍♂️"
                    else:
                        reason_source = ''.join(parse_ip_re.split(without_command))
                        reason, source = "", ""
                        if reason_source:
                            if "/" in reason_source:
                                reason_source = reason_source.split("/")
                                reason = reason_source[0]
                                source = reason_source[1]
                            else:
                                reason = reason_source
                        if reason:
                            reason = reason.strip()
                        if source:
                            source = source.strip()
                        ok = add_ip(ip_address, reason, source, ban_author)
                        if ok:
                            # bot.send_sticker(message.chat.id, stickers.STICKER_LADNO, reply_to_message_id=message.id)
                            bot_response = f"`{ip_address}` - has been banned"
                        else:
                            record = get_ip(ip_address)
                            ip_address = record[0][1].split("/")[0]
                            bot_response = f"`{ip_address}` - already banned"
                            # bot.reply_to(message, response, parse_mode="markdown")
            else:
                # bot.reply_to(message, "скормите мне валидный IP, пожалуйста 🥲")
                bot_response = f"{record} - invalid input data"
        except ValueError as e:
            bot_response = f"{record} - invalid input data"
            print(e)
        finally:
            total_response += (bot_response + "\n")
    return total_response
    # bot.send_sticker(message.chat.id, stickers.STICKER_SAD)


def add_alert_bot(input_text: str, alert_author: str) -> str:
    bot_response = ""
    input_text = remove_nickname(input_text)
    without_command = remove_command(input_text)
    if without_command:
        separated_alert = without_command.split("/")
        body = separated_alert[0].strip()
        source = ""
        try:
            source = separated_alert[1].strip()
        except Exception as e:
            pass
            # bot_response = e
        try:
            add_alert(body, source, alert_author)
            bot_response = "alert has been added"
            # bot.send_sticker(message.chat.id, stickers.STICKER_LADNO)
        except Exception as e:
            # bot.send_sticker(message.chat.id, stickers.STICKER_SAD, reply_to_message_id=message.id)
            bot_response = e
    else:
        bot_response = "invalid alert body"
    return bot_response


def get_pretty_date(date):
    return datetime.strptime(date, '%d.%m.%Y')


def alert_bot(input_text: str) -> str:
    bot_response = ""
    input_text = remove_nickname(input_text)
    without_command = remove_command(input_text)
    file_indicator = False
    if "/file" in without_command:
        without_command = without_command.split("/file")[0].strip()
        file_indicator = True
        file_name = settings.FILE_PATH + f"Alerts_IPs_"
    if not without_command:
        if file_indicator:
            file_name += f"{str(datetime.now().strftime('%d.%m.%Y'))}.xlsx"
            file = open(file_name, 'w+')
            file.close()
            writer = pd.ExcelWriter(file_name, engine='xlsxwriter')
            data = pd.DataFrame(create_file_alerts_by_date(datetime.now().date().strftime('%d.%m.%Y')))
            data.to_excel(writer, 'Sheet1')
            writer.close()
            bot_response = f"created a file named\n`{file_name}`"
        else:
            alerts = get_alerts_by_date(datetime.now().date().strftime('%d.%m.%Y'))
            bot_response = f"alerts list for {datetime.now().date().strftime('%d.%m.%Y')}:\n\n" + make_pretty_alerts(alerts)
    else:
        if "-" in without_command:
            separated = without_command.split("-")
            try:
                date_1, date_2 = datetime.strptime(separated[0], '%d.%m.%Y'), datetime.strptime(separated[1], '%d.%m.%Y')
                alerts = get_alerts_by_period(date_1, date_2)
                if file_indicator:
                    file_name += f"{date_1.strftime('%d.%m.%Y')}-{date_2.strftime('%d.%m.%Y')}.xlsx"
                    file = open(file_name, 'w+')
                    file.close()
                    writer = pd.ExcelWriter(file_name, engine='xlsxwriter')
                    try:
                        output = create_file_alerts_by_period(date_1, date_2)
                        print(output)
                        data = pd.DataFrame(output)
                        data.to_excel(writer, 'Sheet1')
                        writer.close()
                        bot_response = f"created a file named\n`{file_name}`"
                    except Exception as e:
                        print(e)
                        bot_response = "something goes wrong..."
                else:
                    bot_response = f"alerts for {date_1.strftime('%d.%m.%Y')}-{date_2.strftime('%d.%m.%Y')}:\n\n" + make_pretty_alerts(alerts)
            except Exception as e:
                bot_response = "invalid input data"
                print(e)
        else:
            try:
                date = datetime.strptime(without_command, '%d.%m.%Y')
                alerts = get_alerts_by_date(date)
                if file_indicator:
                    file_name += f"{date.strftime('%d.%m.%Y')}.xlsx"
                    file = open(file_name, 'w+')
                    file.close()
                    writer = pd.ExcelWriter(file_name, engine='xlsxwriter')
                    data = pd.DataFrame(create_file_alerts_by_date(date))
                    data.to_excel(writer, 'Sheet1')
                    writer.close()
                    bot_response = f"created a file named\n`{file_name}`"
                else:
                    bot_response = f"alerts for {date.strftime('%d.%m.%Y')}:\n\n" + make_pretty_alerts(alerts)
            except Exception as e:
                # bot.send_sticker(message.chat.id, stickers.STICKER_SAD, reply_to_message_id=message.id)
                bot_response = "invalid input data"
                print(e)
    return bot_response


def ip_bot(input_text: str) -> str:
    bot_response = ""
    input_text = remove_nickname(input_text)
    without_command = remove_command(input_text)
    try:
        ip_address = parse_ip(input_text)
        if ip_address:
            if is_valid(ip_address):
                record = get_ip(ip_address)
                if not record:
                    try:
                        geoip = get_geo_ip(ip_address)
                        country_code, country_name = geoip["country_code"], geoip["country_name"]
                    except Exception as e:
                        country_code, country_name = "UNDEFINED"
                    try:
                        bot_response = f"IP is not banned ✅\ncountry: {flag.flag(country_code)} {country_name}"
                    except ValueError:
                        bot_response = "IP is not banned ✅\ncountry: 📺look like a local IP"
                else:
                    ip_address = record[0][1].split("/")[0]
                    ban_reason = record[0][2]
                    source = record[0][3]
                    ban_author = record[0][4]
                    ban_date = datetime.date(record[0][5]).strftime("%d.%m.%Y")
                    response = f"banned ❌\nip: `{ip_address}`\n"
                    try:
                        geoip = get_geo_ip(ip_address)
                        country_code, country_name = geoip["country_code"], geoip["country_name"]
                        response += f"country: {flag.flag(country_code)} {country_name}\n"
                    except Exception as e:
                        print(e)
                        response += f"country: look like a local IP 📺\n"
                    finally:
                        if ban_reason != "":
                            response += f"ban_reason: {ban_reason}\n"
                        if source != "":
                            response += f"source: {source}\n"
                        response += f"ban_date: {ban_date}\nban_author: @{ban_author}"
                        bot_response = make_shield(response)
            else:
                bot_response = "invalid input data"
        else:
            file_indicator = False
            if "/file" in without_command:
                without_command = without_command.split("/file")[0]
                file_indicator = True
                file_name = settings.FILE_PATH + f"Banned_IPs_"
            if not without_command:
                banned_ips = get_ip_today()
                if file_indicator:
                    file_name += f"{str(datetime.now().strftime('%d.%m.%Y'))}.xlsx"
                    file = open(file_name, 'w+')
                    file.close()
                    writer = pd.ExcelWriter(file_name, engine='xlsxwriter')
                    data = pd.DataFrame(create_file_ip_by_date(datetime.now().date()))
                    data.to_excel(writer, 'Sheet1')
                    writer.close()
                    bot_response = f"created a file named\n`{file_name}`"
                else:
                    if banned_ips:
                        bot_response = f"banned IPs for {datetime.now().date().strftime('%d.%m.%Y')}:\n\n" + "\n".join(f"`{str(banned_address)}`" for banned_address in banned_ips)
                    else:
                        bot_response = "there is no data"
                # bot.send_sticker(message.chat.id, stickers.STICKER_SAD, reply_to_message_id=message.id)
            else:
                if "-" in without_command:
                    separated = without_command.split("-")
                    try:
                        date_1, date_2 = separated[0], separated[1]
                        banned_ips = get_ip_by_period(date_1, date_2)
                        if file_indicator:
                            file_name += f"{date_1}-{date_2}.xlsx"
                            file = open(file_name, 'w+')
                            file.close()
                            writer = pd.ExcelWriter(file_name, engine='xlsxwriter')
                            data = pd.DataFrame(create_file_ip_by_period(date_1, date_2))
                            data.to_excel(writer, 'Sheet1')
                            writer.close()
                            bot_response = f"created a file named\n`{file_name}`"
                        else:
                            if banned_ips:
                                bot_response = f"banned IPs for {date_1}-{date_2}:\n\n" + "\n".join(f"`{str(banned_address)}`" for banned_address in banned_ips)
                            else:
                                bot_response = "there is no data"
                    except Exception as e:
                        bot_response = "invalid input data"
                        print(e)
                else:
                    try:
                        if file_indicator:
                            file_name += f"{without_command}.xlsx"
                            file = open(file_name, 'w+')
                            file.close()
                            writer = pd.ExcelWriter(file_name, engine='xlsxwriter')
                            data = pd.DataFrame(create_file_ip_by_date(without_command))
                            data.to_excel(writer, 'Sheet1')
                            writer.close()
                            bot_response = f"created a file named:\n `{file_name}`"
                        else:
                            bot_response += f"banned IPs for {without_command}:\n\n"
                            banned_ips = get_ip_by_date(get_pretty_date(without_command))
                            if banned_ips:
                                bot_response += "\n".join(f"`{str(banned_address)}`" for banned_address in banned_ips)
                            else:
                                bot_response = "there is no data"
                    except Exception as e:
                        bot_response = "invalid input data"
                        print(e)
    except Exception as e:
        bot_response = e
    return bot_response


def unban_bot(input_text: str) -> str:
    bot_response = ""
    input_text = remove_nickname(input_text)
    splitted_text = input_text.split("\n")
    for record in splitted_text:
        response = ""
        ip_address = parse_ip(record)
        try:
            if is_valid(ip_address):
                ok = remove_ip(ip_address)
                if ok:
                    response = f"`{ip_address}` - successfully unbanned"
                else:
                    response = f"`{ip_address}` - is not banned"
            else:
                response = f"`{ip_address}` - invalid input data"
        except Exception as e:
            response = f"`{ip_address}` - invalid input data"
            print(e)
        finally:
            bot_response += (response + "\n")
    return bot_response
