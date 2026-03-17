import json
import requests
import time
access_token=""
headers = {
    "authorization": f"Bearer {access_token}"
}
routeList=["小7","542","234","南環幹線","205","618","民權幹線"]

def get_data(url):
  response = requests.get(url, headers=headers)
  print(response.status_code)   # 通常是 200 表示成功
  time.sleep(5)
  if response.status_code!=200:
      print(response.text)
      return None
  return response.json()

for route in routeList:
    map_data = []
    stops_url=f"https://tdx.transportdata.tw/api/basic/v2/Bus/StopOfRoute/City/Taipei/{route}?&%24format=JSON"
    data=get_data(stops_url)
    if not data:
        continue
    for subRoute in data:
        route_info = {
            "Route": subRoute["RouteName"]["Zh_tw"],
            "SubRoute": subRoute["SubRouteName"]["Zh_tw"],
            "Direction": subRoute["Direction"],
            "Stops": []
        }

        for stop in subRoute["Stops"]:
            route_info["Stops"].append({
                "Name": stop["StopName"]["Zh_tw"],
                "Lat": stop["StopPosition"]["PositionLat"],
                "Lon": stop["StopPosition"]["PositionLon"],
                "Sequence": stop["StopSequence"]
            })

        map_data.append(route_info)
    with open(f"data/stops/stops_{route}.json", "w", encoding="utf-8") as f:
        json.dump(map_data, f, ensure_ascii=False, indent=2)