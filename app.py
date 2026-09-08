"""Aplicación Streamlit para explorar el dataset vehicles_us.csv."""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st


# -----------------------------------------------------------------------------
# Configuración general
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Explorador de vehículos usados",
    page_icon="🚘",
    layout="wide",
)

sns.set_theme(style="whitegrid")
RUTA_CSV = Path(__file__).resolve().parent / "vehicles_us.csv"


@st.cache_data
def cargar_datos(ruta: Path) -> pd.DataFrame:
    """Carga y prepara el archivo CSV para su análisis en la aplicación."""
    if not ruta.exists():
        raise FileNotFoundError(
            f"No se encontró el archivo '{ruta.name}' en la carpeta de la aplicación."
        )

    datos = pd.read_csv(ruta)

    columnas_requeridas = {
        "price",
        "model",
        "type",
        "condition",
        "odometer",
        "model_year",
    }
    faltantes = columnas_requeridas.difference(datos.columns)
    if faltantes:
        raise ValueError(
            "El archivo no contiene las columnas requeridas: "
            + ", ".join(sorted(faltantes))
        )

    datos = datos.copy()
    datos["date_posted"] = pd.to_datetime(
        datos.get("date_posted"), errors="coerce"
    )

    # Limpieza sencilla y consistente con el EDA.
    for columna in datos.select_dtypes(include="object").columns:
        datos[columna] = datos[columna].str.strip()

    datos["paint_color"] = datos.get("paint_color", pd.Series(index=datos.index)).fillna(
        "Desconocido"
    )
    datos["is_4wd"] = datos.get(
        "is_4wd", pd.Series(index=datos.index)).fillna(0)

    # Imputación básica para que los filtros y gráficos no fallen.
    for columna in ["model_year", "cylinders", "odometer"]:
        if columna in datos.columns and datos[columna].isna().any():
            datos[columna] = datos[columna].fillna(datos[columna].median())

    return datos


def filtrar_datos(datos: pd.DataFrame) -> pd.DataFrame:
    """Construye los controles laterales y devuelve el subconjunto seleccionado."""
    st.sidebar.header("Filtros")
    st.sidebar.caption("Ajusta la información que deseas analizar.")

    modelos = sorted(datos["model"].dropna().unique().tolist())
    tipos = sorted(datos["type"].dropna().unique().tolist())

    modelos_seleccionados = st.sidebar.multiselect(
        "Modelo",
        options=modelos,
        placeholder="Selecciona uno o varios modelos",
    )
    tipos_seleccionados = st.sidebar.multiselect(
        "Tipo de vehículo",
        options=tipos,
        placeholder="Selecciona uno o varios tipos",
    )

    precio_minimo = int(datos["price"].min())
    precio_maximo = int(datos["price"].max())
    rango_precio = st.sidebar.slider(
        "Rango de precio (USD)",
        min_value=precio_minimo,
        max_value=precio_maximo,
        value=(precio_minimo, precio_maximo),
    )

    ordenar_por = st.sidebar.selectbox(
        "Ordenar resultados por",
        options=["Precio", "Modelo", "Tipo"],
    )
    orden_ascendente = st.sidebar.checkbox(
        "Orden ascendente",
        value=True,
        help="Activado: menor a mayor o de A a Z.",
    )

    filtrados = datos.loc[
        datos["price"].between(rango_precio[0], rango_precio[1])
    ].copy()

    if modelos_seleccionados:
        filtrados = filtrados[filtrados["model"].isin(modelos_seleccionados)]
    if tipos_seleccionados:
        filtrados = filtrados[filtrados["type"].isin(tipos_seleccionados)]

    mapa_orden = {"Precio": "price", "Modelo": "model", "Tipo": "type"}
    return filtrados.sort_values(
        by=mapa_orden[ordenar_por], ascending=orden_ascendente
    )


def mostrar_indicadores(datos: pd.DataFrame) -> None:
    """Muestra métricas resumidas del subconjunto filtrado."""
    columnas = st.columns(4)
    columnas[0].metric("Anuncios", f"{len(datos):,}")
    columnas[1].metric("Precio mediano", f"USD {datos['price'].median():,.0f}")
    columnas[2].metric("Odómetro mediano",
                       f"{datos['odometer'].median():,.0f} mi")
    columnas[3].metric("Modelos distintos", f"{datos['model'].nunique():,}")


def grafico_barras(datos: pd.DataFrame, categoria: str):
    """Crea un gráfico de proporciones para una variable categórica."""
    proporciones = (
        datos[categoria]
        .fillna("Desconocido")
        .value_counts(normalize=True)
        .head(12)
        .sort_values()
        .mul(100)
    )

    figura, eje = plt.subplots(figsize=(8, 5))
    proporciones.plot(kind="barh", ax=eje, color="#2878B5")
    eje.set_title(f"Proporción por {categoria}")
    eje.set_xlabel("Proporción de anuncios (%)")
    eje.set_ylabel(categoria.replace("_", " ").title())
    figura.tight_layout()
    return figura


