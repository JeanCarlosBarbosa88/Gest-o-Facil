def gerar_cupom(nome_cliente, dados_cliente, itens, total, pagamento, entrada=0, parcelas=0):
    with open("cupom.txt", "w", encoding="utf-8") as f:
        f.write("====== CUPOM FISCAL ======\n")
        f.write(f"Cliente: {nome_cliente}\n")
        f.write(f"Telefone: {dados_cliente['telefone']}\n")
        f.write(f"CPF: {dados_cliente['cpf']}\n")
        f.write(f'Endereço:{dados_cliente['endereco']}\n')
        f.write("-" * 30 + "\n")

        for item in itens:
            f.write(f"{item['nome']} x{item['quantidade']} = R${item['preco'] * item['quantidade']:.2f}\n")

        f.write("-" * 30 + "\n")
        f.write(f"TOTAL: R${total:.2f}\n")
        f.write(f"Pagamento: {pagamento}\n")

        # 🔥 NOVA PARTE (PARCELAMENTO)
        if pagamento == "parcelado":
            f.write(f"Entrada: R${entrada:.2f}\n")
            restante = total - entrada

            if parcelas > 0:
                valor_parcela = restante / parcelas
                f.write(f"Parcelado em {parcelas}x de R${valor_parcela:.2f}\n")

        f.write("\nObrigado pela preferência!\n")