## API de Informações de Ônibus em Tempo Real (Distrito Federal)

Este projeto fornece uma API FastAPI que consulta dados de ônibus em tempo real no Distrito Federal (Brasil), oferecendo informações sobre localização, horários e tempo estimado de chegada. Os dados são obtidos do serviço Web Feature Service (WFS) da SEMOB (Secretaria de Mobilidade do DF).

### Funcionalidades:

* **Consulta de localização em tempo real:** Obtém dados de localização dos ônibus de uma linha específica, exibindo-os em um mapa interativo.
* **Consulta de horários por linha e sentido:**  Retorna os horários programados para a ida e a volta de uma linha, organizados por hora e minuto, com informações adicionais sobre a operadora e a denominação da linha.
* **Estimativa de tempo de chegada:** Calcula o tempo estimado de chegada do ônibus mais próximo à sua localização, considerando a velocidade atual do ônibus e um tempo adicional para paradas e variações de velocidade.

### Endpoints:

* `/`: Redireciona para a documentação da API.
* `/onibus/{linha}`: Retorna dados JSON dos ônibus da linha especificada, incluindo localização, velocidade e outros detalhes.
* `/mapa/{linha}`: Gera um mapa HTML interativo com a localização dos ônibus da linha especificada.
* `/tempo-chegada/{linha}/{latitude}/{longitude}`: Retorna o ônibus mais próximo da linha especificada, o tempo estimado de chegada em minutos e a hora estimada de chegada (HH:MM).
* `/horarios/ida/{linha}`: Retorna os horários programados para a ida da linha especificada, organizados por hora e minuto, com informações adicionais.
* `/horarios/volta/{linha}`: Retorna os horários programados para a volta da linha especificada, organizados por hora e minuto, com informações adicionais.

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

* Localização em tempo real: 
    - Dados JSON: `http://localhost:8000/onibus/0.809`
    - Mapa: `http://localhost:8000/mapa/0.809`
* Tempo estimado de chegada (para latitude -15.7801 e longitude -47.9292): 
  `http://localhost:8000/tempo-chegada/0.809/-15.7801/-47.9292`
* Horários:
    - Ida: `http://localhost:8000/horarios/ida/0.809`
    - Volta: `http://localhost:8000/horarios/volta/0.809`


## Início Rápido com deploy no DigitalOcean

1. Clique no botão "Deploy to DO" logo abaixo.
2. Siga as instruções no Digital Ocean para implementar seu aplicativo.
3. Aproveite seu aplicativo FastAPI rodando na nuvem!

[![Deploy to DO](https://www.deploytodo.com/do-btn-blue.svg)](https://cloud.digitalocean.com/apps/new?repo=https://github.com/jailsonsb2/api_onibus_DF/tree/main)

Não tem uma conta? Ganhe um bônus de $200 para testar!

[![DigitalOcean Referral Badge](https://web-platforms.sfo2.cdn.digitaloceanspaces.com/WWW/Badge%203.svg)](https://www.digitalocean.com/?refcode=54a7273746ae&utm_campaign=Referral_Invite&utm_medium=Referral_Program&utm_source=badge)


### Observações:

* A API utiliza dados em tempo real, então a localização dos ônibus e os tempos de chegada são apenas estimativas.
* **O código atual desabilita a verificação SSL para fins de teste. Remova `verify=False` em produção e implemente uma solução segura de verificação SSL.**

### Contribuições:

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.

### Licença:

MIT
