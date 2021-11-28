document.addEventListener("DOMContentLoaded", doSetUp);


let buttonAdd = null;
let buttonReset = null;
let inputCity = null;
let routeContainer = null;
let timer1 = null;
let timer2 = null;


// === LEVEL 0 - "Root" ===


async function doSetUp() {
    await doSetUpPageElements();
    await doSetUpTimers();
    await doPopulateRouteLocalStorage();
    await doPopulateRouteContainer();
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

    routeContainer = document.getElementById("id-route");
}


async function doSetUpTimers() {
    timer1 = setInterval(doPopulateRouteLocalStorage, 4000);
    timer2 = setInterval(doPopulateRouteContainer, 4000);
}


// === LEVEL 2  ===


async function doAddCity() {
    const city_name = inputCity.value;
    inputCity.value = "";

    await apiAddCity(city_name);
    await doPopulateRouteLocalStorage();
    await doPopulateRouteContainer();
}


async function doResetPath() {
    await apiResetPath();
    localStorage.removeItem("route");
    await doPopulateRouteContainer();
}


async function doPopulateRouteLocalStorage() {
    const route = await apiGetRoute();
    localStorage.setItem("route", JSON.stringify(route));
}


async function doPopulateRouteContainer() {
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
