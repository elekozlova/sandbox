document.addEventListener("DOMContentLoaded", doSetUp);


let buttonAdd = null;
let buttonReset = null;
let dataSynced = false;
let inputCity = null;
let mapContainer = null;
let routeContainer = null;
let timer1 = null;
let timer2 = null;


// === LEVEL 0 - "Root" ===


async function doSetUp() {
    await doSetUpPageElements();
    await doSetUpTimers();
    await doPopulateRouteLocalStorage();
    await doPopulateUI(true);
    await doRefreshMap(true);
}


// === LEVEL 1  ===


async function doSetUpPageElements() {
    buttonAdd = document.getElementById("id-add");
    buttonAdd.addEventListener("click", doAddCity);

    buttonReset = document.getElementById("id-reset");
    buttonReset.addEventListener("click", doResetPath);

    inputCity = document.getElementById("id-city");
    inputCity.addEventListener("keyup", async function (event) {
        if (event.code === "Enter" && event.key === "Enter") {
            event.preventDefault();
            await doAddCity();
        }
    });

    mapContainer = document.getElementById("id-map");

    routeContainer = document.getElementById("id-route");
}


async function doSetUpTimers() {
    timer1 = setInterval(doPopulateRouteLocalStorage, 4000);
    timer2 = setInterval(doPopulateUI, 4000);
}


async function doPopulateRouteLocalStorage() {
    const route = await apiGetRoute();
    const routeStr = JSON.stringify(route);

    const previousRouteStr = localStorage.getItem("route");
    dataSynced = (previousRouteStr === routeStr);

    localStorage.setItem("route", routeStr);
}


async function doPopulateUI(forced = false) {
    if (!forced && dataSynced) return;

    await doRefreshMap(forced);

    while (routeContainer.firstChild) {
        routeContainer.removeChild(routeContainer.firstChild);
    }

    const route = JSON.parse(localStorage.getItem("route") || "{}");
    if (!route.path || !route.total) {
        console.error(`invalid route: ${JSON.stringify(route)}`);
        return;
    }

    for (const [index, vector] of route.path.entries()) {
        if (index === 0) {
            let hFrom = document.createElement("h3");
            hFrom.innerText = `🌇 ${vector.from_.name}`;
            hFrom.cityId = `${vector.from_.id}`;
            routeContainer.appendChild(hFrom);
        }

        let pPath = document.createElement("p");
        let sPath = document.createElement("span");
        sPath.innerText = `✈️ ${vector.dt.km} km — ${vector.dt.hours} hrs`;
        pPath.appendChild(sPath);
        routeContainer.appendChild(pPath);

        let hTo = document.createElement("h3");
        hTo.innerText = `🏙 ${vector.to.name}`;
        hTo.cityId = `${vector.to.id}`;
        routeContainer.appendChild(hTo);
    }
}


async function doRefreshMap(forced = false) {
    if (!forced && dataSynced) return;

    while (mapContainer.firstChild) {
        mapContainer.removeChild(mapContainer.firstChild);
    }

    let mapFrame = document.createElement("iframe");
    mapFrame.style.width = mapFrame.style.height = "100%";
    mapFrame.src = "/map";
    mapContainer.appendChild(mapFrame);
}


// === LEVEL 2  ===


async function doAddCity() {
    const city_name = inputCity.value;
    inputCity.value = "";

    await apiAddCity(city_name);
    await doPopulateRouteLocalStorage();
    await doPopulateUI();
}


async function doResetPath() {
    await apiResetPath();
    localStorage.removeItem("route");
    await doPopulateUI();
}


// === LEVEL 3  ===


async function apiAddCity(city) {
    return apiCall(
        "/add_city", {
            json: {name: city},
            method: "POST",
        });
}


async function apiResetPath() {
    return apiCall("/del", {method: "DELETE"});
}


async function apiGetRoute() {
    return apiCall("/get_route");
}


// === LEVEL 4 ===


async function apiCall(url, args = {}) {
    const headers = new Headers();

    headers.set("content-type", "application/json");

    const fetchArgs = {
        method: "GET",
        headers: headers,
        body: null,
    }

    if (args) {
        if (args.method) {
            fetchArgs.method = args.method;
            if (args.method !== "GET" && args.json) {
                fetchArgs.body = JSON.stringify(args.json);
            }
        }
    }

    const resp = await fetch(url, fetchArgs);

    if (resp.status !== 200) {
        return null;
    }

    return resp.json();
}
