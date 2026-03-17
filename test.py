import json
for r in ["紅25","藍36","南京幹線","內科通勤專車22","紅33"]:
    with open(f"../yesyes/data/shape/shape_{r}.json",mode="r",encoding="utf-8") as file:
        shapedata=json.load(file)
    with open(f"../yesyes/data/stops/stops_{r}.json",mode="r",encoding="utf-8") as file:
        stopsdata=json.load(file)
        l=[]
    for sshape in shapedata:
        shape_sub=sshape["SubRoute"]
        shape_dir=sshape["Direction"]
        for sstops in stopsdata:
            stops_sub=sstops["SubRoute"]
            stops_dir=sstops["Direction"]
            if shape_sub==stops_sub and shape_dir==stops_dir:
                l.append({
                    "Route":r,
                    "SubRoute":shape_sub,
                    "Direction":sshape["Direction"],
                    "Geometry":sshape["Geometry"],
                    "Stops":sstops["Stops"]
                })
    with open(f"data/route/route_{r}.json",mode="w",encoding="utf-8") as file:
        json.dump(l,file,ensure_ascii=False,indent=2)