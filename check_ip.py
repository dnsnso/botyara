import ipaddress

from config import subnets


def is_our(ip: str) -> bool:
    ip_address = ipaddress.ip_address(ip)

    if ip_address in ipaddress.ip_network(subnets.SUBNET_1) or \
        ip_address in ipaddress.ip_network(subnets.SUBNET_2) or \
          ip_address in ipaddress.ip_network(subnets.SUBNET_3) or \
            ip_address in ipaddress.ip_network(subnets.SUBNET_4) or \
              ip_address in ipaddress.ip_network(subnets.SUBNET_5) or \
                ip_address in ipaddress.ip_network(subnets.SUBNET_6) or \
                  ip_address in ipaddress.ip_network(subnets.SUBNET_7) or \
                    ip_address in ipaddress.ip_network(subnets.SUBNET_8) or \
                      ip_address in ipaddress.ip_network(subnets.SUBNET_9) or \
                        ip_address in ipaddress.ip_network(subnets.SUBNET_10) or \
                          ip_address in ipaddress.ip_network(subnets.SUBNET_11) or \
                            ip_address in ipaddress.ip_network(subnets.SUBNET_12) or \
                              ip_address in ipaddress.ip_network(subnets.SUBNET_13) or \
                                ip_address in ipaddress.ip_network(subnets.SUBNET_14) or \
                                  ip_address in ipaddress.ip_network(subnets.SUBNET_15) or \
                                    ip_address in ipaddress.ip_network(subnets.SUBNET_16) or \
                                      ip_address in ipaddress.ip_network(subnets.SUBNET_17) or \
                                        ip_address in ipaddress.ip_network(subnets.SUBNET_18) or \
                                          ip_address in ipaddress.ip_network(subnets.SUBNET_19) or \
                                            ip_address in ipaddress.ip_network(subnets.SUBNET_20) or \
                                              ip_address in ipaddress.ip_network(subnets.SUBNET_21) or \
                                                ip_address in ipaddress.ip_network(subnets.SUBNET_22) or \
                                                  ip_address in ipaddress.ip_network(subnets.SUBNET_23) or \
                                                    ip_address in ipaddress.ip_network(subnets.SUBNET_24) or \
                                                      ip_address in ipaddress.ip_network(subnets.SUBNET_25):
        return True
    return False


def is_local(ip: str) -> bool:
    ip_address = ipaddress.ip_address(ip)

    if ip_address in ipaddress.ip_network(subnets.LOCAL_SUBNET_1) or \
         ip_address in ipaddress.ip_network(subnets.LOCAL_SUBNET_2) or \
           ip_address in ipaddress.ip_network(subnets.LOCAL_SUBNET_3) or \
             ip_address in ipaddress.ip_network(subnets.VIPNET_SUBNET) or \
               ip_address == ipaddress.ip_address(subnets.LOCALHOST):
        return True
    return False


def is_valid(ip_address: str) -> bool:
    try:
        ipaddress.ip_address(ip_address)
        return True
    except ValueError:
        return False
