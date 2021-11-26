const ADD_URL = '/add_city';
const GET_URL = '/get_route';
const SWAP_URL = '/swap';
const DEL_URL = '/del';

/**
 * @param {string} url
 * @param {object} args
 * @return {json}
 */
async function api_call(url, args) {
    const headers = new Headers();

    headers.set("content-type", "application/json");

    fetchArgs = {
        method: "GET",
        headers: headers,
        body: null,
    }

    if (args) {
        if (args.method) {
            fetchArgs.method = args.method;
            if (args.method != "GET" && args.json) {
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

/**
 * @param {string} city
 * @return {object}
 */
async function create_city(city) {
    const payload = await api_call(
        ADD_URL, {
            json: {name: city},
            method: "POST",
        });

    return payload;
}


/**
 * @return {object}
 */
async function get_distance() {
    const payload = await api_call(GET_URL);

    return payload;
}


/**
 * @return {void}
 */
async function setUpMy_app() {
    let button = document.getElementById("navigator-submit");
    let resultSpan = document.getElementById("result");

    button.addEventListener('click', async function () {
        let inputs = [],
            values = [],
            points = {},
            error = false,
            destString = '',
            result;

        // TODO: delete all cities

        inputs = document.querySelectorAll('#points-fields input');

        for (let input of inputs) {
            if (!input.value) {
                error = true;
                alert(`Не хватает данных в поле ${input.dataset.field}!`);
            } else {
                points[input.name] = input.value;
                values.push(input.value);
                await create_city(input.value);
            }
        }

        if (!error) {
            destString = values.join(' and ');
            result = await get_distance(points);
            let result_ = JSON.stringify(result);
            resultSpan.textContent = `Distance between ${destString}: ${result_} km`;
        }
    })
}

/**
 * @return {void}
 */
async function setUp() {
    await setUpMy_app();
}

document.addEventListener("DOMContentLoaded", setUp);


/**
 * Add/hide additional field by button click
 */
let fieldsContainer = document.getElementById('points-fields');
let openFieldButton = document.getElementById('field-opener');

// start number for new fields
let counter = 3;
// max number of fields
let maxFields = 6;
let getTemplate = function (num) {
    return `<div class="point-block point${num}-wrapper">
      <label for="point${num}">Point ${num}:</label>
      <div class="controller">
        <input id="point${num}" name="point${num}" type="text" data-field=${num} placeholder="City"/>
        <button type="button" 
                class="closer" 
                data-field=${num}
                onclick="removeField(this)">X</button>
      </div>
    </div>`;
}

/**
 * Get node with the close-field-button from the last added field
 * @return {node || bool}
 */
let getLastCloseButton = function () {
    let closeButtons = document.querySelectorAll('.closer');

    if (closeButtons) {
        let len = closeButtons.length;
        return len < 1 ? "" : closeButtons[len - 1];
    }

    return false;
}

/**
 * Add field for point, disables close-button form the previosly added field
 * Increase fields-counter
 * @return {void}
 */
let addField = function () {
    if (counter <= maxFields) {

        if (getLastCloseButton()) {
            getLastCloseButton().disabled = true;
        }

        fieldsContainer.insertAdjacentHTML('beforeend', getTemplate(counter));
        counter++;
    }

    if (counter === maxFields + 1) {
        openFieldButton.disabled = true;
    }
}

/**
 * Remove field for point, enable close-button form the previosly added field
 * Decrease fields-counter
 * @return {void}
 */
let removeField = function (el) {
    let fieldNumber = el.dataset.field;

    if (counter > fieldNumber) {
        openFieldButton.disabled = false;
        counter--;
    }

    el.closest('.point-block').remove();

    if (getLastCloseButton()) {
        getLastCloseButton().disabled = false;
    }
}

/**
 * Listener for the button for adding new fields
 * @return {void}
 */
openFieldButton.addEventListener('click', function (e) {
    e.preventDefault();
    addField();
})
