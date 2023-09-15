import random
import requests
import utils
import urllib3
import base64
import urllib.parse
import re


# domain=["https://google.com/","https://bugcrowd.com/"]
domain=open("all-domains.txt","r",encoding="utf8").read().split("\n")
match = [ "'HIT", "'hit" ]
params=["/cahceeee.css","/cahceeee.js","/cahceeee.avif","/cahceeee.png","/cahceeee.pdf"]
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def request(domain):
    try:
        for param in params:
                for i in range(8):
                    res=requests.get(f"https://www.{domain}{param}",allow_redirects=True)
                    headers = res.headers
                    if any(re.search(x, str(res.headers)) for x in match):
                        print("bug")
                        file = open("Bugs.txt","a")
                        file.write(f"{res.url}\n    Response-Headers: {res.headers}\n\n\n\n\n\n\n\n")
                        print(f"\n{utils.GREEN_CHAR}Bug found:{res.url}")
                    else:
                        pass
                        
    except Exception as e:
                pass


if __name__ == '__main__':
    utils.multithread(request,utils.parse_multithread_args(domain),60,progress_title='Testing for Dependency Confusion')
