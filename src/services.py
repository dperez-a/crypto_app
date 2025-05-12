from datetime import datetime
import math
import pandas as pd
from typing import Optional, List, Dict

from src.models import Trade
from src.db import SessionLocal

# --- Operaciones CRUD y métricas básicas ---

def create_trade(symbol: str, quantity: float, price: float, date: datetime = None) -> Trade:
    """
    Inserta una operación en la base de datos.
    """
    date = date or datetime.utcnow()
    session = SessionLocal()
    try:
        trade = Trade(symbol=symbol.upper(), quantity=quantity, price=price, date=date)
        session.add(trade)
        session.commit()
        session.refresh(trade)
        return trade
    finally:
        session.close()


def get_all_trades() -> List[Trade]:
    """
    Devuelve todas las operaciones ordenadas por fecha.
    """
    session = SessionLocal()
    try:
        return session.query(Trade).order_by(Trade.date).all()
    finally:
        session.close()


def get_trades_by_symbol(symbol: str) -> List[Trade]:
    """
    Devuelve las operaciones de un símbolo concreto.
    """
    session = SessionLocal()
    try:
        return (
            session.query(Trade)
            .filter(Trade.symbol == symbol.upper())
            .order_by(Trade.date)
            .all()
        )
    finally:
        session.close()


def compute_metrics() -> pd.DataFrame:
    """
    Calcula, por símbolo:
      - precio promedio de compra (avg_price)
      - cantidad total (total_qty)
      - inversión total (total_cost)
    Devuelve DataFrame con columnas ['symbol','avg_price','total_qty','total_cost'].
    """
    trades = get_all_trades()
    if not trades:
        return pd.DataFrame(columns=['symbol','avg_price','total_qty','total_cost'])

    df = pd.DataFrame([
        {'symbol': t.symbol, 'qty': t.quantity, 'cost': t.quantity * t.price}
        for t in trades
    ])
    grouped = df.groupby('symbol').agg(
        total_qty=('qty', 'sum'),
        total_cost=('cost', 'sum')
    ).reset_index()
    grouped['avg_price'] = grouped['total_cost'] / grouped['total_qty']
    return grouped[['symbol', 'avg_price', 'total_qty', 'total_cost']]


# === Precios en tiempo real y alertas ===

import yfinance as yf
import ccxt

# Configuración de CCXT para Binance
exchange = ccxt.binance({'enableRateLimit': True})


def get_stock_price(symbol: str) -> Optional[float]:
    """
    Devuelve el precio de cierre más reciente de un ticker de bolsa, o None si falla.
    """
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period="1d")
        if data.empty:
            return None
        return float(data['Close'].iloc[-1])
    except Exception:
        return None


def get_crypto_price(symbol: str) -> Optional[float]:
    """
    Devuelve el precio last de un par cripto (symbol/USDT), o None si falla.
    """
    try:
        ticker = exchange.fetch_ticker(f"{symbol}/USDT")
        return float(ticker['last'])
    except Exception:
        return None


def compute_metrics_with_price() -> pd.DataFrame:
    """
    Extiende compute_metrics() añadiendo:
      - current_price (precio actual o NaN)
      - roi_pct (rendimiento porcentual)
    """
    df = compute_metrics()
    if df.empty:
        return df

    crypto_list = ['BTC', 'ETH', 'XRP', 'LTC', 'ADA']

    def fetch_price(sym: str) -> Optional[float]:
        s = sym.upper()
        if s in crypto_list:
            price = get_crypto_price(s)
        else:
            price = get_stock_price(s)
            # Prueba sufijo español si no hay precio
            if price is None and not s.endswith('.MC'):
                price = get_stock_price(f"{s}.MC")
        return price

    df['current_price'] = df['symbol'].apply(fetch_price)
    df['current_price'] = df['current_price'].apply(lambda x: math.nan if x is None else x)
    df['roi_pct'] = (df['current_price'] - df['avg_price']) / df['avg_price'] * 100

    return df[['symbol', 'avg_price', 'current_price', 'total_qty', 'total_cost', 'roi_pct']]


# Gestión de alertas
alert_rules: Dict[str, float] = {}


def set_price_alert(symbol: str, threshold: float) -> None:
    """
    Configura una alerta para cuando symbol ≥ threshold.
    """
    alert_rules[symbol.upper()] = threshold


def check_alerts() -> List[str]:
    """
    Comprueba todas las alertas y devuelve mensajes para las disparadas.
    """
    messages: List[str] = []
    metrics_df = compute_metrics_with_price()
    for sym, th in alert_rules.items():
        row = metrics_df[metrics_df['symbol'] == sym]
        if not row.empty:
            price = row['current_price'].iloc[0]
            if price >= th:
                messages.append(f"{sym} ha superado {th}: precio actual {price:.2f}")
    return messages

def delete_trade(trade_id: int) -> bool:
    """
    Elimina una operación por su ID.
    Devuelve True si se eliminó, False si no se encontró.
    """
    session = SessionLocal()
    try:
        trade = session.query(Trade).filter(Trade.id == trade_id).first()
        if trade:
            session.delete(trade)
            session.commit()
            return True
        return False
    finally:
        session.close()