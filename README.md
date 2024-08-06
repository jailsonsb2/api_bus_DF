## API de Localização de Ônibus em Tempo Real (Distrito Federal)

Este projeto fornece uma API FastAPI que consulta dados de localização de ônibus em tempo real no Distrito Federal (Brasil) e os exibe em um mapa interativo. Os dados são obtidos do serviço Web Feature Service (WFS) da SEMOB (Secretaria de Mobilidade do DF).

### Funcionalidades:

* **Consulta por linha:** Obtém dados dos ônibus de uma linha específica.
* **Mapa interativo:** Gera um mapa HTML com a localização dos ônibus da linha consultada.
* **Tempo estimado de chegada:** Calcula o tempo estimado de chegada do ônibus mais próximo à sua localização.

### Endpoints:

* `/onibus/{linha}`: Retorna dados JSON dos ônibus da linha especificada.
* `/mapa/{linha}`: Gera um mapa HTML com a localização dos ônibus da linha especificada.
* `/tempo-chegada/{linha}/{latitude}/{longitude}`: Retorna o ônibus mais próximo da linha especificada, o tempo estimado de chegada em minutos e a hora estimada de chegada (HH:MM).

### Dependências:

* FastAPI
* uvicorn
* requests
* folium
* geopy
* pyproj

### Instalação:

1. Crie um ambiente virtual Python: `python -m venv env`
2. Ative o ambiente virtual: 
   - Windows: `env\Scripts\activate`
   - Linux/macOS: `source env/bin/activate`
3. Instale as dependências: `pip install -r requirements.txt`

### Execução:

1. Execute o servidor Uvicorn: `uvicorn main:app --reload`
2. Acesse a API em: http://localhost:8000

### Uso:

**Exemplo de requisição para a linha 0.809:**

* Dados JSON: `http://localhost:8000/onibus/0.809`
* Mapa: `http://localhost:8000/mapa/0.809`
* Tempo estimado de chegada (para latitude -15.7801 e longitude -47.9292): 
  `http://localhost:8000/tempo-chegada/0.809/-15.7801/-47.9292`

### Observações:

* A API utiliza dados em tempo real, então a localização dos ônibus e os tempos de chegada são apenas estimativas.
* **O código atual desabilita a verificação SSL para fins de teste. Remova `verify=False` em produção e implemente uma solução segura de verificação SSL.**

### Contribuições:

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.

### Licença:

MIT

---
