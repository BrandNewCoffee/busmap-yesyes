const map = L.map('map').setView([25.05,121.53],12);

const tiles = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

const colorChart=["red","blue"];
currentLine=null
routeList=["234","南環幹線","205","618","民權幹線","542"];


routeList.forEach(route=>{
    const btn=document.createElement("button");
    btn.textContent=route;
    btn.style.cursor="pointer";
    btn.addEventListener("click",()=>showMenu(route));
    routeMenu.appendChild(btn)}
)

function yesyes(){
    console.log("yesyes");
}

function showMenu(route){
    fetch(`https://BrandNewCoffee.github.io/bus-data/data/shape/shape_${route}.json`)
    .then(res=>res.json())
    .then(data=>{
        let menu=document.querySelector("#subRouteMenu");
        menu.innerHTML="";
        data.forEach(subRoute=>{
            const btn=document.createElement("button");
            btn.textContent=`${subRoute.SubRoute} ${subRoute.Direction}`;
            btn.style.cursor="pointer";
            btn.addEventListener("click",()=>shape(route,subRoute.SubRoute,subRoute.Direction));
            subRouteMenu.appendChild(btn);
        })
    })
}

function stops(){
    fetch("https://BrandNewCoffee.github.io/bus-data/data/stops/stops_南環幹線.json")
    .then(res => res.json())
    .then(data=>{
        data.forEach(subRoute=>{
                    subRoute.stops.forEach(stop => {
                    L.marker([stop.lat, stop.lon])
                    .addTo(routeLayer)
                    .bindPopup(`${subRoute.SubRoute} (${subRoute.Direction})<br>${stop.Name}`);
                });
        });
    });
};

function shape(r,s,d){
    fetch(`https://BrandNewCoffee.github.io/bus-data/data/shape/shape_${r}.json`)
    .then(res=>res.json())
    .then(data=>{
        if(currentLine){map.removeLayer(currentLine)};
        data.forEach(subRoute=>{
            if(subRoute.SubRoute==s && subRoute.Direction==d){
                currentColor=colorChart[subRoute.Direction]
                currentLine=L.polyline(subRoute.Geometry,{color:currentColor}).addTo(map);	
            } 
        });
    });
};
//stops();