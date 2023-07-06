import os

from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())


class Settings:
    TELEGRAM_TOKEN: str = os.getenv("TELEGRAM_API_KEY")
    GEOIP_TOKEN: str = os.getenv("GEOIP_TOKEN")
    FILE_PATH: str = os.getenv("FILE_PATH")
    CONTACT_NICKNAME: str = os.getenv("CONTACT_NICKNAME")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB")
    DB_DRIVER: str = os.getenv("DB_DRIVER")


class Stickers:
    STICKER_CRY: str = os.getenv("STICKER_CRY")
    STICKER_DURKA: str = os.getenv("STICKER_DURKA")
    STICKER_GENIALNO: str = os.getenv("STICKER_GENIALNO")
    STICKER_LADNO: str = os.getenv("STICKER_LADNO")
    STICKER_PUTIN: str = os.getenv("STICKER_PUTIN")
    STICKER_KIT_NAH: str = os.getenv("STICKER_KIT_NAH")
    STICKER_PESIK: str = os.getenv("STICKER_PESIK")
    STICKER_CHEL: str = os.getenv("STICKER_CHEL")
    STICKER_NAH: str = os.getenv("STICKER_NAH")
    STICKER_SAD: str = os.getenv("STICKER_SAD")
    STICKER_EPIC_SAD: str = os.getenv("STICKER_EPIC_SAD")


class Subnets:
    SUBNET_1: str = os.getenv("SUBNET_1")
    SUBNET_2: str = os.getenv("SUBNET_2")
    SUBNET_3: str = os.getenv("SUBNET_3")
    SUBNET_4: str = os.getenv("SUBNET_4")
    SUBNET_5: str = os.getenv("SUBNET_5")
    SUBNET_6: str = os.getenv("SUBNET_6")
    SUBNET_7: str = os.getenv("SUBNET_7")
    SUBNET_8: str = os.getenv("SUBNET_8")
    SUBNET_9: str = os.getenv("SUBNET_9")
    SUBNET_10: str = os.getenv("SUBNET_10")
    SUBNET_11: str = os.getenv("SUBNET_11")
    SUBNET_12: str = os.getenv("SUBNET_12")
    SUBNET_13: str = os.getenv("SUBNET_13")
    SUBNET_14: str = os.getenv("SUBNET_14")
    SUBNET_15: str = os.getenv("SUBNET_15")
    SUBNET_16: str = os.getenv("SUBNET_16")
    SUBNET_17: str = os.getenv("SUBNET_17")
    SUBNET_18: str = os.getenv("SUBNET_18")
    SUBNET_19: str = os.getenv("SUBNET_19")
    SUBNET_20: str = os.getenv("SUBNET_20")
    SUBNET_21: str = os.getenv("SUBNET_21")
    SUBNET_22: str = os.getenv("SUBNET_22")
    SUBNET_23: str = os.getenv("SUBNET_23")
    SUBNET_24: str = os.getenv("SUBNET_24")
    SUBNET_25: str = os.getenv("SUBNET_25")
    VIPNET_SUBNET: str = os.getenv("VIPNET_SUBNET")
    LOCAL_SUBNET_1: str = os.getenv("LOCAL_SUBNET_1")
    LOCAL_SUBNET_2: str = os.getenv("LOCAL_SUBNET_2")
    LOCAL_SUBNET_3: str = os.getenv("LOCAL_SUBNET_3")
    LOCALHOST: str = os.getenv("LOCALHOST")


stickers = Stickers()

settings = Settings()

subnets = Subnets()