def histograma(datos: pd.DataFrame, variable: str):
    """Crea un histograma para la variable numérica seleccionada."""
    figura, eje = plt.subplots(figsize=(8, 5))
    sns.histplot(datos[variable].dropna(), bins=35,
                 kde=True, ax=eje, color="#F28E2B")
    eje.set_title(f"Distribución de {variable}")
    eje.set_xlabel(variable.replace("_", " ").title())
    eje.set_ylabel("Frecuencia")
    figura.tight_layout()
    return figura


def grafico_dispersion(datos: pd.DataFrame, variable_x: str, variable_y: str):
    """Crea un scatterplot con una muestra para mantener buena respuesta visual."""
    muestra = datos.sample(min(8_000, len(datos)), random_state=42)
    figura, eje = plt.subplots(figsize=(8, 5))
    sns.scatterplot(
        data=muestra,
        x=variable_x,
        y=variable_y,
        hue="type",
        alpha=0.45,
        legend=False,
        ax=eje,
    )
    eje.set_title(f"{variable_y.title()} frente a {variable_x.title()}")
    eje.set_xlabel(variable_x.replace("_", " ").title())
    eje.set_ylabel(variable_y.replace("_", " ").title())
    figura.tight_layout()
    return figura


# -----------------------------------------------------------------------------
# Aplicación
# -----------------------------------------------------------------------------
st.title("🚘 Explorador interactivo de vehículos usados")
st.subheader("Convierte el EDA en decisiones visuales, rápidas y comparables")
st.write(
    "Filtra los anuncios por modelo, tipo y precio; después compara distribuciones "
    "y relaciones entre las variables más relevantes."
)

try:
    df = cargar_datos(RUTA_CSV)
except FileNotFoundError as error:
    st.error(str(error))
    st.info(
        "Coloca 'vehicles_us.csv' en la misma carpeta que 'app.py' y reinicia la app.")
    st.stop()
except (pd.errors.ParserError, UnicodeDecodeError) as error:
    st.error("El archivo existe, pero no pudo interpretarse como un CSV válido.")
    st.exception(error)
    st.stop()
except ValueError as error:
    st.error(str(error))
    st.stop()
except Exception as error:
    st.error("Ocurrió un error inesperado al cargar los datos.")
    st.exception(error)
    st.stop()

try:
    df_filtrado = filtrar_datos(df)

    if df_filtrado.empty:
        st.warning(
            "No existen registros para la combinación de filtros seleccionada.")
        st.stop()

    mostrar_indicadores(df_filtrado)

    st.divider()
    st.header("Vista de los datos")
    mostrar_tabla = st.checkbox("Mostrar las primeras 5 filas", value=False)
    if mostrar_tabla:
        st.dataframe(df_filtrado.head(
            5), use_container_width=True, hide_index=True)

    st.divider()
    st.header("Visualizaciones interactivas")

    izquierda, derecha = st.columns(2, gap="large")

    with izquierda:
        st.subheader("Composición y distribución")
        tipo_grafico = st.selectbox(
            "Visualización",
            options=["Gráfico de barras", "Histograma"],
            key="tipo_grafico",
        )

        if tipo_grafico == "Gráfico de barras":
            categoria = st.selectbox(
                "Categoría",
                options=["type", "condition", "fuel",
                         "transmission", "paint_color"],
            )
            fig_izquierda = grafico_barras(df_filtrado, categoria)
        else:
            variable_histograma = st.selectbox(
                "Variable numérica",
                options=["price", "odometer", "model_year",
                         "days_listed", "cylinders"],
            )
            fig_izquierda = histograma(df_filtrado, variable_histograma)

        st.pyplot(fig_izquierda, use_container_width=True)
        plt.close(fig_izquierda)

    with derecha:
        st.subheader("Relación entre variables")
        variables_numericas = [
            "price",
            "odometer",
            "model_year",
            "days_listed",
            "cylinders",
        ]
        variable_x = st.selectbox(
            "Variable del eje X",
            options=variables_numericas,
            index=1,
        )
        variable_y = st.selectbox(
            "Variable del eje Y",
            options=variables_numericas,
            index=0,
        )

        if variable_x == variable_y:
            st.info(
                "Selecciona variables diferentes para observar una relación útil.")
        else:
            fig_derecha = grafico_dispersion(
                df_filtrado, variable_x, variable_y)
            st.pyplot(fig_derecha, use_container_width=True)
            plt.close(fig_derecha)

    with st.expander("Resumen del subconjunto filtrado"):
        st.dataframe(
            df_filtrado[
                ["price", "model_year", "cylinders", "odometer", "days_listed"]
            ].describe().T,
            use_container_width=True,
        )

except Exception as error:
    st.error("No fue posible actualizar la visualización con los filtros actuales.")
    st.exception(error)
