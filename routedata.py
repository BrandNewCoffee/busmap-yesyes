import json

routeList=[]
def list_append(r,s,d,geometry,stops):
    l.append({
        "Route":r,
        "SubRoute":s,
        "Direction":d,
        "Geometry":geometry,
        "Stops":stops
    })

for r in routeList:
    try: #shape或stops檔案為空的路線直接跳過
        with open(f"data/shape/shape_{r}.json",mode="r",encoding="utf-8") as file:
            shapedata=json.load(file)
        with open(f"data/stops/stops_{r}.json",mode="r",encoding="utf-8") as file:
            stopsdata=json.load(file)
    except:
        continue
        
    l=[]
    for stops in stopsdata:#處理副線
        basicshape=dict()
        paired=False
        stops_sub,stops_dir=stops["SubRoute"],stops["Direction"]
        for shape in shapedata:
            shape_sub,shape_dir=shape["SubRoute"],shape["Direction"]
            if  shape_sub==r: #設定基礎shape
                basicshape[shape_dir]=shape["Geometry"]
            if shape_sub==stops_sub and shape_dir==stops_dir: #若stops和shape有匹配的副線->添加此副線到檔案裡
                list_append(r,stops_sub,stops_dir,shape["Geometry"],stops["Stops"])
                paired=True 
                break
        if not paired: #若stops與shape不匹配->給他基礎shape
            list_append(r,stops_sub,stops_dir,basicshape[stops_dir],stops["Stops"])
    with open(f"data/route/route_{r}.json",mode="w",encoding="utf-8") as file:
        json.dump(l,file,ensure_ascii=False,indent=2)