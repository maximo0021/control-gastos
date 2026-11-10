import streamlit as st
import pandas as pd
import os

st.title("💰 Mi Control de Gastos Personal")

# Archivo CSV de almacenamiento
archivo = "gastos.csv"

# Cargar datos o inicializar DataFrame con columnas seguras
if os.path.exists(archivo):
    try:
        df = pd.read_csv(archivo)
        # Verificar si las columnas esenciales existen
        columnas_requeridas = ["Concepto", "Monto", "Categoría", "Fecha"]
        if not all(col in df.columns for col in columnas_requeridas):
            df = pd.DataFrame(columns=columnas_requeridas)
    except Exception:
        df = pd.DataFrame(columns=["Concepto", "Monto", "Categoría", "Fecha"])
else:
    df = pd.DataFrame(columns=["Concepto", "Monto", "Categoría", "Fecha"])

# Formulario para registrar gastos
st.subheader("Registrar Nuevo Gasto")
with st.form("form_gasto", clear_on_submit=True):
    concepto = st.text_input("Concepto")
    monto = st.number_input("Monto", min_value=0.0, format="%.2f")
    categoria = st.selectbox("Categoría", ["Comida", "Transporte", "Servicios", "Entretenimiento", "Otros"])
    fecha = st.date_input("Fecha")
    
    submitted = st.form_submit_button("Guardar Gasto")
    if submitted and concepto:
        nuevo_gasto = pd.DataFrame([[concepto, monto, categoria, str(fecha)]], columns=["Concepto", "Monto", "Categoría", "Fecha"])
        df = pd.concat([df, nuevo_gasto], ignore_index=True)
        df.to_csv(archivo, index=False)
        st.success("¡Gasto guardado con éxito!")
        st.rerun()

# Mostrar tabla de gastos y total
st.subheader("Historial de Gastos")
if not df.empty and "Monto" in df.columns:
    st.dataframe(df, use_container_width=True)
    total = df["Monto"].sum()
    st.metric(label="Total Gastado", value=f"${total:,.2f}")
else:
    st.info("No hay gastos registrados todavía.")
