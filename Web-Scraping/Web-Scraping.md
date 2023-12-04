
### O que é Web-Scraping:

Coletar informações de uma página web. Ou seja, por meio de uma linguagem de programação coletar as informações que estão na página e levar para a sua máquina. Pode ser feito **Web-Scraping** diretamente de um servidor de banco de dados via **API**.

### Python:

Bibliotecas necessárias para realizar **Web-Scraping** com python:

```bash
sudo apt-get install python3-bs4
sudo apt-get install python3-Selenium
sudo apt-get install python3-lxml
```

Com as devidas bibliotecas instaladas  podemos realizar os importes das classes:

```python
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from time import sleep
```

- `from selenium import webdriver`
		- Importa a classe `webdriver` do [[Selenium]], que permite a automação do navegador.

- `from selenium.webdriver.chrome.service import Service`
		- Importa a classe `Service` específica do Chrome para o [[Selenium]].

- `from bs4 import BeautifulSoup`
		- Importa a enumeração `By` para seleção de elementos no [[Selenium]].

- `from bs4 import BeautifulSoup`
		- Importa a classe `BeautifulSoup` do módulo `bs4` para fazer a análise do HTML.

- `from time import sleep`: Importa a função `sleep` do módulo `time` para adicionar pausas no código.

Será usado como exemplo o [detalhamento das despesas públicas](https://portaldatransparencia.gov.br/despesas/consulta?paginacaoSimples=true&tamanhoPagina=&offset=&direcaoOrdenacao=asc&de=01%2F01%2F2023&ate=30%2F11%2F2023&orgaos=OR26252&colunasSelecionadas=funcao%2CsubFuncao%2Cprograma%2Cacao%2CvalorDespesaPaga%2CorgaoVinculado%2CelementoDespesa&ordenarPor=funcao&direcao=asc), referente a **Universidade Federal de Campina Grande(UFCG)** do período de janeiro a novembro de 2023. Como será usado o [[Selenium]] será necessário algumas configurações:

> [!warning]- Sistema operacional
> Essas foram as configurações que utilizei em um ambiente Linux. Portanto, é possível que sejam necessárias outras especificações ao executar em outros sistemas operacionais.

```python
nav = webdriver.ChromeOptions()
nav.binary_location = '/usr/bin/chromium'
driver = webdriver.Chrome(options=nav)
driver.get('https://portaldatransparencia.gov.br/despesas/consulta?paginacaoSimples=true&tamanhoPagina=&offset=&direcaoOrdenacao=asc&de=01%2F01%2F2023&ate=30%2F11%2F2023&orgaos=OR26252&colunasSelecionadas=funcao%2CsubFuncao%2Cprograma%2Cacao%2CvalorDespesaPaga%2CorgaoVinculado%2CelementoDespesa&ordenarPor=funcao&direcao=asc')
```

- `nav = webdriver.ChromeOptions()`: permite configurar opções para o navegador Chrome quando estiver usando o [[Selenium]].

- `nav.binary_location = '/usr/bin/chromium'`: Define o local do binário do navegador (Chromium) que será usado. 

- `driver = webdriver.Chrome(options=nav)`: Inicializa o driver do Chrome usando as opções definidas anteriormente (`nav`).

- `driver.get('link')`: Navega para o URL especificado.

Explicação dos principais métodos do código:

```python
link = driver.find_element(By.ID, 'lista_next')
content = driver.page_source
soup = BeautifulSoup(content, 'lxml')# Apenas aceita essa linha
gastos = soup.find('tbody')
verificador = soup.find('li', {'class' : 'paginate_button next disabled'})
link.click()
driver.quit()
```

- `link = driver.find_element(By.ID, 'lista_next')`: Este trecho encontra o elemento na página que possui o ID **'lista_next'** e atribui isso à variável `link`.

   > [!note]- Algumas outras estratégias para busca 
> `By.ID`: Localiza um elemento pelo atributo ID.
> `By.NAME`: Localiza um elemento pelo atributo name.
> `By.XPATH`: Localiza elementos usando caminhos XPath.
> `By.LINK_TEXT`: Localiza um link pelo texto do link.
> `By.PARTIAL_LINK_TEXT`: Localiza um link por uma parte do texto do link.
> `By.TAG_NAME`: Localiza elementos pelo nome da tag HTML.
> `By.CLASS_NAME`: Localiza elementos pelo nome da classe.
> `By.CSS_SELECTOR`: Localiza elementos usando seletores CSS.

- `content = driver.page_source`: Isso obtém o código-fonte da página carregada pelo **WebDriver** e o armazena na variável `content`.
   
- `soup = BeautifulSoup(content, 'lxml')`: Aqui, o código-fonte da página é analisado pelo **BeautifulSoup** usando o parser **'lxml'** para criar uma árvore de análise (parse tree) que pode ser pesquisada para encontrar elementos HTML.
   
-  `gastos = soup.find('tbody')`: Isso procura e atribui à variável `gastos` a primeira ocorrência de um elemento **'tbody'** na página, presumivelmente onde estão listados os gastos.

  > [!node]- find_all()
> Todas as ocorrência de um elemento

- `verificador = soup.find('li', {'class' : 'paginate_button next disabled'})`: Esta linha tenta localizar um elemento '**li'** com a classe **'paginate_button next disabled'**, o que geralmente indica que o botão de próxima página está desativado. Isso pode ser útil para verificar se já estamos na última página ou se não há mais páginas para percorrer.
  
- `link.click()`: Este comando clica no elemento identificado anteriormente como **'lista_next'**, supondo que seja um botão ou link para a próxima página.
   
- `driver.quit()`: Este é o comando que encerra o **WebDriver**, fechando a sessão do navegador após a conclusão da automação.

```python
for titulo in titulos.find_all('tr'):
	for elemento in titulo.find_all('th'):
		arquivo.write('"' + elemento.text.strip() + '",')
	arquivo.write('\n')
```

Dessa forma, armazenamos os valores no formato CSV da seguinte maneira: '26252 - Universidade Federal de Campina Grande', '20 - Agricultura', '541 - Preservação e conservação ambiental', '1031 - Sem informação', '8593 - APOIO AO DESENVOLVIMENTO DA PRODUCAO AGROPECUARIA SUSTENTAVEL', '52 - Equipamentos e Material Permanente', '0,00'.

  > [!node]- Tabela resultante 
> A tabela resultante upada no [google sheets ](https://docs.google.com/spreadsheets/d/1wMN4EfzNT0RGfEHQh1EBlgEvkoV8NlouT3SrkqIZQCE/edit?usp=sharing)
### Explorando o HTML:

Uma dúvida que pode ter surgido é: *"De onde saíram esse tbody e lista_next?"* Esses elementos foram escolhidos com base na análise do HTML da página, pois são os elementos que mais ajudam no propósito de coleta de dados. Essa analise é feita com as ferramentas de desenvolvedor disponíveis no navegador. É possível visualizar o processo no passo a passo a seguir:

> [!tip]- Dica
> Para abrir as ferramentas de desenvolvedor podemos usar o atalho **Crtl + Shift + i**, ou apenas clicar com botão direito em qualquer lugar da tela e clicamos em inspecionar.

1. **Abrir as Ferramentas de Desenvolvedor:** 
	- Na página de [detalhamento das despesas públicas](https://portaldatransparencia.gov.br/despesas/consulta?paginacaoSimples=true&tamanhoPagina=&offset=&direcaoOrdenacao=asc&de=01%2F01%2F2023&ate=30%2F11%2F2023&orgaos=OR26252&colunasSelecionadas=funcao%2CsubFuncao%2Cprograma%2Cacao%2CvalorDespesaPaga%2CorgaoVinculado%2CelementoDespesa&ordenarPor=funcao&direcao=asc), fica bem claro quais são os dados que pretendemos coletar. Agora, abrimos as ferramentas de desenvolvedor.  
![[Pasted image 20231203182826.png]]

2. **Identificar os Elementos Relevantes:**
    - Ao abrir as ferramentas de desenvolvedor, você verá uma interface dividida em duas partes: a parte esquerda exibe a página web e a parte direita mostra o código HTML correspondente.
![[Pasted image 20231203183514.png]]

3. **Localizar os Dados Desejados:**  
    - Use a ferramenta de inspeção (geralmente um cursor ou uma seta) para selecionar os elementos na página que contêm os dados que você deseja extrair. Clique sobre a tabela e será mostrado na parte a direita o código HTML referente aquele elemento.
![[Pasted image 20231203183558.png]]

4. **Identificar as Tags HTML:**
    - Ao inspecionar os elementos, observe as tags HTML que os rodeiam. Por exemplo,na tabela encontramos o `<head>`, `<tbody>`, `<span>` ou outras tags. 
![[Pasted image 20231203183922.png]]

5. **Anotar as Localizações dos Elementos:**
    - Identifique as classes, IDs, nomes ou outras características dos elementos que contêm os dados que você deseja coletar. Por exemplo, algo como `<table class="dataTable no-footer">`.
![[Pasted image 20231203184046.png]]

6. **Confirmar o Método de Localização:**
    - Após identificar os elementos desejados, confirme o método que será utilizado para localizá-los no código Python usando o BeautifulSoup. Pode ser por classe, ID, nome da tag, etc.
### Considerações finais:

O **Web-Scraping** é uma técnica poderosa para coletar informações de páginas da web, envolve o uso de linguagens de programação para extrair e transferir dados para nossos sistemas. No contexto do **Python**, há bibliotecas cruciais, tais como **BeautifulSoup, Selenium e lxml**, que capacitam essa técnica, permitindo-nos acessar e manipular dados online. O uso dos métodos do [[Selenium]], como `find_element` e `page_source`, junto com a análise do HTML utilizando **BeautifulSoup**, revela o processo de identificação e extração de elementos desejados na página. A exploração do HTML através das ferramentas de desenvolvedor reforça a importância de analisar e selecionar corretamente os elementos alvo. O código Python usado no exemplo é relativamente simples e pode ser facilmente adaptado para coletar dados de outras fontes. No entanto, é importante realizar uma análise cuidadosa do HTML da fonte de dados antes de implementar o **Web-Scraping**. Isso ajudará a garantir que o código funcione corretamente e que você esteja coletando os dados corretos.

Desenvolvido por [Erik Luan(Perfil Github - @Smilke)](https://github.com/Smilke)
