import psutil
import psycopg2
import time
from datetime import datetime


conn_params = {
    "host": "localhost",
    "database": "dblucas",
    "user": "postgres",
    "password": "1234",
    "port": "5432"
}

def criar_tabela():
    with psycopg2.connect(**conn_params) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS sistema_logs (
                    id SERIAL PRIMARY KEY,
                    data_hora TIMESTAMP,
                    cpu_percent FLOAT,
                    memoria_percent FLOAT
                );
            """)
        conn.commit()

def salvar_metricas():
    cpu = psutil.cpu_percent(interval=1)
    memoria = psutil.virtual_memory().percent
    agora = datetime.now()

    with psycopg2.connect(**conn_params) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO sistema_logs (data_hora, cpu_percent, memoria_percent) VALUES (%s, %s, %s)",
                (agora, cpu, memoria)
            )
        conn.commit()
    print(f"[{agora}] CPU: {cpu}% | RAM: {memoria}% - Salvo!")

if __name__ == "__main__":
    criar_tabela()
    print("Monitorando... (Ctrl+C para parar)")
    try:
        while True:
            salvar_metricas()
            time.sleep(5)
    except KeyboardInterrupt:
        print("\nMonitoramento encerrado.")
