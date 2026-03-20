import json
def list_append(r,s,d,geometry,stops):
    l.append({
        "Route":r,
        "SubRoute":s,
        "Direction":d,
        "Geometry":geometry,
        "Stops":stops
    })
for r in ["234","南環幹線","205","618","民權幹線","紅25","藍36","南京幹線","內科通勤專車22","紅33","542","小7"]:
    with open(f"../yesyes/data/shape/shape_{r}.json",mode="r",encoding="utf-8") as file:
        shapedata=json.load(file)
    with open(f"../yesyes/data/stops/stops_{r}.json",mode="r",encoding="utf-8") as file:
        stopsdata=json.load(file)
        l=[]

    for stops in stopsdata:
        shapelist=dict()
        paired=False
        stops_sub=stops["SubRoute"]
        stops_dir=stops["Direction"]
        for shape in shapedata:
            shape_sub=shape["SubRoute"]
            shape_dir=shape["Direction"]
            # print(shape_sub,r)
            if  shape_sub==r:
                shapelist[shape_dir]=shape["Geometry"]

            if shape_sub==stops_sub and shape_dir==stops_dir:
                list_append(r,stops_sub,stops_dir,shape["Geometry"],stops["Stops"])
                paired=True
                break
        
        if not paired:
            # print(stops_sub,stops_dir)
            list_append(r,stops_sub,stops_dir,shapelist[stops_dir],stops["Stops"])
    with open(f"data/route/route_{r}.json",mode="w",encoding="utf-8") as file:
        json.dump(l,file,ensure_ascii=False,indent=2)