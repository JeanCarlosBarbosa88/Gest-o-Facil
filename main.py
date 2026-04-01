import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from banco import conectar, criar_tabela
from cupom import gerar_cupom
from relatorios import vendas_totais
from ia import produtos_mais_vendidos
from grafico import grafico_vendas
from backup import fazer_backup
import os

# Cria as tabelas
criar_tabela()


# Funções auxiliares
def formatar_cpf(cpf):
    cpf = ''.join(filter(str.isdigit, cpf))
    if len(cpf) != 11:
        return cpf
    return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"

def formatar_telefone(telefone):
    telefone = ''.join(filter(str.isdigit, telefone))
    if len(telefone) == 11:
        return f"({telefone[:2]}) {telefone[2:7]}-{telefone[7:]}"
    elif len(telefone) == 10:
        return f"({telefone[:2]}) {telefone[2:6]}-{telefone[6:]}"
    else:
        return telefone

# Configuração da janela
janela = tk.Tk()
janela.rowconfigure(0, weight=1)
janela.columnconfigure(0, weight=1)
janela.title("TK Conceito Modas")
janela.geometry("1090x760")
janela.resizable(False,False)
janela.configure(bg="#46E7CC")

def mudar_tema():
    current = style.theme_use()
    new_theme = "alt" if current == "clam" else "clam"
    style.theme_use(new_theme)

# Estilo ttk moderno
style = ttk.Style()
style.theme_use("clam")

# CORES PADRÃO
BG = "#f4f6f9"
PRIMARY = "#2563eb"
SUCCESS = "#16a34a"
DANGER = "#dc2626"
CARD = "#ffffff"
TEXT = "#1f2937"

janela.configure(bg=BG)

# Notebook
style.configure("TNotebook", background=BG, borderwidth=0)
style.configure("TNotebook.Tab",
                padding=[15, 8],
                font=("Segoe UI", 10, "bold"),
                background="#e5e7eb")
style.map("TNotebook.Tab",
          background=[("selected", PRIMARY)],
          foreground=[("selected", "white")])

# Labels
style.configure("TLabel",
                background=BG,
                font=("Segoe UI", 10),
                foreground=TEXT)

# Botões modernos
style.configure("Primary.TButton",
                background=PRIMARY,
                foreground="white",
                font=("Segoe UI", 10, "bold"),
                padding=8)

style.map("Primary.TButton",
          background=[("active", "#1d4ed8")])

style.configure("Success.TButton",
                background=SUCCESS,
                foreground="white",
                font=("Segoe UI", 10, "bold"),
                padding=8)

style.configure("Danger.TButton",
                background=DANGER,
                foreground="white",
                font=("Segoe UI", 10, "bold"),
                padding=8)

# Entradas
style.configure("TEntry",
                padding=6,
                font=("Segoe UI", 10))

style.configure("TCombobox",
                padding=6,
                font=("Segoe UI", 10))


# Tenta carregar logo
logo_path = "logo.png"
if os.path.exists(logo_path):
    logo_img = tk.PhotoImage(file=logo_path)
    logo_label = tk.Label(janela, image=logo_img, bg="#f5f5f5")
    logo_label.grid(pady=5)
else:
    tk.Label(janela, text="TK CONCEITO MODAS", font=("Hevetica", 15, "bold"), bg="#46E7CC", fg="#6240df").grid(pady=10)

lbl_aviso = ttk.Label(janela, text="", font=("Arial", 9, "bold"), background="#f5f5f5")
lbl_aviso.grid(pady=2)

# Abas
abas = ttk.Notebook(janela)
abas.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

# CLIENTES                                  
aba_clientes = ttk.Frame(abas)
aba_clientes.columnconfigure(0, weight=1)
abas.add(aba_clientes, text="  Clientes  ")

def campo(parent, label, row, column):
    frame = ttk.Frame(parent)
    frame.grid(row=row, column=column, padx=15, pady=8, sticky="ew")

    ttk.Label(frame, text=label).pack(anchor="w")

    entry = ttk.Entry(frame)
    entry.pack(fill="x", pady=3)

    return entry

form_cliente = tk.Frame(aba_clientes, bg=CARD, bd=1, relief="solid")
form_cliente.grid(row=0, column=0, padx=30, pady=20, sticky="ew")

