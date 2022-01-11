import requests
import json
from random import randrange

####################
#CHANGE THESE VALUES
####################
# The percentage you'd see before deciding to reset blocks manually
#   Example: resyncPercentage = 85
resyncPercentage = " <percentage> "

#Your SN pulled from status.sensecapmx.cloud
#   Example: sn = "1109913352197400130"
sn = " <your sn> "

#Your api key pulled from status.sensecapmx.cloud (the accounts menu on the left)
#   Example: status_api_key = "yutjc63detim1dcsn2tbc6vp6783jj2afdrqutpzxa6ks8xe8"
status_api_key = " <your key> "

#Your api key pulled from the miner's dashboard after entering the CPU ID to log in
#   Example: miner_api_key = "7bb44b508d30bvd57e209aaaab37444bdf5615xd726fbbe694f83573efd3a64c1"
miner_api_key = " <your key> "

#Your miner's private IP address
#   Example: miner_private_ip = "192.168.1.52"
miner_private_ip = " <your miner's IP> "

####################



def main():

    # SenseCAP API URL construction
    api_host = "https://status.sensecapmx.cloud/"
    api_path = "/api/openapi/device/view_device"
    requrl = api_host + api_path + "?sn=" + sn + "&api_key=" + status_api_key

    # Creates a list of browser User Agents to prevent rate limiting from some APIs
    try:
        fakeUA = requests.get(url="https://fake-useragent.herokuapp.com/browsers/0.1.11").text
        f = open("fakeUserAgents", "w")
        f.write(fakeUA)
    except:
        f = open("fakeUserAgents", "r")
        fakeUA = f.read()
    f.close
    fakeUA = json.loads(fakeUA)['browsers']['chrome'][randrange(1, 40)]

    # Send the request to pull SD card usage
    r = requests.get(url=requrl, headers={'User-agent': fakeUA})
    apiData=r.text
    print (apiData)
    sdTotal = json.loads(apiData)["data"]["sdTotal"]
    sdUsed = json.loads(apiData)["data"]["sdUsed"]

    # Calculate usage
    percentageUsed = 100*float(sdUsed)/float(sdTotal)
    print ("SD percentage used: " + str(percentageUsed))

    # Reset blocks if above user-defined threshold
    if (percentageUsed > resyncPercentage):
        print ("Resetting...")
        url = "http://" + miner_private_ip +"/resetblocks"
        header = {"Authorization" : "Basic "+miner_api_key}
        r = requests.post(url, headers=header)
    else:
        print ("All good")

if __name__ == "__main__":
    try:
        main()
    except:
        print ("Error pulling data from API. Check connetion or try again later.")
