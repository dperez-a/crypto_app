# Personal Investment Portfolio Manager

A Python macOS application for offline management of cryptocurrency and stock portfolios. Provides manual trade entry, automated metrics (average entry price, total invested, ROI), real-time price fetching, configurable alerts, a multi-page Streamlit dashboard, and Excel export.

---

## Table of Contents

1. [Features](#features)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [Running the App](#running-the-app)
5. [Project Structure](#project-structure)
6. [Usage Guide](#usage-guide)
7. [Configuration](#configuration)
8. [Dependencies](#dependencies)
9. [Contributing](#contributing)
10. [License](#license)

---

## Features

* 📈 **Manual Trade Entry**: Record buys/sells with symbol, quantity, price, and timestamp.
* 🔢 **Automated Metrics**: Calculate average entry price, total invested per asset, and ROI.
* 💹 **Real-Time Prices**: Fetch live market prices using [yfinance](https://pypi.org/project/yfinance/) (stocks) and [ccxt](https://pypi.org/project/ccxt/) (crypto).
* 🚨 **Price Alerts**: Set threshold alerts and receive notifications in-app.
* 📊 **Streamlit Dashboard**:

  * Dashboard view with bar charts (investment distribution, ROI) and detailed metrics table.
  * Separate pages for trade registration, listing/deletion, alerts, and export.
* 💾 **Excel Export**: Export trades and metrics to `.xlsx` files.

---

## Prerequisites

* **macOS** (Intel or Apple Silicon) with Python 3.13 installed via Homebrew.
* [Homebrew](https://brew.sh/) for package management.
* Git for version control.

---

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/your-username/crypto_app.git
   cd crypto_app
   ```

2. **Create and activate a virtual environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

---

## Running the App

### Streamlit Dashboard (recommended)

```bash
streamlit run src/app.py
```

* Opens a web UI at `http://localhost:8501`.
* Navigate pages via the sidebar: **Dashboard**, **Register Trade**, **Trades**, **Alerts**, **Export**.

### CLI Mode

```bash
python3 -m src.main
```

* Text-based menu in terminal for listing, adding, metrics, export, and exit.

---

## Project Structure

```
crypto_app/
├── venv/               # Virtual environment
├── data/               # SQLite database & output Excel files
├── src/
│   ├── db.py           # SQLAlchemy setup & init_db()
│   ├── models.py       # Trade model definition
│   ├── services.py     # CRUD, metrics, pricing, alerts
│   ├── main.py         # CLI entry point & export function
│   └── app.py          # Streamlit multi-page dashboard
├── requirements.txt    # Python dependencies
├── README.md           # Project documentation
└── .gitignore          # Ignored files
```

---

## Usage Guide

1. **Register a trade**: Enter symbol (e.g., `BTC`, `AAPL`), quantity, price, and optional timestamp.
2. **View trades**: Browse or delete recorded operations.
3. **Check metrics**: See aggregated average price, current market price, total invested, and ROI.
4. **Set alerts**: Define price thresholds to monitor key assets.
5. **Export data**: Generate `data/trades.xlsx` and `data/metrics.xlsx`.

---

## Configuration

* **Database**: `data/portfolio.db` (auto-created on first run).
* **Excel output**: `data/trades.xlsx`, `data/metrics.xlsx`.
* **Alert rules**: Stored in memory; reset on restart.

---

## Dependencies

See [`requirements.txt`](requirements.txt) for full list. Major libraries:

* SQLAlchemy + SQLite
* Pandas
* openpyxl
* yfinance
* ccxt
* Streamlit

---

## Contributing

1. Fork the repo.
2. Create a feature branch: `git checkout -b feature/YourFeature`.
3. Commit your changes: `git commit -m "Add some feature"`.
4. Push branch: `git push origin feature/YourFeature`.
5. Open a Pull Request.

Please follow code style and include tests when possible.

---

## License

MIT License © 2025 Daniel Pérez
