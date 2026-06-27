import json
import requests
import time
access_token="***"
headers = {
    "authorization": f"Bearer {access_token}"
}
routeList=[]

def get_data(url):
    response = requests.get(url, headers=headers)
    print(response.status_code,end=':') # 通常是 200 表示成功

    if response.status_code!=200:
        print(response.text)
        return None
    return response.json()

for i in range(len(routeList)//5+1):
    for route in routeList[5*i:5*i+5]:
        newCoor=[]
        shape_url = f"https://tdx.transportdata.tw/api/basic/v2/Bus/Shape/City/Taipei/{route}?%24filter=RouteName%2FZh_tw%20eq%20%27{route}%27&%24format=JSON"
        data=get_data(shape_url)
        print(route) 
        if not data:
            continue

        for subRoute in data:
            innerCoor=[]
            coor=subRoute["Geometry"][12:-1].split(",")
            for pair in coor:
                lat,lon=map(float,pair.split())
                innerCoor.append([lon,lat])
            
            s=subRoute["SubRouteName"].get("Zh_tw") #副線與路線名稱相同者，SubRouteName為空
            if s==None:
                s=subRoute["RouteName"]["Zh_tw"]
            newCoor.append({
                "Route":subRoute["RouteName"]["Zh_tw"],
                "SubRoute":s,
                "Direction":subRoute["Direction"],
                "Geometry":innerCoor
                })

        with open(f"../yesyes/data/shape/shape_{route}.json",mode="w",encoding="utf-8") as file:
            json.dump(newCoor,file,ensure_ascii=False, indent=2)
    if 5*(i+1)>=len(routeList):
        break
    else:
        print(f"wait 60 seconds please. {len(routeList)-5*(i+1)} routes left.")
        time.sleep(60)


# t=input().split(',')
# ya=[]
# for a in t:
#   j=a.split()
#   ya.append(f'[{j[1]},{j[0]}]')
# print(','.join(ya))