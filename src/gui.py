import PySimpleGUI as sg
import pandas as pd
from datetime import datetime
from src.db import init_db
from src.services import (
    create_trade,
    get_all_trades,
    compute_metrics
)

# Inicializa DB
init_db()

# Configuración de la ventana
sg.theme("LightBlue2")
layout = [
    [sg.Text("Gestor de Portafolio", font=("Any", 16))],

    # Tabla de operaciones
    [sg.Frame("Operaciones registradas", [
        [sg.Table(
            values=[],
            headings=["ID","Símbolo","Cantidad","Precio","Fecha"],
            key="-TABLE-",
            auto_size_columns=True,
            display_row_numbers=False,
            num_rows=10,
            expand_x=True,
            expand_y=True,
        )]
    ], expand_x=True, expand_y=True)],

    # Formulario añadir
    [sg.Frame("Añadir Operación", [
        [sg.Text("Símbolo", size=(8,1)), sg.Input(key="-SYM-", size=(10,1))],
        [sg.Text("Cantidad", size=(8,1)), sg.Input(key="-QTY-", size=(10,1))],
        [sg.Text("Precio", size=(8,1)), sg.Input(key="-PRC-", size=(10,1))],
        [sg.Text("Fecha (YYYY-MM-DD HH:MM)", size=(20,1)), sg.Input(key="-DT-", size=(16,1))],
        [sg.Button("Añadir", key="-ADD-")]
    ])],

    # Métricas y export
    [
      sg.Button("Ver Métricas", key="-METRICS-"),
      sg.Button("Exportar a Excel", key="-EXPORT-"),
      sg.Button("Salir", key="-EXIT-")
    ],

    # Área de salida de texto
    [sg.Multiline("", size=(60,10), key="-OUTPUT-", disabled=True)]
]

window = sg.Window("Crypto & Bolsa Manager", layout, resizable=True)

def refresh_table():
    data = get_all_trades()
    table_data = [[t.id, t.symbol, t.quantity, t.price, t.date.strftime("%Y-%m-%d %H:%M")] for t in data]
    window["-TABLE-"].update(values=table_data)

# Primera carga
refresh_table()

while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, "-EXIT-"):
        break

    if event == "-ADD-":
        try:
            sym = values["-SYM-"].strip().upper()
            qty = float(values["-QTY-"])
            prc = float(values["-PRC-"])
            dt = values["-DT-"].strip()
            date = datetime.strptime(dt, "%Y-%m-%d %H:%M") if dt else None
            trade = create_trade(sym, qty, prc, date)
            window["-OUTPUT-"].print(f"→ Añadido: {trade}")
            refresh_table()
        except Exception as e:
            window["-OUTPUT-"].print(f"⚠ Error al añadir: {e}")

    elif event == "-METRICS-":
        df = compute_metrics()
        if df.empty:
            window["-OUTPUT-"].print("→ No hay datos para métricas.")
        else:
            window["-OUTPUT-"].print("\nMétricas:")
            window["-OUTPUT-"].print(df.to_string(index=False))

    elif event == "-EXPORT-":
        try:
            # Reusa la función de main
            from src.main import export_to_excel
            export_to_excel()
            window["-OUTPUT-"].print("✔ Exportación completada.")
        except Exception as e:
            window["-OUTPUT-"].print(f"⚠ Error exportando: {e}")

window.close()