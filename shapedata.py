import json
import requests
import time
access_token="eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJER2lKNFE5bFg4WldFajlNNEE2amFVNm9JOGJVQ3RYWGV6OFdZVzh3ZkhrIn0.eyJleHAiOjE3NzMwNDEzOTQsImlhdCI6MTc3Mjk1NDk5NCwianRpIjoiZDk0YTNiMmUtMzVkNC00YzBmLWI5NGItOGEwZWY2NjMyOGU1IiwiaXNzIjoiaHR0cHM6Ly90ZHgudHJhbnNwb3J0ZGF0YS50dy9hdXRoL3JlYWxtcy9URFhDb25uZWN0Iiwic3ViIjoiNDQzOTdjOWEtZGFkNC00MjNkLTk0YzAtNWI5ODllN2FkZDZkIiwidHlwIjoiQmVhcmVyIiwiYXpwIjoiMzEwNzU4LWYwYjJlMTA2LWEyNzUtNGU2NiIsImFjciI6IjEiLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsic3RhdGlzdGljIiwicHJlbWl1bSIsInBhcmtpbmdGZWUiLCJtYWFzIiwiYWR2YW5jZWQiLCJnZW9pbmZvIiwidmFsaWRhdG9yIiwidG91cmlzbSIsImhpc3RvcmljYWwiLCJjd2EiLCJiYXNpYyJdfSwic2NvcGUiOiJwcm9maWxlIGVtYWlsIiwidXNlciI6ImY1ZWUzNjE5In0.c4OE0PPpNZjzsp1Nhx7ezpKIqBAuLQCgKBTEMPw7mAoHnxcvprj0HNy1UYuqgh-OLT-mzNFNZJIV5uycS94KCdOMYdxfST1oeJxWijD72ofruemQQXuJ6w8IXkbs4O55n152dm4OIRqk3_DWXkVLoUkhhvceXkPu3gd84AytvD0Qp-TLMaEOHvhYxIa_6JXCsritgynd7tOvuzrUnvAyjle_Yg4eDR3QzJmH0OTDhY9r8ky6DTVTfqKrYBZQW9SGqoaZBp8H9dfPTlQjyUSyLKkc-79uOqLWbPDQ4C8cWr8_CN4KgHeIVAWRUx086LAsgV1QfzU9O4M9ZpOjh6p1tg"
headers = {
    "authorization": f"Bearer {access_token}"
}
routeList=["小7","542","234","南環幹線","205","618","民權幹線"]

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
            
        newCoor.append({
            "Route":subRoute["RouteName"]["Zh_tw"],
            "SubRoute":subRoute["SubRouteName"].get("Zh_tw"),
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