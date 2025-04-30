import streamlit as st
from datetime import datetime
import uuid

# Banco de dados em memória
if "fornecedores" not in st.session_state:
    st.session_state.fornecedores = []

if "produtos" not in st.session_state:
    st.session_state.produtos = []

if "estoque" not in st.session_state:
    st.session_state.estoque = []

if "pedidos" not in st.session_state:
    st.session_state.pedidos = []

# Funções
def cadastrar_fornecedor(nome, contato):
    st.session_state.fornecedores.append({
        "id": str(uuid.uuid4())[:8],
        "nome": nome,
        "contato": contato
    })
    st.success("Fornecedor cadastrado!")

def cadastrar_produto(nome, categoria):
    st.session_state.produtos.append({
        "id": str(uuid.uuid4())[:8],
        "nome": nome,
        "categoria": categoria
    })
    st.success("Produto cadastrado!")

def registrar_estoque(produto_id, tipo, quantidade):
    st.session_state.estoque.append({
        "id": str(uuid.uuid4())[:8],
        "produto_id": produto_id,
        "tipo": tipo,  # entrada ou saída
        "quantidade": quantidade,
        "data": datetime.now()
    })
    st.success("Movimentação registrada!")

def criar_pedido(produto_id, fornecedor_id, quantidade):
    st.session_state.pedidos.append({
        "id": str(uuid.uuid4())[:8],
        "produto_id": produto_id,
        "fornecedor_id": fornecedor_id,
        "quantidade": quantidade,
        "data": datetime.now(),
        "status": "Pendente"
    })
    st.success("Pedido criado!")

def get_nome_produto(pid):
    for p in st.session_state.produtos:
        if p["id"] == pid:
            return p["nome"]
    return "?"

def get_nome_fornecedor(fid):
    for f in st.session_state.fornecedores:
        if f["id"] == fid:
            return f["nome"]
    return "?"

# Interface
st.title("🔗 Supply Chain Management (SCM)")

menu = st.sidebar.radio("Menu", ["Fornecedores", "Produtos", "Estoque", "Pedidos", "Visão Geral"])

if menu == "Fornecedores":
    st.header("📦 Fornecedores")
    with st.form("form_forn"):
        nome = st.text_input("Nome do Fornecedor")
        contato = st.text_input("Contato (email, telefone...)")
        if st.form_submit_button("Cadastrar"):
            cadastrar_fornecedor(nome, contato)

    st.subheader("Lista de Fornecedores")
    for f in st.session_state.fornecedores:
        st.write(f"- {f['nome']} ({f['contato']})")

elif menu == "Produtos":
    st.header("📋 Produtos")
    with st.form("form_prod"):
        nome = st.text_input("Nome do Produto")
        categoria = st.text_input("Categoria")
        if st.form_submit_button("Cadastrar"):
            cadastrar_produto(nome, categoria)

    st.subheader("Lista de Produtos")
    for p in st.session_state.produtos:
        st.write(f"- {p['nome']} ({p['categoria']})")

elif menu == "Estoque":
    st.header("📊 Movimentação de Estoque")
    if not st.session_state.produtos:
        st.warning("Cadastre produtos primeiro.")
    else:
        produto = st.selectbox("Produto", st.session_state.produtos, format_func=lambda x: x["nome"])
        tipo = st.radio("Tipo", ["Entrada", "Saída"])
        qtd = st.number_input("Quantidade", min_value=1, step=1)
        if st.button("Registrar"):
            registrar_estoque(produto["id"], tipo.lower(), qtd)

    st.subheader("📦 Histórico de Estoque")
    for mov in st.session_state.estoque[::-1]:
        st.write(f"{mov['data'].strftime('%d/%m/%Y %H:%M')} - {mov['tipo'].capitalize()} de {mov['quantidade']} unid. do produto {get_nome_produto(mov['produto_id'])}")

elif menu == "Pedidos":
    st.header("📑 Pedidos de Compra")
    if not st.session_state.fornecedores or not st.session_state.produtos:
        st.warning("Cadastre fornecedores e produtos.")
    else:
        produto = st.selectbox("Produto", st.session_state.produtos, format_func=lambda x: x["nome"])
        fornecedor = st.selectbox("Fornecedor", st.session_state.fornecedores, format_func=lambda x: x["nome"])
        qtd = st.number_input("Quantidade", min_value=1, step=1)
        if st.button("Criar Pedido"):
            criar_pedido(produto["id"], fornecedor["id"], qtd)

    st.subheader("📄 Lista de Pedidos")
    for p in st.session_state.pedidos[::-1]:
        st.write(f"{p['data'].strftime('%d/%m/%Y')} - Pedido {p['id']} | {p['quantidade']}x {get_nome_produto(p['produto_id'])} de {get_nome_fornecedor(p['fornecedor_id'])} | Status: {p['status']}")

elif menu == "Visão Geral":
    st.header("📈 Visão Geral de Estoque")
    estoque_total = {}
    for mov in st.session_state.estoque:
        pid = mov["produto_id"]
        if pid not in estoque_total:
            estoque_total[pid] = 0
        estoque_total[pid] += mov["quantidade"] if mov["tipo"] == "entrada" else -mov["quantidade"]

    for pid, saldo in estoque_total.items():
        st.write(f"🧺 {get_nome_produto(pid)}: **{saldo} unidades**")
