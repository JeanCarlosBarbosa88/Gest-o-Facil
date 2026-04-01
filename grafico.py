import matplotlib.pyplot as plt
from banco import conectar
 
def grafico_vendas():
    conn = conectar()
    cur = conn.cursor()
 
    cur.execute("SELECT data, total FROM vendas")
 
    dados = cur.fetchall()
    conn.close()
 
    if not dados:
        plt.figure()
        plt.title("Sem dados de vendas ainda")
        plt.show()
        return
 
    datas = [str(d[0])[:10] for d in dados]
    valores = [d[1] for d in dados]
 
    plt.figure(figsize=(10, 5))
    plt.plot(datas, valores, marker='o', color='blue')
    plt.xticks(rotation=45)
    plt.title("Vendas por Data")
    plt.xlabel("Data")
    plt.ylabel("Valor (R$)")
    plt.tight_layout()
    plt.show()
 