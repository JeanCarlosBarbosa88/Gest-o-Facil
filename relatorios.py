from banco import conectar
 
def vendas_totais():
    conn = conectar()
    cur = conn.cursor()
 
    cur.execute("SELECT SUM(total) FROM vendas")
    total = cur.fetchone()[0]
 
    conn.close()
    return total or 0
 
def vendas_por_pagamento():
    conn = conectar()
    cur = conn.cursor()
 
    cur.execute("""
        SELECT pagamento, SUM(total)
        FROM vendas
        GROUP BY pagamento
    """)
 
    dados = cur.fetchall()
    conn.close()
    return dados
 