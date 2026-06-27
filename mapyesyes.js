const map = L.map('map').setView([25.05,121.53],12);

const tiles = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 20,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

const colorChart=["red","blue"];
const dirChart=["去程","回程"];
let routeList=[];
let currentLine=null;
//start=null;
let currentStops=L.layerGroup().addTo(map);
const dataCache=[];

async function getRouteList(){
    const res=await fetch("https://BrandNewCoffee.github.io/busmap-yesyes/data/routelist_sorted.json");
    const data=await res.json();
    return data;
}

async function init(){
    routeList=await getRouteList();
    routeList.forEach(r=>showMenu(r,"routeList"));    
}

init();

async function getData(r){
    if(dataCache[r]){
        return dataCache[r];
    }

    const res=await fetch(`https://BrandNewCoffee.github.io/busmap-yesyes/data/route/route_${r}.json`);
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
    console.log("yesyes");
}

function search(){
    let content=document.getElementById("searchInput").value;
    const srchList=document.getElementById("searchRouteList");
    srchList.innerHTML="";
    routeList.forEach(route=>{
        if(route.includes(content)){showMenu(route,"searchRouteList")}
    })
    const menu=document.getElementById("routeMenu");
    const subMenu=document.getElementById("subRouteMenu");
    const srchMenu=document.getElementById("searchRouteMenu");
    menu.style.display="none";
    subMenu.style.display="none";
    srchMenu.style.display="flex";
}

function showMenu(r,menu){
    const list=document.getElementById(menu);
    const btn=document.createElement("button");
    btn.textContent=r;
    btn.classList.add("routeBtn");
    btn.addEventListener("click",()=>showSubMenu(r));
    list.appendChild(btn);
}

async function showSubMenu(r){
    const data=await getData(r); //data=dataCache[r]
    const subList=document.getElementById("subRouteList");
    subList.innerHTML="";
    for(const s in data){  //提示:r、s、d為key，並非資料本身(value)
        const subRow=document.createElement("div");
        subRow.classList.add("subRouteRow");
        for(const d in data[s]){
            const btn=document.createElement("button");
            btn.textContent=s;
            btn.classList.add("routeBtn");
            btn.addEventListener("click",()=>showRoute(r,s,d));
            subRow.appendChild(btn);
        }
        subList.appendChild(subRow);
    }
    const menu=document.getElementById("routeMenu");
    const subMenu=document.getElementById("subRouteMenu");
    const srchMenu=document.getElementById("searchRouteMenu");
    menu.style.display="none";
    subMenu.style.display="flex";
    srchMenu.style.display="none";
}

function backToMenu(){
    const menu=document.getElementById("routeMenu");
    const subMenu=document.getElementById("subRouteMenu");
    const srchMenu=document.getElementById("searchRouteMenu");
    menu.style.display="flex";
    subMenu.style.display="none";
    srchMenu.style.display="none";
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
    // let geo=data.Geometry
    // start=L.marker(geo[0]).addTo(map).bindPopup("起點");
};
