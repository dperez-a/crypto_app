import sys
from datetime import datetime
import pandas as pd

from src.db import init_db
from src.services import (
    create_trade,
    get_all_trades,
    get_trades_by_symbol,
    compute_metrics,
)

DATA_DIR = 'data'
TRADES_FILE = f'{DATA_DIR}/trades.xlsx'
METRICS_FILE = f'{DATA_DIR}/metrics.xlsx'

def export_to_excel():
    # Exportar todas las operaciones
    trades = get_all_trades()
    if trades:
        df_trades = pd.DataFrame([{
            'id': t.id,
            'symbol': t.symbol,
            'quantity': t.quantity,
            'price': t.price,
            'date': t.date
        } for t in trades])
        df_trades.to_excel(TRADES_FILE, index=False)
        print(f"✔ Operaciones exportadas a {TRADES_FILE}")
    else:
        print("No hay operaciones para exportar.")

    # Exportar métricas
    df_metrics = compute_metrics()
    if not df_metrics.empty:
        df_metrics.to_excel(METRICS_FILE, index=False)
        print(f"✔ Métricas exportadas a {METRICS_FILE}")
    else:
        print("No hay métricas para exportar.")

def main():
    init_db()

    while True:
        print("\n=== Gestor de Portafolio ===")
        print("1. Listar operaciones")
        print("2. Añadir operación")
        print("3. Ver métricas")
        print("4. Exportar a Excel")
        print("5. Salir")
        choice = input("Selecciona una opción (1-5): ").strip()

        if choice == "1":
            trades = get_all_trades()
            if trades:
                for t in trades:
                    print(t)
            else:
                print("→ No hay operaciones registradas.")
        
        elif choice == "2":
            symbol = input("Símbolo (p.ej. TAO, ENAGAS): ").strip().upper()
            quantity = float(input("Cantidad: ").strip())
            price = float(input("Precio unitario: ").strip())
            date_str = input("Fecha (YYYY-MM-DD HH:MM) [enter para ahora]: ").strip()
            date = datetime.strptime(date_str, "%Y-%m-%d %H:%M") if date_str else None
            trade = create_trade(symbol, quantity, price, date)
            print(f"→ Operación creada: {trade}")

        elif choice == "3":
            df = compute_metrics()
            if df.empty:
                print("→ No hay datos para calcular métricas.")
            else:
                print("\nMétricas de portafolio:")
                print(df.to_markdown(index=False))

        elif choice == "4":
            export_to_excel()

        elif choice == "5":
            print("¡Hasta luego!")
            sys.exit(0)

        else:
            print("Opción no válida, intenta de nuevo.")

if __name__ == "__main__":
    main()