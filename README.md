# Proyecto_S7
Proyecto final Sprint 7 curso 'Científico de Datos Tripleten' 

## Explorador interactivo de vehículos usados

Aplicación web desarrollada con **Streamlit** para explorar y visualizar anuncios de vehículos usados a partir del archivo `vehicles_us.csv`.

El proyecto transforma los principales resultados del análisis exploratorio realizado en `EDA_vehicles_us.ipynb` en una aplicación interactiva que permite filtrar registros, ordenar información y comparar variables mediante gráficos.

## Objetivo del proyecto

Construir una herramienta sencilla, visual y profesional que permita:

- Explorar anuncios de vehículos usados.
- Filtrar la información por modelo, tipo y rango de precio.
- Ordenar los resultados por precio, modelo o tipo.
- Consultar indicadores generales del subconjunto seleccionado.
- Analizar distribuciones de variables numéricas.
- Comparar proporciones de categorías.
- Explorar relaciones entre pares de variables numéricas.

## Estructura del proyecto

```text
vehicles_project/
├── app.py
├── vehicles_us.csv
├── EDA_vehicles_us.ipynb
├── README.md
└── requirements.txt
```

### Descripción de los archivos

- `app.py`: aplicación interactiva desarrollada con Streamlit.
- `vehicles_us.csv`: conjunto de datos con anuncios de vehículos usados.
- `EDA_vehicles_us.ipynb`: notebook con el análisis exploratorio de datos.
- `README.md`: documentación general del proyecto.
- `requirements.txt`: lista de dependencias necesarias para ejecutar la aplicación.

## Conjunto de datos

El archivo `vehicles_us.csv` contiene información sobre anuncios de vehículos usados.

Entre las variables principales se encuentran:

- `price`: precio anunciado del vehículo.
- `model_year`: año del modelo.
- `model`: modelo del vehículo.
- `condition`: condición declarada.
- `cylinders`: número de cilindros.
- `fuel`: tipo de combustible.
- `odometer`: kilometraje registrado.
- `transmission`: tipo de transmisión.
- `type`: tipo de vehículo.
- `paint_color`: color del vehículo.
- `is_4wd`: indicador de tracción 4x4.
- `date_posted`: fecha de publicación.
- `days_listed`: cantidad de días que permaneció publicado el anuncio.

## Funcionalidades de la aplicación

### Filtros interactivos

La barra lateral permite:

- Seleccionar uno o varios modelos.
- Seleccionar uno o varios tipos de vehículo.
- Definir un rango de precio.
- Elegir la columna utilizada para ordenar los resultados.
- Cambiar entre orden ascendente y descendente.

### Indicadores

La aplicación muestra indicadores que se actualizan según los filtros seleccionados:

- Cantidad de anuncios.
- Precio mediano.
- Odómetro mediano.
- Cantidad de modelos distintos.

### Tabla interactiva

Mediante una casilla de verificación, el usuario puede mostrar las primeras cinco filas del conjunto de datos filtrado.

### Visualizaciones

La aplicación permite alternar entre diferentes gráficos:

- Gráfico de barras con proporciones de categorías.
- Histograma de una variable numérica.
- Gráfico de dispersión entre dos variables numéricas.

Los gráficos se actualizan automáticamente con base en los filtros aplicados.

## Tecnologías utilizadas

- Python
- Streamlit
- pandas
- Matplotlib
- seaborn
- Jupyter Notebook

## Instalación

### 1. Clonar el repositorio

```bash
git clone <https://github.com/Jonarmiranda/Proyecto_S7.git>
cd Proyecto_S7
```

Si el proyecto todavía no se encuentra en GitHub, también puedes abrir directamente su carpeta desde Visual Studio Code.

### 2. Crear un entorno virtual

#### Windows con PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

#### Windows con Git Bash

```bash
python -m venv .venv
source .venv/Scripts/activate
```

#### macOS o Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar las dependencias

```bash
pip install -r requirements.txt
```

Si todavía no cuentas con `requirements.txt`, puedes instalar las dependencias directamente:

```bash
pip install streamlit pandas matplotlib seaborn
```

## Ejecución local

Asegúrate de que `app.py` y `vehicles_us.csv` se encuentren en la misma carpeta.

Ejecuta:

```bash
streamlit run app.py
```

Streamlit mostrará en la terminal la dirección local de la aplicación. Normalmente, el navegador se abrirá automáticamente.

## Detener la aplicación

Para detener el servidor de Streamlit, regresa a la terminal donde se está ejecutando y presiona:

```text
Ctrl + C
```

## Uso de la aplicación

1. Abre la aplicación en el navegador.
2. Selecciona los filtros desde la barra lateral.
3. Revisa los indicadores actualizados.
4. Activa la casilla para visualizar las primeras cinco filas.
5. Elige un gráfico de barras o un histograma en la columna izquierda.
6. Selecciona dos variables diferentes para generar el gráfico de dispersión.
7. Abre el resumen estadístico para consultar las medidas descriptivas del subconjunto filtrado.

## Manejo de errores

La aplicación contempla los siguientes escenarios:

- El archivo `vehicles_us.csv` no existe en la carpeta del proyecto.
- El CSV no puede interpretarse correctamente.
- Faltan columnas necesarias para construir los filtros o gráficos.
- La combinación de filtros no devuelve registros.
- Ocurre un error al actualizar una visualización.

Cuando se detecta alguno de estos problemas, la aplicación muestra un mensaje informativo en lugar de detenerse sin explicación.

## Metodología

El proyecto se desarrolló en dos etapas:

1. **Análisis exploratorio:** revisión de estructura, tipos de datos, valores faltantes, duplicados, distribuciones, valores atípicos y relaciones entre variables.
2. **Aplicación interactiva:** implementación de filtros, indicadores, tablas y visualizaciones para consultar los resultados de forma dinámica.

## Posibles mejoras

- Incorporar filtros por condición, combustible y año del modelo.
- Agregar una opción para descargar el subconjunto filtrado.
- Incluir visualizaciones temporales por fecha de publicación.
- Aplicar escalas o límites configurables para reducir el efecto visual de valores extremos.
- Añadir un modelo predictivo de precios en una etapa posterior.
- Publicar la aplicación en Streamlit Community Cloud.

## Autor

**Jonathan Rafael Miranda Primera**

Proyecto desarrollado como parte de una práctica de análisis de datos y creación de aplicaciones web con Python y Streamlit.

Link app: https://proyecto-s7-tqgt.onrender.com

## Estado del proyecto

Proyecto funcional para ejecución local. La aplicación puede seguir ampliándose con nuevas visualizaciones, filtros y componentes analíticos.

