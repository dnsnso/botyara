import re


remove_nickname_re = re.compile(r'\D{1,}[@][^\s]{1,}')
ip_address_re = r'[0-9]+(?:\.[0-9]+){3}'
remove_command_re = re.compile(r'^\x2F[^\s]{1,}')
parse_ip_re = re.compile(r'[0-9]+(?:\.[0-9]+){3}')