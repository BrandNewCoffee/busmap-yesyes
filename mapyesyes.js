const map = L.map('map').setView([25.05,121.53],12);

const tiles = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 20,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

const colorChart=["red","blue"];
currentLine=null
//start=null
routeList=["234","南環幹線","205","618","民權幹線","紅25","藍36","南京幹線","內科通勤專車22","紅33","542","小7"];
currentStops=L.layerGroup().addTo(map)

routeList.forEach(route=>{
    const btn=document.createElement("button");
    btn.textContent=route;
    btn.classList.add("button");
    btn.addEventListener("click",()=>showMenu(route));
    routeMenu.appendChild(btn)}
)

function yesyes(){
    console.log("yesyes");
}

function showMenu(route){
    fetch(`https://BrandNewCoffee.github.io/bus-data/data/route/route_${route}.json`)
    .then(res=>res.json())
    .then(data=>{
        let menu=document.querySelector("#shapeMenu");
        menu.innerHTML="";
        data.forEach(subRoute=>{
            const btn=document.createElement("button");
            btn.textContent=`${subRoute.SubRoute}(${subRoute.Direction})`;
            btn.classList.add("button");
            btn.addEventListener("click",()=>showRoute(route,subRoute.SubRoute,subRoute.Direction));
            shapeMenu.appendChild(btn);
        })
    })
}

function showRoute(r,s,d){
    stops(r,s,d);
    shape(r,s,d);
}

function stops(r,s,d){
    fetch(`https://BrandNewCoffee.github.io/bus-data/data/route/route_${r}.json`)
    .then(res => res.json())
    .then(data=>{
        currentStops.clearLayers();
        data.forEach(subRoute=>{
            if(s==subRoute.SubRoute && d==subRoute.Direction){
                subRoute.Stops.forEach(stop => {
                L.marker([stop.Lat, stop.Lon])
                .addTo(currentStops)
                .bindPopup(`${subRoute.SubRoute}<br>${stop.Name}(${stop.Sequence})`);//`${subRoute.SubRoute}(${subRoute.Direction})<br>${stop.Name}`
                })
            }
        })
    })
}

function shape(r,s,d){
    fetch(`https://BrandNewCoffee.github.io/bus-data/data/route/route_${r}.json`)
    .then(res=>res.json())
    .then(data=>{
        if(currentLine){map.removeLayer(currentLine)};
        data.forEach(subRoute=>{
            if(subRoute.SubRoute==s && subRoute.Direction==d){
                currentColor=colorChart[subRoute.Direction]
                currentLine=L.polyline(subRoute.Geometry,{color:currentColor}).addTo(map);
                // if(start){map.removeLayer(start)};
                // let geo=subRoute.Geometry
                // start=L.marker(geo[0]).addTo(map).bindPopup("起點");
            } 
        });
    });
};

