import requests
import pandas as pd
from bs4 import BeautifulSoup
import re

def extraer_nombre(url):
    match = re.search(r'/quote/([A-Z0-9.]+)', url)
    if match:
        return match.group(1)
    return None


def scrap():
    
    url = input('ingresela url de la pagina de yahoo finance: ')
    print(url)

    if not url.startswith('https:'):
        print('url invalida!')
        return
    
    nombre_accion = extraer_nombre(url)
    nombre_accion_str = f'{nombre_accion}_datos.csv'

    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Cache-Control': 'max-age=0',
    }   

    try:
        pagina = requests.get(url, headers= headers)

        if pagina.status_code != 200:
            print(f'error de la pagina. codigo de estado{pagina.status_code}')
            return
    
        soup = BeautifulSoup(pagina.content, 'html.parser')
        tabla = soup.find('table')

        if not tabla:
            print('no se ha encontrado la tabla ')
            return
        
        tabla = tabla.find_all('tr')[1:]

        data = []
        for fila in tabla:
            columnas = fila.find_all('td')
            fila_datos = [columna.get_text(strip=True) for columna in columnas]
            data.append(fila_datos)

        columnas = ['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
        df = pd.DataFrame(data, columns=columnas)
        df.to_csv(nombre_accion_str, index=False)

    except Exception as e:
        print(f"Ocurrió un error: {e}")

