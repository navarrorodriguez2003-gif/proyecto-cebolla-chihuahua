import streamlit as st
import pandas as pd
import datetime
import altair as alt
import streamlit.components.v1 as components

# 1. CONFIGURACIÓN INICIAL Y CARGA DE DATOS
st.set_page_config(page_title="Sistema Cebolla Chihuahua", layout="wide")

@st.cache_data
def cargar_csv():
    try:
        # Asegúrate de que el archivo se llame exactamente así
        data = pd.read_csv('datos_chihuahua.csv')
        data.columns = data.columns.str.strip().str.upper()
        return data
    except:
        return None

df = cargar_csv()

def leer_en_voz_alta(texto):
    js_code = f"<script>var msg = new SpeechSynthesisUtterance('{texto}'); msg.lang = 'es-MX'; window.speechSynthesis.speak(msg);</script>"
    components.html(js_code, height=0)

# --- LÓGICA DE NAVEGACIÓN POR BOTONES ---
if 'pagina' not in st.session_state:
    st.session_state.pagina = "Menu"

def ir_a(nombre_pagina):
    st.session_state.pagina = nombre_pagina

# --- PANTALLA A: MENÚ PRINCIPAL (BOTONES GIGANTES) ---
if st.session_state.pagina == "Menu":
    st.title("🍀 Bienvenido al Sistema Agrícola")
    st.subheader("Seleccione una opción para comenzar:")
    
    col_menu = st.columns(1)[0]
    with col_menu:
        if st.button("🏠 INICIO: INFORMACIÓN GENERAL DEL CULTIVO", use_container_width=True):
            ir_a("Inicio")
        if st.button("📚 BIBLIOTECA DE ENFERMEDADES Y FOTOS", use_container_width=True):
            ir_a("Biblioteca")
        if st.button("📈 PREDICCIÓN DE CLIMA Y LLUVIA", use_container_width=True):
            ir_a("Predicciones")
        if st.button("📊 ANÁLISIS HISTÓRICO (LÍNEAS)", use_container_width=True):
            ir_a("Historico")
        if st.button("🌱 DIAGNÓSTICO DE SALUD DE LA PLANTA", use_container_width=True):
            ir_a("Salud")
        if st.button("⚖️ EQUIDAD Y SESGOS DE GÉNERO", use_container_width=True):
            ir_a("Equidad")

