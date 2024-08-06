import folium
import pyproj

def gerar_mapa(dados_onibus):
    """Gera um mapa HTML com a localização dos ônibus."""
    mapa_onibus = folium.Map(location=[-15.8, -48], zoom_start=14)

    # Definir projeções
    proj_4326 = pyproj.CRS("EPSG:4326")  # WGS 84 (latitude e longitude)
    proj_3857 = pyproj.CRS("EPSG:3857")  # Web Mercator (usado pelo Leaflet)

    for onibus in dados_onibus['features']:
        coordenadas_4326 = onibus['geometry']['coordinates']  # Coordenadas originais em EPSG:4326

        # Converter coordenadas para EPSG:3857 (metros)
        coordenadas_3857 = pyproj.transform(proj_4326, proj_3857, 
                                            coordenadas_4326[0], coordenadas_4326[1])

        # Converter coordenadas de metros para graus decimais usando pyproj.transform
        coordenadas_folium = pyproj.transform(proj_3857, proj_4326, *coordenadas_3857)

        # Inverter a ordem das coordenadas para (latitude, longitude)
        coordenadas_folium = [coordenadas_folium[1], coordenadas_folium[0]] 

        print(f"Coordenadas (Graus Decimais): {coordenadas_folium}")
        popup_text = f"Linha: {onibus['properties']['numerolinha']}<br>IMEI: {onibus['properties']['imei']}"
        print(f"Popup: {popup_text}")
        marker = folium.Marker(location=coordenadas_folium, popup=popup_text)
        print(f"Adicionando marcador: {marker}")
        marker.add_to(mapa_onibus)

    return mapa_onibus._repr_html_()