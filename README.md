# About The Project
Telegram bot to track blocking of IP addresses, as well as security incidents.

## Description

Allows you to track the state of the address, check the country of origin, export to a file, sort by date.
When working with security incidents, it allows you to track the status, sort by date, and also export to a file.

## Getting Started

### Dependencies

Can be run on any system as long as it is compatible with the libraries described in file
  ```sh
  requirements.txt
  ```

### Installing



### Executing program

1. Get a free API Key for your telegram bot at [@BotFather](https://t.me/botfather)
2. Clone the repo
   ```sh
   git clone https://github.com/dnsnso/botyara/
   ```
3. Install Python packages
   ```sh
   pip install -r requirements.txt
   ```
4. Enter your Telegram Bot API in `.env`
   ```sh
   TELEGRAM_API_KEY = 'ENTER YOUR TELEGRAM BOT API'
   ```
5. Get a free API Key for your geoip account at [ipinfo.io](https://ipinfo.io/)
6. Enter your Geo IP token `.env`
   ```sh
   GEOIP_TOKEN = 'ENTER YOUR GEO IP'
   ```

## Authors

* n1ck
* dns@nso.ru

## Version History

* 1.0
    * Initial release

## License

This project is licensed under the GPL-3.0 License - see the LICENSE.md file for details
