import requests

def consultarCidade(cidade):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={cidade}&units=metric&appid=271d1234d3f497eed5b1d80a07b3fcd1'
    resposta = requests.get(url).json()
    return resposta
