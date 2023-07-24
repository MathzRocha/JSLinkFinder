from colorama import init, Fore, Style
from modules import buscar_arquivos_js, buscar_palavras_em_js

init()


def imprimir_resultados(resultados):
    """
    Funçao utilizada para retornar os resultados
    :param resultados: parametro que vem retornado de outra funçao utilizada no código
    :return:
    """
    for palavra, ocorrencias in resultados.items():
        if ocorrencias:
            print(f"\n{Fore.GREEN}Palavra '{palavra}' encontrada em {len(ocorrencias)} ocorrências:{Style.RESET_ALL}")
            for url_js, conteudo_encontrado in ocorrencias:
                print(f"{Fore.CYAN}Link: {url_js}{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}Conteúdo encontrado: {conteudo_encontrado}{Style.RESET_ALL}\n")
        else:
            print(f"{Fore.RED}Palavra '{palavra}' não encontrada.{Style.RESET_ALL}")


if __name__ == "__main__":
    url_pagina = input("Digite a URL: ").strip().lower()

    links_js_encontrados = buscar_arquivos_js(url_pagina)

    if links_js_encontrados:
        print(f"\n{Fore.GREEN}Arquivos .js encontrados:{Style.RESET_ALL}")
        for link_js in links_js_encontrados:
            print(link_js)

        palavras_especificas = input(
            "\nDigite as palavras específicas separadas por vírgula (ou deixe em branco para buscar todas as palavras): ").split(
            ',')
        palavras_especificas = [palavra.strip() for palavra in palavras_especificas if palavra.strip()]

        if palavras_especificas:
            resultados = buscar_palavras_em_js(links_js_encontrados, palavras_especificas)
            imprimir_resultados(resultados)
        else:
            print("\nNenhuma palavra específica foi informada.")

    else:
        print(f"\n{Fore.RED}Nenhum arquivo .js encontrado.{Style.RESET_ALL}")
