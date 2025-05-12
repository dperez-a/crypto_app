import os, sys

# Asegura que el proyecto esté en sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import streamlit as st
import pandas as pd
from datetime import datetime

from src.db import init_db
from src.services import (
    create_trade,
    get_all_trades,
    compute_metrics_with_price,
    set_price_alert,
    check_alerts,
    delete_trade
)

# Inicializa la base de datos
init_db()

# Sidebar de navegación
st.set_page_config(page_title="Gestor de Portafolio", layout="wide")
menu = st.sidebar.radio("Ir a", ["Dashboard", "Registrar Operación", "Operaciones", "Alertas", "Exportar"] )

# Función para carga de datos
@st.cache_data
def load_trades():
    return get_all_trades()

@st.cache_data
def load_metrics():
    return compute_metrics_with_price()

# Página: Dashboard
def page_dashboard():
    st.title("📊 Dashboard")
    df_metrics = load_metrics()
    if df_metrics.empty:
        st.info("No hay datos para mostrar.")
        return
    # Distribución de inversión
    st.subheader("Distribución de la inversión")
    df_dist = df_metrics[['symbol','total_cost']].set_index('symbol')
    st.bar_chart(df_dist)
    # ROI por símbolo
    st.subheader("ROI por símbolo")
    df_roi = df_metrics[['symbol','roi_pct']].set_index('symbol')
    st.bar_chart(df_roi)
    # Tabla de métricas
    st.subheader("Métricas detalladas")
    df_display = df_metrics.drop(columns=['total_cost'])
    st.dataframe(
        df_display.style.format({
            "avg_price": "€ {:.2f}",
            "current_price": "€ {:.2f}",
            "roi_pct": "{:.2f} %"
        }), use_container_width=True
    )

# Página: Registrar Operación
def page_register():
    st.title("➕ Registrar Operación")
    with st.form("add_trade_form"):
        symbol = st.text_input("Símbolo", max_chars=10)
        qty = st.number_input("Cantidad", min_value=0.0, format="%.8f")
        price = st.number_input("Precio unitario", min_value=0.0, format="%.8f")
        date_str = st.text_input("Fecha (YYYY-MM-DD HH:MM)")
        submitted = st.form_submit_button("Añadir")
        if submitted:
            try:
                dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M") if date_str else None
                trade = create_trade(symbol, qty, price, dt)
                st.success(f"Operación añadida: {trade}")
            except Exception as e:
                st.error(f"Error: {e}")

# Página: Operaciones Registradas
def page_operations():
    st.title("📋 Operaciones Registradas")
    trades = load_trades()
    if not trades:
        st.info("No hay operaciones registradas.")
        return
    df_ops = pd.DataFrame([
        {"ID": t.id, "Símbolo": t.symbol, "Cantidad": t.quantity,
         "Precio": t.price, "Fecha": t.date.strftime("%Y-%m-%d %H:%M")} for t in trades
    ])
    st.dataframe(df_ops, use_container_width=True)
    # Formulario eliminar
    st.subheader("🗑️ Eliminar Operación")
    del_id = st.number_input("ID", min_value=1, step=1)
    if st.button("Borrar Operación"):
        if delete_trade(del_id):
            st.success(f"Operación {del_id} borrada.")
            st.experimental_rerun()
        else:
            st.error("ID no encontrado.")

# Página: Alertas de Precio
def page_alerts():
    st.title("🚨 Alertas de Precio")
    with st.form("alerts_form"):
        sym = st.text_input("Símbolo alerta")
        th = st.number_input("Umbral (€)", min_value=0.0, format="%.2f")
        submitted = st.form_submit_button("Configurar Alerta")
        if submitted:
            if sym and th > 0:
                set_price_alert(sym, th)
                st.success(f"Alerta establecida: {sym.upper()} ≥ {th}")
            else:
                st.error("Datos inválidos.")
    st.markdown("---")
    alerts = check_alerts()
    if alerts:
        for msg in alerts:
            st.warning(msg)
    else:
        st.info("No hay alertas disparadas.")

# Página: Exportar
def page_export():
    st.title("💾 Exportar a Excel")
    if st.button("Exportar Operaciones y Métricas"):
        try:
            from src.main import export_to_excel
            export_to_excel()
            st.success("Exportación completada")
        except Exception as e:
            st.error(f"Error al exportar: {e}")

# Ruteo de páginas
if menu == "Dashboard":
    page_dashboard()
elif menu == "Registrar Operación":
    page_register()
elif menu == "Operaciones":
    page_operations()
elif menu == "Alertas":
    page_alerts()
elif menu == "Exportar":
    page_export()
