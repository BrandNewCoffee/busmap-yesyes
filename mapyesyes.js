const map = L.map('map').setView([25.05,121.53],12);

const tiles = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 20,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

const colorChart=["red","blue"];
currentLine=null
//start=null
const routeList=["234","南環幹線","205","618","民權幹線","紅25","藍36","南京幹線","內科通勤專車22","紅33","2","536","303","303區","542","669","小7"];
currentStops=L.layerGroup().addTo(map)
const dataCache=[];

routeList.forEach(route=>{
    const btn=document.createElement("button");
    btn.textContent=route;
    btn.classList.add("button");
    btn.addEventListener("click",()=>showSubMenu(route));
    routeMenu.appendChild(btn)}
)

async function getData(r){
    if(dataCache[r]){
        return dataCache[r];
    }

    const res=await fetch(`https://BrandNewCoffee.github.io/bus-data/data/route/route_${r}.json`);
    const data=await res.json();
    
    dataCache[r]={};
    data.forEach(subRouteData=>{
        const s=subRouteData.SubRoute;
        const d=subRouteData.Direction;
        if(!dataCache[r][s]){
            dataCache[r][s]={};
        }
        dataCache[r][s][d]=subRouteData;
    });

    return dataCache[r];
}

async function yesyes(){

}

async function showSubMenu(r){
    const data=await getData(r);
    let menu=document.querySelector("#shapeMenu");
    menu.innerHTML="";
    for(const s in data){  //r、s、d為key，並非資料本身(value)
        for(const d in data[s]){
            const btn=document.createElement("button");
            btn.textContent=`${s}(${d})`;
            btn.classList.add("button");
            btn.addEventListener("click",()=>showRoute(r,s,d));
            shapeMenu.appendChild(btn);
        }
    }
}

function showRoute(r,s,d){
    stops(r,s,d);shape(r,s,d);
}

async function stops(r,s,d){
    let data=await getData(r);
    data=data[s][d];
    currentStops.clearLayers();
    data.Stops.forEach(stop=>{
            L.marker([stop.Lat, stop.Lon])
            .addTo(currentStops)
            .bindPopup(`${s}<br>${stop.Name}(${stop.Sequence})`);
    })
}

async function shape(r,s,d){
    let data=await getData(r);
    data=data[s][d];
    if(currentLine){map.removeLayer(currentLine)};
    currentColor=colorChart[d];
    currentLine=L.polyline(data.Geometry,{color:currentColor}).addTo(map);
    // if(start){map.removeLayer(start)};
    // let geo=subRoute.Geometry
    // start=L.marker(geo[0]).addTo(map).bindPopup("起點");
};
