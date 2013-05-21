
import sys
import urllib
import pprint
from BeautifulSoup import BeautifulSoup

MAX_NAME_LENGTH = 16

SUFFIXES = {
    "ad": ["ad"],
    "as": ["as", "az"],
    "bz": ["bz", "bs"],
    "cc": ["cc", "ck"],
    "cd": ["cd", "cid"],
    "co": ["co", "ko"],
    "dj": ["dj", "dge", "dage", "dege", "dige", "duge"],
    "fm": ["fm", "fam", "pham", "phm"],
    "io": ["io", "yo"],
    "la": ["la", "lay"],
    "me": ["me"],
    "ms": ["ms"],
    "nu": ["nu", "new", "noo"],
    "sc": ["sc", "sk"],
    "sr": ["sr", "sir", "ser", "swer", "cer"],
    "su": ["su", "soo"],
    "tv": ["tv", "tiv", "tive"],
    "tk": ["tk", "tic", "tick"],
    "ws": ["ws", "wse"]
}

term = sys.argv[1]

def searchOnelook(suffix, term):
    onelookUrl = "http://onelook.com/?w=*" + suffix + "%3A" + term
    f = urllib.urlopen(onelookUrl)
    onelookHtml = f.read()
    f.close()
    onelookParsed = BeautifulSoup(onelookHtml)
    try:
        anchors = onelookParsed.findAll("table")[3].findAll("a")
    except:
        print "OneLook FAIL: " + onelookUrl
        return []
    results = []
    for a in anchors:
        try:
            text = str(a.text)
        except:
            print "FAIL:  " + a.text
            continue 
        results.append(text)
    return results


def domainAvailable(domain):
    url = "http://" + domain
    print "domainAvailable called on: " + url
    return False
    try:
        f = urllib.urlopen(url)
        response = f.read()
        f.close()
        print url + ": " + "RESPONSE"
        return False
    except:
        print url + ": " + "no response"
        return True

def constructName(phrase):
    spaceless = phrase.replace(" ", "").replace("-", "").replace(",", "").replace("'", "")
    name = {
        "name": phrase,
        "spaceless": spaceless,
        "length": len(phrase),
        "shortDomain": spaceless[0:-2] + "." + spaceless[-2:],
        "comDomain": spaceless + ".com"
    }
    name["shortDomainAvailable"] = domainAvailable(name["shortDomain"])
    name["comDomainAvailable"] = domainAvailable(name["comDomain"])
    return name


domainsAvailable = []
domainsNotAvailable = []
#for suffix in [SUFFIXES["co"], SUFFIXES["tk"]]:
for suffix, suffixSounds in SUFFIXES.items():
    for suffixSound in suffixSounds:
        print "--- suffixSound: " + suffixSound
        onelook = searchOnelook(suffixSound, term)
        for phrase in onelook[0:50]:
            if (len(phrase) < MAX_NAME_LENGTH):
                name = constructName(phrase[0:0-len(suffixSound)] + suffix)
                if name["shortDomainAvailable"] and name["comDomainAvailable"]:
                    domainsAvailable.append(name)
                else:
                    domainsNotAvailable.append(name)

domainsAvailable.sort(key=lambda x: x[u"length"])
domainsNotAvailable.sort(key=lambda x: x[u"length"])
pprint.pprint([domain["shortDomain"] for domain in domainsAvailable])
