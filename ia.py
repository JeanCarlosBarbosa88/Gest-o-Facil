from banco import conectar
 
def produtos_mais_vendidos():
    conn = conectar()
    cur = conn.cursor()
 
    cur.execute("""
        SELECT produto, SUM(quantidade) as total
        FROM itens_venda
        GROUP BY produto
        ORDER BY total DESC
        LIMIT 5
    """)
 
    dados = cur.fetchall()
    conn.close()
 
    return dados
 