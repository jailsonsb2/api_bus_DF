from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
import requests
import mapa
from geopy.distance import geodesic
from datetime import datetime, timedelta

app = FastAPI(title="API Localização de Ônibus")

@app.get("/", response_class=RedirectResponse)
async def redirect_to_docs():
    """Redireciona para a documentação da API."""
    return RedirectResponse(url="/docs")

@app.get("/onibus/{linha}")
def get_onibus_by_linha(linha: str):
    """Retorna os dados dos ônibus da linha especificada."""
    url = f"https://geoserver.semob.df.gov.br/geoserver/semob/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=semob%3AUltima%20Posicao%20Transmitida&outputFormat=application%2Fjson&CQL_FILTER=numerolinha='{linha}'"
    #response = requests.get(url, verify=False)   REMOVA verify=False EM PRODUÇÃO!
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data['features']:  # Verificar se há ônibus na linha
            return data
        else:
            raise HTTPException(status_code=404, detail=f"Nenhum ônibus encontrado na linha {linha}.")
    else:
        raise HTTPException(status_code=500, detail="Erro ao obter dados do servidor.")

@app.get("/mapa/{linha}", response_class=HTMLResponse)
def get_mapa_onibus(linha: str):
    """Gera um mapa com a localização dos ônibus da linha."""
    dados_onibus = get_onibus_by_linha(linha)
    if dados_onibus:
        mapa_html = mapa.gerar_mapa(dados_onibus)
        return HTMLResponse(content=mapa_html, status_code=200)
    else:
        raise HTTPException(status_code=404, detail=f"Nenhum ônibus encontrado na linha {linha}.")


@app.get("/horarios/ida/{linha}")
async def get_horarios_ida(linha: str):
    """Retorna os horários programados para a ida da linha especificada."""
    url = f"https://geoserver.semob.df.gov.br/geoserver/semob/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=semob%3AViagens%20Programadas%20por%20Linha&outputFormat=application%2Fjson&CQL_FILTER=cd_linha='{linha}' AND cs_sentido='I'"
    #response = requests.get(url, verify=False)   REMOVA verify=False EM PRODUÇÃO!
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        horarios = processar_horarios(data)
        return horarios
    else:
        raise HTTPException(status_code=500, detail="Erro ao obter dados do servidor.")



@app.get("/horarios/volta/{linha}")
async def get_horarios_volta(linha: str):
    """Retorna os horários programados para a volta da linha especificada."""
    url = f"https://geoserver.semob.df.gov.br/geoserver/semob/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=semob%3AViagens%20Programadas%20por%20Linha&outputFormat=application%2Fjson&CQL_FILTER=cd_linha='{linha}' AND cs_sentido='V'"
    #response = requests.get(url, verify=False)   REMOVA verify=False EM PRODUÇÃO!
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        horarios = processar_horarios(data)
        return horarios
    else:
        raise HTTPException(status_code=500, detail="Erro ao obter dados do servidor.")

def processar_horarios(data):
    """Processa os dados do WFS e retorna os horários organizados por hora e minuto, 
       com as horas em ordem crescente, horários completos (HH:MM) e informações adicionais.
    """
    horarios = {
        'domingo': {},
        'segunda': {},
        'terca': {},
        'quarta': {},
        'quinta': {},
        'sexta': {},
        'sabado': {},
    }
    for viagem in data['features']:
        hora_prevista = viagem['properties']['hora_prevista'].strip()
        
        # Extrair hora e minuto, garantindo que a hora seja "00" para meia-noite
        hora, minuto = hora_prevista.split(':') if ':' in hora_prevista else ('00', hora_prevista[1:])  

        horario_completo = f"{hora}:{minuto}"  # Criar o horário completo (HH:MM)

        # Informações adicionais
        info_adicionais = {
            'operadora': viagem['properties']['nm_operadora'],
            'denominacao_linha': viagem['properties']['tx_denominacao_linha'],
            'sentido': viagem['properties']['cs_sentido']
            # Adicione outros campos conforme necessário
        }

        for dia in horarios:
            if viagem['properties'][f'st_{dia}'] == 'S':
                if hora not in horarios[dia]:
                    horarios[dia][hora] = []
                horarios[dia][hora].append({
                    'horario': horario_completo,
                    'info': info_adicionais
                })  # Adicionar horário completo e informações adicionais

    # Ordenar as horas em ordem crescente para cada dia da semana
    for dia in horarios:
        horarios[dia] = dict(sorted(horarios[dia].items()))

    return horarios
   

@app.get("/tempo-chegada/{linha}/{latitude}/{longitude}")
async def get_tempo_chegada(linha: str, latitude: float, longitude: float):
    """Retorna o ônibus mais próximo da linha especificada e o tempo estimado de chegada."""
    dados_onibus = get_onibus_by_linha(linha)

    if not dados_onibus['features']:
        raise HTTPException(status_code=404, detail=f"Nenhum ônibus encontrado na linha {linha}.")

    onibus_mais_proximo, tempo_chegada, hora_estimada = calcular_tempo_chegada(
        latitude, longitude, dados_onibus
    )

    return {
        "onibus": onibus_mais_proximo['properties'],
        "tempo_chegada_minutos": tempo_chegada,
        "hora_estimada": hora_estimada.strftime('%H:%M')
    }

def calcular_tempo_chegada(latitude, longitude, dados_onibus):
    """Calcula o tempo estimado de chegada do ônibus mais próximo."""
    distancia_minima = float('inf')
    onibus_mais_proximo = None

    for onibus in dados_onibus['features']:
        onibus_latitude = onibus['properties']['latitude']
        onibus_longitude = onibus['properties']['longitude']

        distancia = geodesic((latitude, longitude), (onibus_latitude, onibus_longitude)).kilometers

        if distancia < distancia_minima:
            distancia_minima = distancia
            onibus_mais_proximo = onibus

    onibus_velocidade = onibus_mais_proximo['properties']['velocidade']

    # Calcular o tempo estimado em horas
    tempo_estimado_horas = distancia_minima / onibus_velocidade

    # Converter o tempo estimado para minutos
    tempo_estimado_minutos = tempo_estimado_horas * 60

    # Adicionar 20% de tempo adicional para paradas e variações de velocidade
    tempo_adicional_minutos = tempo_estimado_minutos * 0.20
    tempo_total_minutos = tempo_estimado_minutos + tempo_adicional_minutos

    # Calcular a hora estimada de chegada
    hora_chegada = datetime.now() + timedelta(minutes=tempo_total_minutos)

    return onibus_mais_proximo, tempo_total_minutos, hora_chegada