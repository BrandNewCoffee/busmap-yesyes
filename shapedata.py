import json
import requests
import time
access_token=""
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