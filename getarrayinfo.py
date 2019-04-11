import sys
import warnings
import purestorage
from hpe3parclient import client, exceptions
import urllib3
from datetime import date

# disable annoying output
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) # hide insecure https query
warnings.filterwarnings("ignore", category=DeprecationWarning) 

# pure part

PUREARRAYS=[{'name':<name>, 'apitoken':<apitoken>},{'name': , 'apitoken': },...]
PUREARRAYDATA=[]

def getArrayInfo():

    for array in PUREARRAYS:
        ARRAY = array['name']
        API_TOKEN = array['apitoken']

        # Connect to the Array
        try:
            array = purestorage.FlashArray(ARRAY, api_token=API_TOKEN)
        except purestorage.PureError:
            print(e)
            print("PureError Unable to connect to the pure array: " + ARRAY)
            sys.exit(1)
        except Exception as e:
            print(e)
            print('Exception - Unable to connect to the pure array: ', ARRAY)
            sys.exit(1)

        arrayInfo = array.get()
        arrayName = arrayInfo['array_name']
        arrayOSVersion = arrayInfo['version']
        arrayRevision = arrayInfo['revision']
        PUREINFO = {'name':arrayName,'osversion':arrayOSVersion,'revision':arrayRevision}

        PUREARRAYDATA.append(PUREINFO)

        # close the REST session
        array.invalidate_cookie()

getArrayInfo()

#3par part 

HPARRAYS = [<dns hostnames of arrays>]
USERNAME = <userid>
PASSWORD = <PWD>
HPEARRAYDATA = []
for hparray in HPARRAYS:
    ARRAYNAME = hparray
    def run_command(array_name, command):
        try:
            hp_client.ssh.open()
            outputList = hp_client.ssh.run(command)
            hp_client.ssh.close()
            return outputList
        except Exception as e:
            print('Unable to connect to array (SSH)')
            print(e)
            sys.exit(1)


    def get_arrayinfo(array_name):
        try:
            hparrayinfo = hp_client.getStorageSystemInfo()
        except Exception as e:
            print('Unable to get system info')
            print(e)
            sys.exit(1)
        
        #print(hparrayinfo['name'] + hparrayinfo['systemVersion'] + hparrayinfo['patches'])
        HPEARRAYINFO = {'name' : hparrayinfo['name'],'osversion' : hparrayinfo['systemVersion'], 'revision' : hparrayinfo['patches'] }
        HPEARRAYDATA.append(HPEARRAYINFO)
        
    # this creates the client object and sets the url to the 3PAR server
    try:
        hp_client = client.HPE3ParClient("http://" + ARRAYNAME + ":8008/api/v1")
        hp_client.login(USERNAME, PASSWORD)
    except Exception as e:
        print('Unable to connect to array (http)')
        sys.exit(1)

    # Set the SSH authentication options for the SSH based calls.
    hp_client.setSSHOptions(ARRAYNAME, USERNAME, PASSWORD)


    get_arrayinfo(ARRAYNAME) 
    

    # kill session
    hp_client.logout()


ARRAYDATA = []
for item in PUREARRAYDATA:
    ARRAYDATA.append(item)

for item in HPEARRAYDATA:
    ARRAYDATA.append(item)

i = len(ARRAYDATA)

html = '<div class="table-wrap"><table class="confluenceTable"><tbody><tr><th class="confluenceTh">Array</th><th class="confluenceTh">OS version</th><th class="confluenceTh">Revision/ Patches</th></tr>'

for x in range(0,i):
    html = html + '<tr><td class="confluenceTd">' + ARRAYDATA[x]['name'] + '</td> <td class="confluenceTd">' + ARRAYDATA[x]['osversion'] + '</td><td class="confluenceTd">' + ARRAYDATA[x]['revision'] + '</td></tr>'

html = html + '</tbody></table></div>'
 
today = date.today()

f= open("arrayinfo"+str(today) + ".txt","w+")
f.write(html)
f.close 