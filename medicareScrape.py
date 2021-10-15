import requests
import json
import pandas as pd
import os
import re
from addressToLL import getLatLong

# TODO
# Mess around with locations/ clean up the csv

def main():

    # EDIT ADDRESS TO GET CSV OF ALL NEARBY NURSING HOMES
    # ===================================================
    address = "tuscola, TX"

    # Collects the latitude/longitude coordinates from given address
    latLong = getLatLong(address)
    latLong = re.findall(r"[-+]?\d*\.\d+|\d+", latLong)
    latLong = [float(i) for i in latLong]
    print(latLong)  # Display coords (debugging)

    data = get_json(latLong)   # Raw .JSON file
    save_to_csv(data.get('results'))

# Returns a json file from data provided by the request to the API
def get_json(coords): 
    url = "https://www.medicare.gov/api/care-compare/provider"

    # Request body/paylod
    # CHANGE, provides new data based on geolocation (Latitude/Longitude)
    payload = json.dumps({
        "type": "NursingHome",
        "filters": {
            "radiusSearch": {
            "coordinates": {
                "lon": coords[1],      # Currently, can only change location via lon and lat coordinates
                "lat": coords[0]       # This is because medicare.gov is powered by smartystreets
            },
            "radius": 50               # Increase/decrease to expand searching area
            }
        },
        "page": 1,
        "limit": 100,                  # Results per page (keep 100, easy to make big csv)
        "returnAllResults": True,
        "sort": [
            "closest",
            "rank",
            "alpha"
        ]
    })

    # Request Headers
    # DO NOT CHANGE
    headers = {
        'authority': 'www.medicare.gov',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
        'accept': 'application/json, text/plain, */*',
        'content-type': 'application/json',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
        'sec-ch-ua-platform': '"Windows"',
        'origin': 'https://www.medicare.gov',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.medicare.gov/care-compare',
        'accept-language': 'en-US,en;q=0.9',
        'cookie': 'optimizelyEndUserId=1cf80a178c0b000093f15d61a8010000a8020000; _cb_ls=1; _cb=D3I2ORDmK8M7Cf9Tdb; QuantumMetricUserID=3fd5b4cd735b526f481bba687a41dea1; QSI_SI_3e0OfIJ37DZYJ6Z_intercept=true; bamCHTutorial=true; _gcl_au=1.1.1624367411.1633559541; _gid=GA1.2.1905952758.1633976921; CONSENTMGR=c1:1%7Cc2:1%7Cc3:1%7Cc4:1%7Cc5:1%7Cc6:1%7Cc7:1%7Cc8:1%7Cc9:1%7Cc10:1%7Cc11:1%7Cc12:1%7Cc13:1%7Cc14:1%7Cc15:1%7Cts:1633977195874%7Cconsent:true; _abck=2997C74ED9F8AE34CBF5C07FAA1617A6~0~YAAQQI7cQ0NJ13h8AQAAVtC0egaT5xqVKYdLylKMU/SKX55E+xczj6Wl7/1fCzUKANXRrRVYIkOA5XttF2eF0pUG92dnL6wLI0VDDt6jwO6tZnOp9OMApx7kP0L5PakJ3WtwFKAioDTAjMfSFfMjDrFTaI90b5q6iZ8TF5ylcm8YDTHrlB7JWVQLoYo1ENWTlw9V+xS9CeaQRXnqgChxt0DYVMxzUguaF3w/GlSXkmAeZfYfBRqelmWYQVFCZ+qRL3fdQWeWNaK7Dc1rVEmd3fAoTrzaoDIdGWMx912JJeJ0HAZDNHq1ycYRqZXFWv/2beP9csmedSxmiHS3LEu9+2imL503WeKIUy2C4+oTI9Wtb1gP2PLIo7XBC01uI/ksz8z7nkrdzJIof89jJf0QmGam5/+azG1+3bk=~-1~-1~-1; bm_sz=496BFA0D80883F9699682D6E877DEDFD~YAAQQI7cQ0RJ13h8AQAAVtC0eg1NhlSX8dejfQvzhxnFUIuKs2H4mu7AmG481JXGgr27VFcxAVkcU+c15bhICBIEYmJluSEQVwW6KalkQ6+eVdYe0CNs/lFcoTe1Klq99yy7snqVQkIjD/vJxK7uRGSvw8hQTzR2EdKtXT4ssWhuSEFsNkuBDDpD/GaEmz8ZgVHqHTwXiUHDpBPrQDUSk3/oacHhJGtHApm48O+4PxspXolHd2veVupVi2VUagcmXJVMtFTL/SwoMTdLDtlPYXrqb+6BK9ri3DHe14xKKBd56nfKJg==~4277318~3618371; ak_bmsc=8C38A18C089C153BD9A04A5AA546D4FA~000000000000000000000000000000~YAAQQI7cQ0xJ13h8AQAAfNC0eg2F7p4Xs6+UThFHU47gKWrP8BnL/uPqd5M27RD+8HlSb7QKuIA6P94mqU+6a7falHiioPpo6baz9ETeBJnIl1BPIVUXH5RW/LNgS+J8OWClP/4ZCMWHZ6Wg5vJ21mZsEoWjio4GloKYZvstZqvcamLf+I3uBtxtMZbEUtoML81JuDtWlYrKM0ZIOekVc8N1tmJH1PNr10pDHhGjf5Rue/TDI27zhcNhhRA/raz2NnKHRC2zn/7RfaYFO9+0Pt55B2CGDf4Pq1W+DmVabPRjjIZVcErPqcDo9ZamVZdPlxBkxOF2dwu5F0YHQSeV37x8yuh75XUBaNF9npDLYkySD3+FP0dHOaZLBHQaWDK57gDal/JVj9TRj/NT; _chartbeat2=.1633546643079.1634146242523.11010111.D7BWnJDpzXuJCv7uPcDcQnXNDDH3sg.1; _cb_svref=null; _gat=1; _gat_GSA_ENOR0=1; _ga=GA1.1.1513042276.1633546643; QuantumMetricSessionID=0e97a8a8c668b03b914d7a172917d2a9; QSI_HistorySession=https%3A%2F%2Fwww.medicare.gov%2Fcare-compare%2Fresults%3FsearchType%3DNursingHome%26page%3D1%26city%3DCollege%2520Station%26state%3DTX%26zipcode%3D77840%26radius%3D25%26sort%3Dclosest~1634146242896; _ga_QCS12ML6QJ=GS1.1.1634146242.14.0.1634146253.0; _chartbeat4=t=BLof5MCBGxhNDPI8pFDQLp5FCLRhfk&E=1&x=0&c=0.18&y=3555&w=969; utag_main=v_id:017c56f7a40e001031b2ab9dee0b05072002606a00bd0$_sn:15$_se:2$_ss:0$_st:1634148053850$dc_visit:15$ses_id:1634146241938%3Bexp-session$_pn:2%3Bexp-session$dc_event:1%3Bexp-session$dc_region:us-east-1%3Bexp-session; akavpau_default=1634146555~id=d9a7d9d29f08f67a969432b1054f1448; bm_sv=FA9D19449B2DBE27532D4EC53022A178~nwTNoY4sVLlJf9akWa961gZVkAJx4RRl1CsMnTQvw/ajcC6yJmKnEHGnKySRksprGwsIjxrVhDgwzEG1D44Z5Uos3/aLDpgBvWbdaPHiyHsE/i7P3GgnCsf9rivu9HgEnPWL3aSjo2pyNifOS3xoLr5ci4cfaLgSZD3nMsMyZdg=; _abck=2997C74ED9F8AE34CBF5C07FAA1617A6~-1~YAAQPY7cQ2oH1Hp8AQAAa//gegaCeLAlLMtW1Q/mfMdPX7a7OA+HrikyYwWARzl8uy0gt3Jc9HFQdXSxT8ImXEvZhuiGhhHrNa+eiMFY+XrPQ72mG3WxLBNrgFaAoluizjAODbx+cq3TQ5mowHhE03CgqzwbCzUKrO7/jRP2ji2qalrWEhXz0gQE79fM/nS1/As+beoBRgH/yGPp2yzR6o2sdqjfnUwiJ4wjE6xq+4sOsft8PqF7jogYQLUBcy01dKCRrsvgkIkmAcbE/roeUgm3OUMZcBAuSp2PZv6vzIhtp6mr9NOPR0wMpdV2kPoSAEOmfqvPin1UjyIcyf76W64GNdMoHb9n/b1IgvJ3k11NlCiOFsqSSA8hALassXQn90+SJ3BssA36uT+EKSUlEYfq5J/3wl5WzZA=~0~-1~-1; _ga=GA1.1.1513042276.1633546643; bm_sv=FA9D19449B2DBE27532D4EC53022A178~nwTNoY4sVLlJf9akWa961gZVkAJx4RRl1CsMnTQvw/ajcC6yJmKnEHGnKySRksprGwsIjxrVhDgwzEG1D44Z5Uos3/aLDpgBvWbdaPHiyHt4aMe+07NKINwjHhvNnSUgnV+gwnhbB9FvL80n9YhGpswrzUATRnsGCZp67zPRdSU=; optimizelyEndUserId=1cf80a178c0b000093f15d61a8010000a8020000; akavpau_default=1634149438~id=29790089272d7c209ed4b1f7955fb18b'
    }

    response = requests.request("POST", url, headers=headers, data=payload) # Sends a POST request to the API, providing the necessary request headers and payload
                                                                            # Is it a RESTful API ??

    return response.json()

# Creates CSV file from collected data
def save_to_csv(data):
    if data:
        dataFrame = pd.json_normalize(data) # Turns JSON into a Panda data frame (normalize) then transfers data frame to CSV format

        # Selects certain fields from the df. See data.csv in medicareData for all fields
        newFrame = dataFrame.filter(['distance','name','nursingHome.addressLine1','nursingHome.addressCity','nursingHome.addressState',
                                     'nursingHome.addressZipcode','nursingHome.phone','nursingHome.overallRating'],axis=1)

        path = 'C:\\Users\\bamblini\\Desktop\\Coding\\Python\\scrape1\\scraper\\medicareData'
        newFrame.to_csv(os.path.join(path,"temp.csv"))        # Because Pandas are used, for multiple pages of data we can concatinate csv into one, or simply edit original df
        print('Went to CSV')

if __name__ == '__main__':  # Runs Main
    main()

# Use PostMan to provide code that sends request to API 
# https://www.youtube.com/watch?v=ThKiZjLNN8Y