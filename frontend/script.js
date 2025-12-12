const API_BASE = "http://127.0.0.1:8000";

function adjustQty(qty) {
    return Math.ceil(qty * 1000) / 1000;
}

async function placeMarketOrder() {
    const symbol = document.getElementById("market-symbol").value;
    const side = document.getElementById("market-side").value;
    let qty = parseFloat(document.getElementById("market-qty").value);
    qty = adjustQty(qty);

    const resElem = document.getElementById("market-result");

    try {
        const res = await fetch(`${API_BASE}/market`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ symbol, side, qty })
        });
        const data = await res.json();
        resElem.textContent = JSON.stringify(data, null, 2);
    } catch (err) {
        resElem.textContent = err;
    }
}

async function placeLimitOrder() {
    const symbol = document.getElementById("limit-symbol").value;
    const side = document.getElementById("limit-side").value;
    let qty = parseFloat(document.getElementById("limit-qty").value);
    qty = adjustQty(qty);
    const price = parseFloat(document.getElementById("limit-price").value);

    const resElem = document.getElementById("limit-result");

    try {
        const res = await fetch(`${API_BASE}/limit`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ symbol, side, qty, price })
        });
        const data = await res.json();
        resElem.textContent = JSON.stringify(data, null, 2);
    } catch (err) {
        resElem.textContent = err;
    }
}

async function placeTWAPOrder() {
    const symbol = document.getElementById("twap-symbol").value;
    const side = document.getElementById("twap-side").value;
    let qty = parseFloat(document.getElementById("twap-qty").value);
    qty = adjustQty(qty);
    const slices = parseInt(document.getElementById("twap-slices").value);
    const interval = parseInt(document.getElementById("twap-interval").value);

    const resElem = document.getElementById("twap-result");

    try {
        const res = await fetch(`${API_BASE}/twap`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ symbol, side, qty, slices, interval })
        });
        const data = await res.json();
        resElem.textContent = JSON.stringify(data, null, 2);
    } catch (err) {
        resElem.textContent = err;
    }
}