form_cliente.columnconfigure(0, weight=1)
form_cliente.columnconfigure(1, weight=1)

entry_nome_cliente = campo(form_cliente, "Nome", 0, 0)
entry_cpf          = campo(form_cliente, "CPF", 0, 1)
entry_tel          = campo(form_cliente, "Telefone", 2, 0)
entry_email        = campo(form_cliente, "Email", 2, 1)
entry_endereco     = campo(form_cliente, "Endereço", 4, 0)

def cadastrar_cliente():
    nome     = entry_nome_cliente.get().strip()
    cpf      = formatar_cpf(entry_cpf.get())
    telefone = formatar_telefone(entry_tel.get())
    endereco = entry_endereco.get().strip()

    if not nome or not cpf or not telefone:
        messagebox.showerror("Erro", "Preencha Nome, CPF e Telefone!")
        return

    conn = conectar()
    cur  = conn.cursor()
    cur.execute(
        "INSERT INTO clientes (nome, cpf, telefone, endereco) VALUES (?, ?, ?, ?)",
        (nome, cpf, telefone, endereco)
    )
    conn.commit()
    conn.close()

    for e in [entry_nome_cliente, entry_cpf, entry_tel, entry_email, entry_endereco]:
        e.delete(0, tk.END)

    messagebox.showinfo("OK", f"Cliente '{nome}' cadastrado com sucesso!")

ttk.Button(aba_clientes, text="Cadastrar Cliente", command=cadastrar_cliente).grid(pady=10)

   
# PRODUTOS
aba_produtos = ttk.Frame(abas)
abas.add(aba_produtos, text="  Produtos  ")

form_produto = ttk.Frame(aba_produtos)
form_produto.grid(sticky="ew", padx=20, pady=10)

entry_nome_prod = campo(form_produto, "Nome do produto", 0, 0)
entry_categoria = campo(form_produto, "Categoria", 0, 1)
entry_preco     = campo(form_produto, "Preço (R$)", 2, 0)
entry_estoque   = campo(form_produto, "Estoque (quantidade)", 2, 1)

TAMANHOS_DISPONIVEIS = ["PP", "P", "M", "G", "GG", "XG",
                        "34", "36", "38", "40", "42", "44", "46", "48",
                        "Único"]

ttk.Label(form_produto, text="Tamanhos disponíveis (marque os que tem em estoque):").grid(row=4, column=0, columnspan=2, sticky="w", padx=20, pady=(10,0))

frame_tamanhos = ttk.Frame(form_produto)
frame_tamanhos.grid(row=5, column=0, columnspan=2, padx=20, pady=5, sticky="w")

