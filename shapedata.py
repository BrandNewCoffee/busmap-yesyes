import json
import requests
import time
access_token="eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJER2lKNFE5bFg4WldFajlNNEE2amFVNm9JOGJVQ3RYWGV6OFdZVzh3ZkhrIn0.eyJleHAiOjE3NzMzMTUyMDksImlhdCI6MTc3MzIyODgwOSwianRpIjoiMDc5OWEyYmItNzlhNy00MjUxLTlkYTEtYzRiMTJmMjNjMWNlIiwiaXNzIjoiaHR0cHM6Ly90ZHgudHJhbnNwb3J0ZGF0YS50dy9hdXRoL3JlYWxtcy9URFhDb25uZWN0Iiwic3ViIjoiNDQzOTdjOWEtZGFkNC00MjNkLTk0YzAtNWI5ODllN2FkZDZkIiwidHlwIjoiQmVhcmVyIiwiYXpwIjoiMzEwNzU4LWYwYjJlMTA2LWEyNzUtNGU2NiIsImFjciI6IjEiLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsic3RhdGlzdGljIiwicHJlbWl1bSIsInBhcmtpbmdGZWUiLCJtYWFzIiwiYWR2YW5jZWQiLCJnZW9pbmZvIiwidmFsaWRhdG9yIiwidG91cmlzbSIsImhpc3RvcmljYWwiLCJjd2EiLCJiYXNpYyJdfSwic2NvcGUiOiJwcm9maWxlIGVtYWlsIiwidXNlciI6ImY1ZWUzNjE5In0.PhzrZpkQIy_mVfo2EsHnYRSJzwk_H4bWfS1x0Z_R2vHJNelCpmws8lnOd7oEKW0_7LPLai_mZjdp_H6kTQ8A9JBJrHSsc4dtF_5GlUPjbdpHl7USir4VI_dhIJuEIcGleFjukY3riadY8qhZSIRxXvi7qboUVVHflbOen8toDvViaMatD2HEBbOr31NIvT8onRA9jLUcZwTGqPKlLJ6oPtsY4IgryvlROalsyZff2_05NEqSkm43WM7F_MBMPO8fi5XTNZ5h3Zl9njhtctjMK80QHaijYORG5FB2gqMXcatZGXpun0kquKHwD0yAmEhETwSgDpkOQlJF73prMWePPQ"
headers = {
    "authorization": f"Bearer {access_token}"
}
routeList=["小7"]#,"542","234","南環幹線","205","618","民權幹線"]

def get_data(url):
    response = requests.get(url, headers=headers)
    print(response.status_code) # 通常是 200 表示成功
    time.sleep(0.5)

    if response.status_code!=200:
        print(response.text)
        return None
    return response.json()

for route in routeList: #shape
    newCoor=[]
    shape_url = f"https://tdx.transportdata.tw/api/basic/v2/Bus/Shape/City/Taipei/{route}?&%24format=JSON"
    data=get_data(shape_url) 
    if not data:
        continue

    for subRoute in data:
        innerCoor=[]
        coor=subRoute["Geometry"][12:-1].split(",")
        for pair in coor:
            lat,lon=map(float,pair.split())
            innerCoor.append([lon,lat])
        
        s=subRoute["SubRouteName"].get("Zh_tw")
        if s==None:
            s=subRoute["RouteName"]["Zh_tw"]
        newCoor.append({
            "Route":subRoute["RouteName"]["Zh_tw"],
            "SubRoute":s,
            "Direction":subRoute["Direction"],"Geometry":innerCoor
            })

    with open(f"data/shape/shape_{route}.json",mode="w",encoding="utf-8") as file:
        json.dump(newCoor,file,ensure_ascii=False, indent=2)

# t=input().split(',')
# ya=[]
# for a in t:
#   j=a.split()
#   ya.append(f'[{j[1]},{j[0]}]')
# print(','.join(ya))