# Binance Futures Trading Bot (Testnet)

A **simplified trading bot** for Binance Futures Testnet (USDT-M) built in **Python** with **FastAPI backend** and a **lightweight HTML/JS frontend**.  
Supports **Market**, **Limit**, and **TWAP orders**, demonstrating basic algorithmic trading concepts.

---

## Features

- **Market Orders**: Buy/Sell immediately at market price.
- **Limit Orders**: Buy/Sell at a specified price.
- **TWAP Orders**: Split a total quantity into multiple slices over a time interval.
- **Backend**: FastAPI, python-binance, logs requests/responses/errors, handles min notional and precision.
- **Frontend**: Simple GUI to place orders and view responses in real-time.
- **CORS support** for frontend integration.

---

---

---

## Setup Instructions

1.  **Clone repository**

    ```bash
    git clone <repo_url>
    cd trading-bot
    ```

2.  **Install Python dependencies**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Set Binance Testnet API keys in `.env`:**

    ```bash
    BINANCE_API_KEY=<your_testnet_api_key>
    BINANCE_API_SECRET=<your_testnet_api_secret>
    ```

4.  **Run backend**

    ```bash
    uvicorn api.server:app --reload
    ```
    > **Backend runs at:** `http://127.0.0.1:8000`

5.  **Serve frontend**

    ```bash
    cd frontend
    python3 -m http.server 8001
    ```
    > **Open browser:** `http://127.0.0.1:8001`

---

## Usage

### Market Order

* Enter symbol, side, qty
* Click **Place Market Order**

### Limit Order

* Enter symbol, side, qty, price
* Click **Place Limit Order**

### TWAP Order

* Enter symbol, side, total qty, slices, interval (sec)
* Click **Place TWAP Order**
* *Bot splits orders over specified interval
