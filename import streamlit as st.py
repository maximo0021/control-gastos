import streamlit as st
import pandas as pd
import os

st.title("💰 Mi Control de Gastos Personal")

# Cargar datos
archivo = "gastos.csv"
if os.path.exists(archivo):
    df = pd.read_csv(archivo)
else:
    df = pd.DataFrame(columns=["Concepto", "Monto", "Categoría", "Fecha"])

# Formulario para registrar gastos
st.subheader("Registrar Nuevo Gasto")
with st.form("form_gasto"):
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

# Mostrar tabla de gastos
st.subheader("Historial de Gastos")
if not df.empty:
    st.dataframe(df, use_container_width=True)
    total = df["Monto"].sum()
    st.metric(label="Total Gastado", value=f"${total:,.2f}")
else:
    st.info("No hay gastos registrados todavía.")