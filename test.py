import requests

# Ruta al archivo que deseas subir
file_path = r"excel_contratos.csv"

# URL del endpoint
url = "https://excel-gpt-action.onrender.com/upload/excel"
# url = "http://192.168.3.246:5000/upload/excel"

# Abrir el archivo en modo binario
with open(file_path, 'rb') as f:
    files = {'file': (file_path, f)}
    response = requests.post(url, files=files)

# Imprimir la respuesta
print(response.status_code)
print(response.json())