tamanho_vars = {}
for i, tam in enumerate(TAMANHOS_DISPONIVEIS):
    var = tk.BooleanVar()
    tamanho_vars[tam] = var
    cb = ttk.Checkbutton(frame_tamanhos, text=tam, variable=var)
    cb.grid(row=i // 8, column=i % 8, sticky="w", padx=4, pady=2)

def cadastrar_produto():
    nome      = entry_nome_prod.get().strip()
    categoria = entry_categoria.get().strip()
    preco_txt = entry_preco.get().strip()
    estq_txt  = entry_estoque.get().strip()

    if not nome or not categoria or not preco_txt or not estq_txt:
        messagebox.showerror("Erro", "Preencha todos os campos do produto!")
        return

    try:
        preco   = float(preco_txt.replace(",", "."))
        estoque = int(estq_txt)
    except ValueError:
        messagebox.showerror("Erro", "Preço e Estoque devem ser números válidos!")
        return

    tamanhos_selecionados = [t for t, v in tamanho_vars.items() if v.get()]
    tamanhos_str = ", ".join(tamanhos_selecionados) if tamanhos_selecionados else "Único"

    conn = conectar()
    cur  = conn.cursor()
    cur.execute(
        "INSERT INTO produtos (nome, categoria, preco, estoque, tamanhos) VALUES (?, ?, ?, ?, ?)",
        (nome, categoria, preco, estoque, tamanhos_str)
    )
    conn.commit()
    conn.close()

    for e in [entry_nome_prod, entry_categoria, entry_preco, entry_estoque]:
        e.delete(0, tk.END)
    for v in tamanho_vars.values():
        v.set(False)

    messagebox.showinfo("OK", f"Produto '{nome}' cadastrado!\nTamanhos: {tamanhos_str}")

ttk.Button(aba_produtos, text="Cadastrar Produto", command=cadastrar_produto).grid(pady=10)

 
#  ABA VENDAS 
frame_vendas_container = ttk.Frame(abas)
abas.add(frame_vendas_container, text="  Vendas  ")

canvas_vendas = tk.Canvas(frame_vendas_container)
scrollbar = ttk.Scrollbar(frame_vendas_container, orient="vertical", command=canvas_vendas.yview)

frame_vendas = ttk.Frame(canvas_vendas)

frame_vendas.bind(
    "<Configure>",
    lambda e: canvas_vendas.configure(scrollregion=canvas_vendas.bbox("all"))
)

canvas_vendas.create_window((0, 0), window=frame_vendas, anchor="nw")

canvas_vendas.configure(yscrollcommand=scrollbar.set)
canvas_vendas.bind("<MouseWheel>", lambda e: canvas_vendas.yview_scroll(int(-1*(e.delta/120)), "units"))

frame_vendas_container.columnconfigure(0, weight=1)
frame_vendas_container.rowconfigure(0, weight=1)

canvas_vendas.grid(row=0, column=0, sticky="nsew")
scrollbar.grid(row=0, column=1, sticky="ns")

# Cliente
ttk.Label(frame_vendas, text="Cliente:").grid(row=0, column=0, sticky="w")
entry_cliente_busca = ttk.Entry(frame_vendas, width=20)
entry_cliente_busca.grid(row=0, column=1, padx=6)
entry_cliente_id = ttk.Entry(frame_vendas)  # fica oculto
entry_cliente_id.grid(row=0, column=99)

# Label para mostrar o cliente selecionado
lbl_cliente_selecionado = ttk.Label(frame_vendas, text="Nenhum cliente selecionado", foreground="red")
lbl_cliente_selecionado.grid(row=0, column=2, padx=10, sticky="w")

# Produto
ttk.Label(frame_vendas, text="Produto:").grid(row=1, column=0, sticky="w", pady=4)
entry_produto_busca = ttk.Entry(frame_vendas, width=20)
entry_produto_busca.grid(row=1, column=1, padx=6)
entry_id = ttk.Entry(frame_vendas)  #fica oculto
entry_id.grid(row=1, column=99)

# Tamanho
ttk.Label(frame_vendas, text="Tamanho:").grid(row=1, column=2, padx=(20,4))
tamanho_venda_var = tk.StringVar()
combo_tamanho_venda = ttk.Combobox(frame_vendas, textvariable=tamanho_venda_var, width=8,
                                   values=TAMANHOS_DISPONIVEIS)
combo_tamanho_venda.grid(row=1, column=3)

# Quantidade
ttk.Label(frame_vendas, text="Quantidade:").grid(row=2, column=0, sticky="w", pady=4)
entry_qtd = ttk.Entry(frame_vendas, width=10)
entry_qtd.grid(row=2, column=1, padx=6)

# FRAME DE INFORMAÇÕES DO PRODUTO
frame_info = ttk.Frame(frame_vendas)
frame_info.grid(row=3, column=0, columnspan=4, sticky="w", padx=6, pady=5)

lbl_produto_info = ttk.Label(frame_info, text="", foreground="#2e7d32")
lbl_produto_info.grid(row=0, column=0, sticky="w")

# Listas de busca
lista_busca_clientes = tk.Listbox(frame_vendas, height=4, width=80, relief="solid", borderwidth=1)
lista_busca_clientes.grid(pady=5)
lista_busca_produtos = tk.Listbox(frame_vendas, height=4, width=80, relief="solid", borderwidth=1)
lista_busca_produtos.grid(pady=5)

# Itens da venda
lista_itens = tk.Listbox(
    frame_vendas,
    width=80,
    height=8,
    bg="#ffffff",
    fg="#111827",
    font=("Segoe UI", 10),
    relief="flat",
    highlightthickness=1,
    highlightbackground="#d1d5db"
)

itens_venda = []

# Funções de busca e seleção
def buscar_cliente_nome(event=None):
    nome = entry_cliente_busca.get()
    if not nome:
        lista_busca_clientes.delete(0, tk.END)
        return
    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT id, nome, telefone FROM clientes WHERE nome LIKE ?", (f"%{nome}%",))
    resultados = cur.fetchall()
    conn.close()
    lista_busca_clientes.delete(0, tk.END)
    for r in resultados:
        lista_busca_clientes.insert(tk.END, f"{r[0]} | {r[1]} | {r[2]}")

def selecionar_cliente(event):
    if lista_busca_clientes.curselection():
        selecionado = lista_busca_clientes.get(tk.ACTIVE)
        partes = selecionado.split("|")
        cliente_id = partes[0].strip()
        cliente_nome = partes[1].strip()
        entry_cliente_id.delete(0, tk.END)
        entry_cliente_id.insert(0, cliente_id)
        lbl_cliente_selecionado.config(text=f"Cliente: {cliente_nome}", foreground="green")
        # Limpa a lista de busca para não ocupar espaço
        lista_busca_clientes.delete(0, tk.END)

def buscar_produto_nome(event=None):
    nome = entry_produto_busca.get()
    if not nome:
        lista_busca_produtos.delete(0, tk.END)
        return
    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT id, nome, preco, estoque FROM produtos WHERE nome LIKE ?", (f"%{nome}%",))
    resultados = cur.fetchall()
    conn.close()
    lista_busca_produtos.delete(0, tk.END)
    for r in resultados:
        lista_busca_produtos.insert(tk.END, f"{r[0]} | {r[1]} | R${r[2]} | Estoque: {r[3]}")

def selecionar_produto(event):
    if lista_busca_produtos.curselection():
        selecionado = lista_busca_produtos.get(tk.ACTIVE)
        partes = selecionado.split("|")
        entry_id.delete(0, tk.END)
        entry_id.insert(0, partes[0].strip())
        buscar_produto_info()

def buscar_produto_info(*_):
    pid = entry_id.get().strip()
    if not pid:
        lbl_produto_info.config(text="")
        return
    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT nome, preco, estoque, tamanhos FROM produtos WHERE id=?", (pid,))
    p = cur.fetchone()
    conn.close()
    if p:
        nome, preco, estoque, tamanhos = p
        lbl_produto_info.config(text=f"Produto: {nome}  |  R${preco:.2f}  |  Estoque: {estoque}  |  Tamanhos: {tamanhos}")
        tam_lista = [t.strip() for t in tamanhos.split(",")] if tamanhos else []
        combo_tamanho_venda["values"] = tam_lista
        if tam_lista:
            tamanho_venda_var.set(tam_lista[0])
    else:
        lbl_produto_info.config(text="Produto não encontrado")

def adicionar_item():
    pid = entry_id.get().strip()
    if not pid:
        messagebox.showerror("Erro", "Selecione um produto!")
        return
    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT nome, preco, estoque FROM produtos WHERE id=?", (pid,))
    produto = cur.fetchone()
    conn.close()
    if not produto:
        messagebox.showerror("Erro", "Produto não encontrado!")
        return
    nome, preco, estoque = produto
    try:
        qtd = int(entry_qtd.get())
    except ValueError:
        messagebox.showerror("Erro", "Quantidade inválida!")
        return
    if qtd <= 0:
        messagebox.showerror("Erro", "Quantidade deve ser maior que zero!")
        return
    if qtd > estoque:
        messagebox.showerror("Erro", f"Sem estoque suficiente! Disponível: {estoque}")
        return
    tamanho = tamanho_venda_var.get()
    itens_venda.append({
        "id": pid,
        "nome": nome,
        "quantidade": qtd,
        "preco": preco,
        "tamanho": tamanho
    })
    tam_info = f" [{tamanho}]" if tamanho else ""
    lista_itens.insert(tk.END, f"{nome}{tam_info}  x{qtd}  R${preco:.2f}  = R${preco*qtd:.2f}")
    
    # Limpa campos do produto
    entry_id.delete(0, tk.END)
    entry_qtd.delete(0, tk.END)
    tamanho_venda_var.set("")
    lbl_produto_info.config(text="")
    
    # Atualiza total
    atualizar_total()

# Bindings
entry_cliente_busca.bind("<KeyRelease>", buscar_cliente_nome)
lista_busca_clientes.bind("<<ListboxSelect>>", selecionar_cliente)
entry_produto_busca.bind("<KeyRelease>", buscar_produto_nome)
lista_busca_produtos.bind("<<ListboxSelect>>", selecionar_produto)
entry_id.bind("<FocusOut>", buscar_produto_info)
entry_id.bind("<Return>", buscar_produto_info)

ttk.Button(frame_vendas, text="+ Adicionar Item", command=adicionar_item).grid()

# Frame de pagamento
frame_pgto = ttk.LabelFrame(frame_vendas, text="Pagamento", padding=10)
frame_pgto.grid(sticky="ew", padx=20, pady=10)

# Opção de pagamento: à vista ou parcelado
tipo_pagamento = tk.StringVar(value="dinheiro")

ttk.Label(frame_pgto, text="Forma de pagamento:").grid(row=0, column=0, sticky="w")

formas = ["dinheiro", "pix", "credito", "debito", "parcelado"]

for i, forma in enumerate(formas):
    ttk.Radiobutton(
        frame_pgto,
        text=forma.capitalize(),
        variable=tipo_pagamento,
        value=forma
    ).grid(row=0, column=i+1, padx=5, sticky="w")
# Total da venda
ttk.Label(frame_pgto, text="Total da venda:").grid(row=1, column=0, sticky="w", pady=5)
lista_itens = tk.Listbox(
    frame_vendas,
    width=80,
    height=8,
    bg="#ffffff",
    fg="#111827",
    font=("Segoe UI", 10),
    relief="flat",
    highlightthickness=1,
    highlightbackground="#d1d5db"
)

def atualizar_total():
    total = sum(i["preco"] * i["quantidade"] for i in itens_venda)
    return total

# Campos para parcelado
frame_parcelado = ttk.Frame(frame_pgto)
frame_parcelado.grid(row=2, column=0, columnspan=2, sticky="ew", pady=5)

ttk.Label(frame_parcelado, text="Entrada (R$):").grid(row=0, column=0, sticky="w", padx=(0,10))
entry_entrada = ttk.Entry(frame_parcelado, width=10)
entry_entrada.grid(row=0, column=1, sticky="w")
entry_entrada.insert(0, "0.00")

ttk.Label(frame_parcelado, text="Nº Parcelas:").grid(row=1, column=0, sticky="w", padx=(0,10), pady=5)
entry_num_parcelas = ttk.Combobox(frame_parcelado, values=[1,2,3,4,5,6,8,10,12], width=8)
entry_num_parcelas.grid(row=1, column=1, sticky="w")
entry_num_parcelas.set(1)

ttk.Label(frame_parcelado, text="Intervalo (dias):").grid(row=2, column=0, sticky="w", padx=(0,10))
entry_intervalo = ttk.Combobox(frame_parcelado, values=[7,15,30,60,90], width=8)
entry_intervalo.grid(row=2, column=1, sticky="w")
entry_intervalo.set(30)

ttk.Label(frame_parcelado, text="1ª parcela:").grid(row=3, column=0, sticky="w", padx=(0,10), pady=5)
entry_data_prim = ttk.Entry(frame_parcelado, width=12)
entry_data_prim.grid(row=3, column=1, sticky="w")
entry_data_prim.insert(0, datetime.now().strftime("%d/%m/%Y"))

def mostrar_parcelas():
    total = atualizar_total()
    if tipo_pagamento.get() == "avista":
        frame_parcelado.grid_remove()
        return
    frame_parcelado.grid()
    try:
        entrada = float(entry_entrada.get().replace(",", "."))
        num = int(entry_num_parcelas.get())
        intervalo = int(entry_intervalo.get())
        data_str = entry_data_prim.get()
        data_prim = datetime.strptime(data_str, "%d/%m/%Y")
    except:
        messagebox.showerror("Erro", "Dados inválidos para simulação!")
        return
    restante = total - entrada
    if restante <= 0:
        messagebox.showinfo("Simulação", "Entrada maior ou igual ao total. Nenhuma parcela gerada.")
        return
    valor_parcela = restante / num
    texto = f"Valor de cada parcela: R$ {valor_parcela:.2f}\nDatas:\n"
    for i in range(num):
        data = data_prim + timedelta(days=i * intervalo)
        texto += f"  Parcela {i+1}: {data.strftime('%d/%m/%Y')}\n"
    messagebox.showinfo("Simulação de Parcelas", texto)

ttk.Button(frame_parcelado, text="Simular Parcelas", command=mostrar_parcelas).grid(row=4, column=0, columnspan=2, pady=5)

# Função para finalizar venda
def finalizar_venda():
    conn = None
    try:
        if not itens_venda:
            messagebox.showerror("Erro", "Adicione pelo menos um item!")
            return

        cliente_id = entry_cliente_id.get().strip()
        if not cliente_id:
            messagebox.showerror("Erro", "Selecione um cliente!")
            return

        total = sum(i["preco"] * i["quantidade"] for i in itens_venda)

        conn = conectar()
        cur = conn.cursor()

# Buscar cliente
        cur.execute("SELECT nome, telefone, cpf, endereco FROM clientes WHERE id=?", (cliente_id,))
        cliente = cur.fetchone()
        if not cliente:
            messagebox.showerror("Erro", "Cliente não encontrado!")
            return

        nome_cliente, telefone, cpf, endereco = cliente

        pagamento_tipo = tipo_pagamento.get()
        entrada = 0
        parcelas_num = 0
        restante = 0
        valor_parcela = 0

# PARCELAMENTO 
        if pagamento_tipo == "parcelado":
            entrada = float(entry_entrada.get().replace(",", "."))
            parcelas_num = int(entry_num_parcelas.get())
            intervalo = int(entry_intervalo.get())
            data_prim = datetime.strptime(entry_data_prim.get(), "%d/%m/%Y")

            restante = total - entrada
            if restante > 0:
                valor_parcela = restante / parcelas_num

        # SALVAR VENDA        
        cur.execute("""
            INSERT INTO vendas (cliente_id, data, total, pagamento, entrada, parcelas_total)
            VALUES (?, datetime('now'), ?, ?, ?, ?)
        """, (cliente_id, total, pagamento_tipo, entrada, parcelas_num))

        venda_id = cur.lastrowid

# SALVAR ITENS + ESTOQUE 
        for item in itens_venda:
            cur.execute("""
                INSERT INTO itens_venda (venda_id, produto_id, quantidade, preco)
                VALUES (?, ?, ?, ?)
            """, (venda_id, item["id"], item["quantidade"], item["preco"]))

            cur.execute("""
                UPDATE produtos
                SET estoque = estoque - ?
                WHERE id = ?
            """, (item["quantidade"], item["id"]))
# PARCELAS
        if pagamento_tipo == "parcelado" and restante > 0:
            for i in range(parcelas_num):
                data_venc = data_prim + timedelta(days=i * intervalo)

                cur.execute("""
                    INSERT INTO parcelas (venda_id, cliente_id, numero, valor, data_vencimento)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    venda_id,
                    cliente_id,
                    i + 1,
                    valor_parcela,
                    data_venc.strftime("%Y-%m-%d")
                ))

        conn.commit()

# CUPOM
        gerar_cupom(
            nome_cliente,
            {"telefone": telefone, "cpf": cpf, "endereco": endereco},
            itens_venda,
            total,
            pagamento_tipo,
            entrada,
            parcelas_num
        )

        messagebox.showinfo("Sucesso", f"Venda salva com sucesso!\nTotal: R$ {total:.2f}")

# LIMPAR TELA
        lista_itens.delete(0, tk.END)
        itens_venda.clear()
        entry_cliente_id.delete(0, tk.END)
        entry_cliente_busca.delete(0, tk.END)
        lbl_cliente_selecionado.config(text="Nenhum cliente selecionado", foreground="red")

        atualizar_total()

    except Exception as e:
        if conn:
            conn.rollback()
        messagebox.showerror("Erro", str(e))

    finally:
        if conn:
            conn.close()

ttk.Button(frame_vendas, text="✔ Finalizar Venda", command=finalizar_venda).grid(pady=10)

# LISTA CLIENTES 
aba_clientes_lista = ttk.Frame(abas)
abas.add(aba_clientes_lista, text="  Lista Clientes  ")
ttk.Label(aba_clientes_lista, text="Clientes e total gasto", font=("Arial", 11, "bold")).grid(pady=8)
lista_clientes = tk.Listbox(aba_clientes_lista, width=90, height=18, relief="solid", borderwidth=1)
lista_clientes.grid(padx=20, pady=5)

def carregar_clientes():
    conn = conectar()
    cur = conn.cursor()
    cur.execute("""
        SELECT c.id, c.nome, c.cpf, c.telefone, COALESCE(SUM(v.total), 0)
        FROM clientes c
        LEFT JOIN vendas v ON c.id = v.cliente_id
        GROUP BY c.id, c.nome
        ORDER BY c.nome
    """)
    dados = cur.fetchall()
    conn.close()
    lista_clientes.delete(0, tk.END)
    for cid, nome, cpf, tel, total in dados:
        lista_clientes.insert(
            tk.END,
            f"[{cid}]  {nome:<25}  CPF: {cpf}  Tel: {tel}  |  Gasto: R${total:.2f}"
        )
ttk.Button(aba_clientes_lista, text="Atualizar Lista", command=carregar_clientes).grid(pady=8)

def excluir_cliente():
    if not lista_clientes.curselection():
        return

    selecionado = lista_clientes.get(tk.ACTIVE)
    cid = selecionado.split("]")[0].replace("[", "")

    conn = conectar()
    cur = conn.cursor()
    cur.execute("DELETE FROM clientes WHERE id=?", (cid,))
    conn.commit()
    conn.close()

    carregar_clientes()
    messagebox.showinfo("OK", "Cliente excluído!")
ttk.Button(aba_clientes_lista, text="Excluir Cliente", command=excluir_cliente).grid() 

#  ABA LISTA PRODUTO
aba_produtos_lista = ttk.Frame(abas)
abas.add(aba_produtos_lista, text="  Lista Produtos  ")
ttk.Label(aba_produtos_lista, text="Produtos em estoque", font=("Arial", 11, "bold")).grid(pady=8)
lista_produtos_lb = tk.Listbox(aba_produtos_lista, width=100, height=18, relief="solid", borderwidth=1)
lista_produtos_lb.grid(padx=20, pady=5)

def carregar_produtos():
    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT id, nome, categoria, preco, estoque, tamanhos FROM produtos ORDER BY nome")
    dados = cur.fetchall()
    conn.close()
    lista_produtos_lb.delete(0, tk.END)
    for pid, nome, cat, preco, estoque, tamanhos in dados:
        lista_produtos_lb.insert(
            tk.END,
            f"[{pid}]  {nome:<25}  {cat:<15}  R${preco:>7.2f}  Estoque:{estoque:>4}  Tam: {tamanhos}"
        )
ttk.Button(aba_produtos_lista, text="Atualizar Lista", command=carregar_produtos).grid(pady=8)

def excluir_produto():
    if not lista_produtos_lb.curselection():
        return

    selecionado = lista_produtos_lb.get(tk.ACTIVE)
    pid = selecionado.split("]")[0].replace("[", "")

    conn = conectar()
    cur = conn.cursor()
    cur.execute("DELETE FROM produtos WHERE id=?", (pid,))
    conn.commit()
    conn.close()

    carregar_produtos()
    messagebox.showinfo("OK", "Produto excluído!")
ttk.Button(aba_produtos_lista, text="Excluir Produto", command=excluir_produto).grid()

#  RELATÓRIOS
aba_rel = ttk.Frame(abas)
abas.add(aba_rel, text="  Relatórios  ")

def ver_relatorio():
    total = vendas_totais()
    top   = produtos_mais_vendidos()
    texto = f"Total vendido: R${total:.2f}\n\nTop 5 produtos mais vendidos:\n"
    for p in top:
        texto += f"  • {p[0]}  —  {p[1]} unidades\n"
    messagebox.showinfo("Relatorio", texto)

ttk.Button(aba_rel, text="Ver Relatorio", command=ver_relatorio).grid(pady=10)
ttk.Button(aba_rel, text="Ver Grafico de Vendas", command=grafico_vendas).grid(pady=10)
ttk.Button(aba_rel, text="Fazer Backup", command=fazer_backup).grid(pady=10)

# FIADO / PARCELAS
aba_fiado = ttk.Frame(abas)
abas.add(aba_fiado, text="  Parcelas  ")
lista_parcelas = tk.Listbox(aba_fiado, width=100, height=18, relief="solid", borderwidth=1)
lista_parcelas.grid(padx=20, pady=10)

def carregar_parcelas():
    conn = conectar()
    cur = conn.cursor()
    cur.execute("""
        SELECT p.id, c.nome, p.valor, p.data_vencimento, p.status, p.numero, p.venda_id
        FROM parcelas p
        JOIN clientes c ON p.cliente_id = c.id
        ORDER BY p.data_vencimento ASC
    """)
    dados = cur.fetchall()
    conn.close()
    lista_parcelas.delete(0, tk.END)
    for pid, nome, valor, data, status, num, venda_id in dados:
        lista_parcelas.insert(
            tk.END,
            f"[{pid}] {nome} | Parcela {num} | R${valor:.2f} | Venc: {data} | {status}"
        )
    atualizar_label_aviso()  
    
def verificar_vencimentos():
    hoje = datetime.now().date()
    daqui_5 = hoje + timedelta(days=5)
    daqui_1 = hoje + timedelta(days=1)
    
    conn = conectar()
    cur = conn.cursor()
    cur.execute("""
        SELECT p.id, c.nome, p.valor, p.data_vencimento, p.numero
        FROM parcelas p
        JOIN clientes c ON p.cliente_id = c.id
        WHERE p.status = 'PENDENTE'
          AND date(p.data_vencimento) BETWEEN date(?) AND date(?)
        ORDER BY p.data_vencimento ASC
    """, (hoje.strftime("%Y-%m-%d"), daqui_5.strftime("%Y-%m-%d")))
    todas = cur.fetchall()
    conn.close()
    
    venc_5 = [p for p in todas if datetime.strptime(p[3], "%Y-%m-%d").date() <= daqui_5]
    venc_1 = [p for p in todas if datetime.strptime(p[3], "%Y-%m-%d").date() == daqui_1]
    return venc_5, venc_1

def mostrar_avisos():
    venc_5, venc_1 = verificar_vencimentos()
    msg = ""
    if venc_1:
        msg += "⚠️ PARCELAS VENCENDO AMANHÃ:\n"
        for p in venc_1:
            msg += f"  • {p[1]} - Parcela {p[4]} - R$ {p[2]:.2f} (vence {p[3]})\n"
    if venc_5:
        if msg:
            msg += "\n"
        msg += "📆 PARCELAS VENCENDO NOS PRÓXIMOS 5 DIAS:\n"
        for p in venc_5:
            if p not in venc_1:
                msg += f"  • {p[1]} - Parcela {p[4]} - R$ {p[2]:.2f} (vence {p[3]})\n"
    if msg:
        messagebox.showwarning("Aviso de Vencimento", msg)

def atualizar_label_aviso():
    venc_5, venc_1 = verificar_vencimentos()
    total = len(venc_5) + len(venc_1)
    if total > 0:
        lbl_aviso.config(text=f"⚠️ {total} parcela(s) próxima(s) do vencimento!", foreground="red")
    else:
        lbl_aviso.config(text="✅ Nenhuma parcela próxima do vencimento.", foreground="green")

def pagar_parcela():
    if not lista_parcelas.curselection():
        messagebox.showerror("Erro", "Selecione uma parcela!")
        return
    selecionado = lista_parcelas.get(tk.ACTIVE)
    id_parcela = selecionado.split("]")[0].replace("[", "").strip()
    conn = conectar()
    cur = conn.cursor()
    cur.execute("UPDATE parcelas SET status = 'PAGO' WHERE id=?", (id_parcela,))
    conn.commit()
    conn.close()
    carregar_parcelas()
    messagebox.showinfo("Sucesso", "Parcela marcada como paga!")
    
# Após criar a aba aba_fiado (já existe), adicione este bind
def on_aba_selecionada(event):
    aba_atual = abas.tab(abas.select(), "text")
    if "Parcelas" in aba_atual:
        mostrar_avisos()
        atualizar_label_aviso()
    else:
        atualizar_label_aviso()

abas.bind("<<NotebookTabChanged>>", on_aba_selecionada)    

ttk.Button(aba_fiado, text="Atualizar Lista", command=carregar_parcelas).grid(pady=5)
ttk.Button(aba_fiado, text="Marcar Parcela Paga", command=pagar_parcela).grid(pady=5)



# Carrega listas iniciais
carregar_clientes()
carregar_produtos()
carregar_parcelas()
atualizar_total()
atualizar_label_aviso()  
mostrar_avisos()     

janela.mainloop()