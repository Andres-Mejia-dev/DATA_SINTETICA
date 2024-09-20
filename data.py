import streamlit as st
from faker import Faker
from faker.providers import BaseProvider
import pandas as pd
from io import BytesIO

# Inicializa el objeto Faker con localización para Colombia
info_fake = Faker('es_CO')

# Diccionario que mapea los campos a funciones de Faker para generar datos falsos
campos_disponible = {
    'Nombre': info_fake.name,
    'Dirección': info_fake.address,
    'Correo electrónico': info_fake.email,
    'Celular': info_fake.phone_number,
    'Número de Tarjeta de Crédito': info_fake.credit_card_number,
    'Fecha vencimiento TC': info_fake.credit_card_expire,
    'Código de Verificación TC': info_fake.credit_card_security_code
}

# Función para generar datos sintéticos
def generar_data(fields, num_rows):
    # Crea un diccionario con las listas de datos generados para cada campo
    data = {field: [func() for _ in range(num_rows)] for field, func in fields.items()}
    # Convierte el diccionario a un DataFrame de pandas
    return pd.DataFrame(data)

# Título de la aplicación en Streamlit
st.title('Generador de Datos Sintéticos')
st.write('Seleccionar campos que desea generar y cantidad de datos')

# Selección de campos que el usuario desea generar
campos_seleccionados = st.multiselect(
    'Selecciona los campos',
    options=list(campos_disponible.keys()),
    default=list(campos_disponible.keys())
)

# Selección de la cantidad de filas de datos a generar
num_rows = st.number_input(
    'Cantidad de datos a generar', 
    min_value=1,
    max_value=500, 
    value=10
)

# Si el botón de "Generar Datos" es presionado
if st.button('Generar Datos'):
    # Filtra las funciones seleccionadas por el usuario
    selected_funcs = {field: campos_disponible[field] for field in campos_seleccionados}
    
    # Genera los datos en un DataFrame
    df = generar_data(selected_funcs, num_rows)

    # Crea un buffer en memoria para almacenar el archivo Excel
    output = BytesIO()
    
    # Escribe los datos en un archivo Excel usando xlsxwriter
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        writer.book.use_constant_memory = True  # Optimiza el uso de memoria
        df.to_excel(writer, index=False)  # Escribe el DataFrame en el archivo Excel
    
    output.seek(0)  # Coloca el puntero al inicio del archivo para la descarga

    # Muestra un mensaje de éxito en la interfaz
    st.success('Datos generados.')
    st.write(df)  # Muestra el DataFrame en la aplicación

    # Botón para descargar el archivo Excel
    st.download_button(
        label='Descargar Excel',
        data=output,
        file_name='Datos_sinteticos.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
