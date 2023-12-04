#Autor Erik Luan 
#https://github.com/Smilke

from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from time import sleep

nav = webdriver.ChromeOptions()
nav.binary_location = '/usr/bin/chromium'  
driver = webdriver.Chrome(options=nav) 
driver.get('https://portaldatransparencia.gov.br/despesas/consulta?paginacaoSimples=true&tamanhoPagina=&offset=&direcaoOrdenacao=asc&de=01%2F01%2F2023&ate=30%2F11%2F2023&orgaos=OR26252&colunasSelecionadas=funcao%2CsubFuncao%2Cprograma%2Cacao%2CvalorDespesaPaga%2CorgaoVinculado%2CelementoDespesa&ordenarPor=funcao&direcao=asc')

# Inicialização da variável de controle para os títulos das colunas
titulo_v = False
    
# Loop principal para coletar dados de várias páginas
while True:
    # Encontrando o botão "Próximo" na página
    link = driver.find_element(By.ID, 'lista_next')
    
    # Obtendo o código-fonte HTML da página atual
    content = driver.page_source
    
    # Criando uma estrutura do HTML usando BeautifulSoup
    soup = BeautifulSoup(content, 'lxml')
    
    # Localizando a seção da página que contém os dados de gastos
    gastos = soup.find('tbody')
    
    # Verificando se o botão "Próximo" está desabilitado, indicando o fim das páginas
    verificador =  soup.find('li', {'class' : 'paginate_button next disabled'})
    
    # Abrindo o arquivo CSV para escrita
    with open('data.csv', 'a') as arquivo:
        # Verificando se os títulos das colunas ainda não foram escritos
        if not titulo_v:
            # Encontrando e escrevendo os títulos das colunas no arquivo CSV
            titulos = soup.find('thead')
            for titulo in titulos.find_all('tr'):
                for elemento in titulo.find_all('th'):
                    arquivo.write('"' + elemento.text.strip() + '",')
                arquivo.write('\n')
            # Alterando o valor de titulo_v para indicar que os títulos foram escritos
            titulo_v = True
                
        # Iterando sobre os elementos de gastos na página e escrevendo no arquivo CSV
        for gasto in gastos.find_all('tr'):
            for elemento in gasto.find_all('td'):
                if elemento.text.strip():
                    arquivo.write('"' + elemento.text.strip() + '",')
                else:  
                    arquivo.write('"",')
            arquivo.write('\n')
            
    # Verificando se chegou ao final das páginas e interrompendo o loop
    if verificador:
        break
    
    # Clicando no botão "Próximo" para ir para a próxima página e aguardando 1 segundo
    link.click()
    sleep(1)
    
driver.quit()