# --- PANTALLA B: CONTENIDO DE LAS SECCIONES ---
else:
    # Botón de retorno siempre visible arriba
    if st.button("⬅️ VOLVER AL MENÚ PRINCIPAL", use_container_width=True):
        ir_a("Menu")
        st.rerun()

    # --- SECCIÓN 1: INICIO ---
    if st.session_state.pagina == "Inicio":
        st.title("🏠 Guía Detallada de Cultivo")
        st.image("https://www.gob.mx/cms/uploads/article/main_image/81414/cebolla.jpg", caption="Campo de Chihuahua")
        st.write("""
        La cebolla es un cultivo fundamental en Chihuahua. Para un buen bulbo, se requiere:
        - **Clima:** Fresco al inicio (13-24°C) y calor al final para cerrar el bulbo.
        - **Suelo:** Suelto, con buen drenaje para evitar pudriciones.
        - **Riego:** Constante sin encharcar; se reduce antes de la cosecha.
        - **Variedades:** Blancas y amarillas de día corto son las más exitosas.
        """)
        c1, c2 = st.columns(2)
        with c1:
            st.success("## 🌱 1. SIEMBRA (Oct - Dic)")
            st.image("https://cdn-icons-png.flaticon.com/512/3105/3105075.png", width=120)
        with c2:
            st.warning("## 📦 2. COSECHA (May - Jul)")
            st.image("https://cdn-icons-png.flaticon.com/512/1514/1514935.png", width=120)

    # --- SECCIÓN 2: BIBLIOTECA (7 ENFERMEDADES) ---
    elif st.session_state.pagina == "Biblioteca":
        st.title("📚 Galería de Enfermedades y Soluciones")
        enf = {
            "1. Mancha Púrpura": ["https://extension.unr.edu/publications/photos/4014_1.jpg", "Solución: Fungicida de cobre y evitar mojar hojas."],
            "2. Mildiú Velloso": ["https://puebla.com.mx/wp-content/uploads/2021/04/mildiu-cebolla.jpg", "Solución: Mejorar aireación y eliminar restos enfermos."],
            "3. Raíz Rosada": ["https://vegetablemdonline.ppath.cornell.edu/Images/Onion/Onion_Pink/PinkRoot_Onion1.jpg", "Solución: Rotación de cultivos por 5 años."],
            "4. Podredumbre Blanca": ["https://www.agrowin.com.mx/wp-content/uploads/2019/07/pudricion-blanca-cebolla.jpg", "Solución: Solarización del suelo."],
            "5. Carboncillo": ["https://www.agricolajerez.com/wp-content/uploads/2019/10/aspergillus-niger-cebolla.jpg", "Solución: Secado profundo al sol."],
            "6. Trips": ["https://www.koppert.mx/globalassets/mexico/images/pest-and-diseases/pest/trips/trips-en-cebolla.jpg", "Solución: Trampas amarillas."],
            "7. Pudrición Blanda": ["https://infoagronomo.net/wp-content/uploads/2018/01/Pudricion-bacteriana-cebolla.jpg", "Solución: Evitar golpes al bulbo."]
        }
        for nombre, datos in enf.items():
            with st.expander(f"🔍 {nombre}"):
                st.image(datos[0], use_container_width=True)
                st.info(f"**✅ {datos[1]}**")

    # --- SECCIÓN 3: PREDICCIONES ---
    elif st.session_state.pagina == "Predicciones":
        st.title("📈 Pronóstico Mensual")
        if df is not None:
            mes_n = datetime.datetime.now().month
            if st.button("📢 ESCUCHAR CLIMA Y LLUVIA", use_container_width=True):
                datos = df[df['MES'] == mes_n]
                t_med, t_max = datos['T_MED'].mean(), datos['T_MED'].max()
                lluvia = "Alta" if mes_n in [7, 8, 9] else "Baja"
                mm = "40-70 mm" if lluvia == "Alta" else "5-10 mm"
                res_v = f"Promedio: {t_med:.1f}°C | Máxima: {t_max:.1f}°C | Lluvia: {lluvia} ({mm})"
                st.success(res_v)
                leer_en_voz_alta(f"Promedio de {t_med:.1f} grados y lluvia {lluvia}.")

    # --- SECCIÓN 4: ANÁLISIS HISTÓRICO ---
    elif st.session_state.pagina == "Historico":
        st.title("📊 Análisis de Años Pasados")
        if df is not None:
            año = st.selectbox("Elija el año:", sorted(df['YEAR'].unique(), reverse=True))
            chart = alt.Chart(df[df['YEAR'] == año]).mark_line(point=True, color='red').encode(
                x='MES:N', y='T_MED:Q', tooltip=['MES', 'T_MED']).properties(height=400)
            st.altair_chart(chart, use_container_width=True)

    # --- SECCIÓN 5: SALUD (DIAGNÓSTICO) ---
    elif st.session_state.pagina == "Salud":
        st.title("🌱 Diagnóstico Rápido")
        s1 = st.checkbox("Manchas moradas"); s2 = st.checkbox("Raíces rosas"); s3 = st.checkbox("Polvo negro")
        s4 = st.checkbox("Algodoncillo blanco"); s5 = st.checkbox("Tallo aguado y mal olor")
        if st.button("⚡ ANALIZAR", use_container_width=True):
            if s2: st.warning("Diagnóstico: Raíz Rosada.")
            elif s3: st.warning("Diagnóstico: Carboncillo.")
            elif s1: st.warning("Diagnóstico: Mancha Púrpura.")
            elif s4: st.warning("Diagnóstico: Podredumbre Blanca.")
            elif s5: st.warning("Diagnóstico: Pudrición Blanda.")
            else: st.success("Planta sana.")

    # --- SECCIÓN 6: EQUIDAD DE GÉNERO ---
    elif st.session_state.pagina == "Equidad":
        st.title("⚖️ Género y Agricultura")
        st.write("Identificación y prevención de sesgos en el campo:")
        with st.expander("❓ ¿Qué son los sesgos?"):
            st.write("Prejuicios que invisibilizan el trabajo de la mujer en la cosecha o empaque.")
        with st.expander("🛡️ Cómo prevenirlos"):
            st.info("Incluir a las mujeres en capacitaciones técnicas y toma de decisiones financieras.")
        if st.button("📢 ESCUCHAR RESUMEN", use_container_width=True):
            leer_en_voz_alta("Reconocer el trabajo de las mujeres mejora la economía de Chihuahua.")