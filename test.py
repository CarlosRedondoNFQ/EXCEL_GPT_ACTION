import requests
import base64

# Ruta al archivo que deseas subir
file_path = r"excel_contratos.csv"

# URL del endpoint
url = "https://excel-gpt-action.onrender.com/upload/excel"
# url = "http://192.168.3.246:5000/upload/excel"

# # Abrir el archivo en modo binario
# with open(file_path, 'rb') as f:
#     files = {'file': (file_path, f)}
#     response = requests.post(url, files=files)

# # Imprimir la respuesta
# print(response.status_code)
# print(response.json())


# Leer y codificar el archivo en Base64
with open(file_path, 'rb') as file:
    file_data = base64.b64encode(file.read()).decode('utf-8')

# Crear el payload JSON
payload = {
    'file_name': 'archivo.xlsx',
    'file_data': file_data
}

# Enviar la solicitud POST
response = requests.post(url, json=payload)

# Imprimir la respuesta
print(response.status_code)
print(response.json())
