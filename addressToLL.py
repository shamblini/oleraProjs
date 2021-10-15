import requests

# Turns string address into web address format
def formatAddy(address):
    address = address.replace(" ", "%20")
    address = address.replace(",", "%2C")
    return address

# Returns the lat and longitude of the current address
# Powered by latlong.net's API
def getLatLong(address):
    formatted = formatAddy(address)
    url = "https://www.latlong.net/_spm4.php"

    # EDIT to change address. Needs to be in web address format (%20 = ' ', etc.)
    payload='c1='+formatted+'&action=gpcm&cp='

    headers = {
        'authority': 'www.latlong.net',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
        'content-type': 'application/x-www-form-urlencoded',
        'x-requested-with': 'XMLHttpRequest',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
        'sec-ch-ua-platform': '"Windows"',
        'accept': '*/*',
        'origin': 'https://www.latlong.net',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.latlong.net/convert-address-to-lat-long.html',
        'accept-language': 'en-US,en;q=0.9',                                         # This is what caused error last time 
        'cookie': '_ga=GA1.2.721979643.1634146345; _gid=GA1.2.1556143895.1634146345; PHPSESSID=4eq0n9v9iou9bdtsneo2401gr1; OptanonConsent=isIABGlobal=false&datestamp=Thu+Oct+14+2021+13%3A07%3A40+GMT-0500+(Central+Daylight+Time)&version=6.14.0&hosts=&landingPath=NotLandingPage&groups=C0003%3A1%2CC0004%3A1%2CC0002%3A1%2CC0001%3A1&AwaitingReconsent=false&geolocation=US%3BTX; OptanonAlertBoxClosed=2021-10-14T18:07:40.423Z'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    #print(response.text)
    return(response.text)