const CREATE_URL = '/create_city';
const CREATE_URL = '/result';


async function api_call(url, args) {
    const headers = new Headers();
    headers.set("content-type", "application/json");
    const resp = await fetch(
        url, {
            body: JSON.stringify(args.json),
            method: args.method || 'POST',
            headers: headers,
        });

    if (resp.status !== 200) {
        return null;
    }


    return await resp.json();
}


async function create_city(city) {
    const payload = await api_call(CREATE_URL, {json: city});
    return payload;
}

async function setUpMy_app() {
    let input1 = document.getElementById("point1");
    let input2 = document.getElementById("point2");
    let button = document.getElementById("navigator-submit");
    let resultSpan = document.querySelector("#result");
   
    button.addEventListener('click', async function() {
        let value1 = input1.value;
        let value2 = input2.value;
        if (value1 === '' || value2 === '') {
            alert('Не хватает данных!');
        } else {
          let points = {
            start: value1,
            end: value2
          };
          let result = await get_distance(points);

        resultSpan.textContent = `Distance between ${points.start} and ${points.end} : ${result} km`;
       }
    })
}

async function setUp() {
    await setUpMy_app();
}


document.addEventListener("DOMContentLoaded", setUp);