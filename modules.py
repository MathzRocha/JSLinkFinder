import requests
import re
from urllib.parse import urljoin

def buscar_arquivos_js(url):
    """
    Faz a busca por arquivos JS dentro uma URL
    :param url: Utiliza a URL informada pelo usuário para efetuar a requisiçao e a busca dos arquivos
    :return: retorna os links dos arquivos JS.
    """
    try:
        # realiza a request
        response = requests.get(url)

        # Verifica se retorna a requisiçao deu 200
        if response.status_code == 200:
            # Utiliza regex para encontrar links para arquivos .js
            padrao_js = r'(?:src=")(.*?\.js)'
            urls_js = re.findall(padrao_js, response.text)

            # Busca apenas por aquivos absolutos com .js
            links_absolutos_js = [urljoin(url, js) for js in urls_js]

            return links_absolutos_js

        else:
            print(f"Erro ao acessar a página. Status code: {response.status_code}")
            return []

    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {e}")
        return []


def buscar_palavras_em_js(urls_js, palavras):
    """
    Funcao utilizada para buscar paralavras definidas pelo usuario, dentro dos arquivos JS encontrados pelo script
    :param urls_js: Parametro passado pela funcao anterior, ele e usado para guardar as urls que estao os arquivos JS
    :param palavras: parametro que é fornecido pelo usuario, com as palavras que ele deseja buscar no JS
    :return: Retorna os resultados encontrados
    """
    resultados = {palavra: [] for palavra in palavras}

    for url_js in urls_js:
        try:
            # Faz a requisição HTTP para o arquivo .js
            response = requests.get(url_js)

            # Verifica se a requisição foi bem-sucedida
            if response.status_code == 200:
                conteudo_js = response.text

                # Procura por cada palavra específica no conteúdo do arquivo .js
                for palavra in palavras:
                    padrao = r'\b' + re.escape(palavra) + r'\b'
                    ocorrencias = re.finditer(padrao, conteudo_js, re.IGNORECASE)
                    for ocorrencia in ocorrencias:
                        inicio_ocorrencia = max(0, ocorrencia.start() - 20)
                        fim_ocorrencia = min(len(conteudo_js), ocorrencia.end() + 20)
                        conteudo_encontrado = conteudo_js[inicio_ocorrencia:fim_ocorrencia]
                        resultados[palavra].append((url_js, conteudo_encontrado))

            else:
                print(f"Erro ao acessar o arquivo .js. Status code: {response.status_code}")

        except requests.exceptions.RequestException as e:
            print(f"Erro na requisição: {e}")

    return resultados


def imprimir_resultados(resultados):
    for palavra, ocorrencias in resultados.items():
        if ocorrencias:
            print(f"\n{Fore.GREEN}Palavra '{palavra}' encontrada em {len(ocorrencias)} ocorrências:{Style.RESET_ALL}")
            for url_js, conteudo_encontrado in ocorrencias:
                print(f"{Fore.CYAN}Link: {url_js}{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}Conteúdo encontrado: {conteudo_encontrado}{Style.RESET_ALL}\n")
        else:
            print(f"{Fore.RED}Palavra '{palavra}' não encontrada.{Style.RESET_ALL}")