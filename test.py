import json
def list_append(r,s,d,geometry,stops):
    l.append({
        "Route":r,
        "SubRoute":s,
        "Direction":d,
        "Geometry":geometry,
        "Stops":stops
    })

routeList=["234","南環幹線","205","618","民權幹線","紅25","藍36","南京幹線","內科通勤專車22","紅33","2","536","303","303區","542","669","小7"]

for r in routeList:
    with open(f"../yesyes/data/shape/shape_{r}.json",mode="r",encoding="utf-8") as file:
        shapedata=json.load(file)
    with open(f"../yesyes/data/stops/stops_{r}.json",mode="r",encoding="utf-8") as file:
        stopsdata=json.load(file)
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