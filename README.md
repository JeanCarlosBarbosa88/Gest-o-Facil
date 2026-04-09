Sistema de Gestão para Loja de Roupas

Sistema desktop completo desenvolvido em Python para gerenciamento de lojas de roupas, com controle de clientes, produtos, vendas, estoque e parcelamento.

Funcionalidades

Cadastro de clientes,  
Cadastro de produtos com tamanhos (PP ao GG e numeração),  
Controle de estoque automático,  
Registro de vendas com múltiplos itens,  
Sistema de pagamento (dinheiro, pix, cartão e parcelado),  
Geração de parcelas,   
Controle de contas a receber,  
Relatórios de vendas,  
Identificação de produtos mais vendidos,  
Geração automática de cupom,  
Backup do sistema,  

Arquitetura do Sistema

O sistema foi desenvolvido utilizando **arquitetura modular**, separando responsabilidades em diferentes arquivos:

main.py = Interface e regras principais
banco.py = Conexão e estrutura do banco de dados
ia.py = Análise de produtos mais vendidos
relatorios.py = Geração de relatórios
cupom.py = Emissão de comprovantes
grafico.py = Visualização de dados
backup.py = Backup do banco

Essa abordagem facilita manutenção, escalabilidade e organização do código.

Banco de Dados usando SQLite

O sistema utiliza SQLite, garantindo leveza e fácil distribuição.

Principais tabelas:

clientes = dados dos clientes  
produtos = controle de estoque e preços  
vendas = registro das vendas  
itens_venda = itens vendidos  
parcelas = controle de pagamentos parcelados  
contas_receber = controle financeiro  

Interface Gráfica desenvolvida em TKinter

Com abas modernas
Navegação intuitiva
Organização de Formulários

Sistema roda com aplicação desktop leve, sendo ideal para pequenos negócios.

Conrtrole de Estoque
O estoque sempre é atualizado a cada venda automaticamente
Bloqueio de venda se não tem produto disponílvel pela quantidade

Parcelamento o sistema permite:
Definir entrada,
Números de parcelas,
intervalos de dias,
Geração automática de parcelas

Relatórios e Inteligência
Total de vendas
Top 5 produtos mais vendidos

Geração de Cupom
Após cada venda, o sistema automaticamente gera um comprovante contendo informações:
Dados cliente
Produtos comprados
Forma de pagamento
Parcelamento, quando tem

Forma usada Tecnologias
Python
TKinter
SQLite

Como Executar:
Clone o repositório
git clone https://github.com/seu-usuario/seu-repo

Acesse a pasta
cd seu-repo

Execute o sistema
python main.py

----------------------------------------------------------

Este projeto foi desenvolvido com objetivo de por em prática e aplicar
conceitos de desnvolvimento fullstack, criando uma solução real para pequeno comerciantes,
tendo a lógica de negócio e organização de sistema.
O sistema foi implementado e sendo utilizado em uma loja de roupas garantido o funcionamento
e trazendo agilidade para gestão do comércio.

Demonstração do sistema: https://youtu.be/3O3uQ_1JOu8
