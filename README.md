# Dashboard de Análise de Impactos Econômicos - Brasil

Este repositório contém um dashboard interativo desenvolvido para analisar os impactos da pandemia e da guerra da Ucrânia nos mercados econômicos do Brasil, focando em commodities relevantes.

## Conteúdo do Repositório

- **app.py**: Arquivo principal que contém a aplicação Dash para o dashboard.
- **Dados Tratados/**: Pasta que contém os dados utilizados na análise.
- **assets/**: Pasta para arquivos estáticos como CSS e imagens.
- **pages/**: Pasta que contém os layouts das diferentes páginas do dashboard.
- **callbacks**: Scripts que contêm os callbacks para interações dos usuários.

## Tecnologias Utilizadas

- **Dash**: Framework Python para criação de aplicações web interativas.
- **Plotly**: Biblioteca para criação de gráficos interativos.
- **Pandas**: Manipulação e análise de dados.
- **HTML, CSS, JavaScript**: Utilizados para personalização do layout e interatividade.

## Funcionalidades do Dashboard

1. **Análise de Commodities**: Visualização dos preços e tendências de commodities como petróleo, gás natural, carvão, e produtos agrícolas relevantes para o Brasil.
   
2. **Impactos da Pandemia e Guerra da Ucrânia**: Análise de como eventos globais influenciaram os mercados brasileiros.

3. **Visualizações Interativas**: Gráficos interativos que permitem ao usuário explorar diferentes períodos e variáveis.

## Telas e gráficos

### Home
![image](https://github.com/LeandroRochAlg/Analise-de-Dados/assets/87719561/5a70e70f-0bf1-473a-831f-26e172f281be)

### Taxa de Câmbio e Volatilidade
![image](https://github.com/LeandroRochAlg/Analise-de-Dados/assets/87719561/6e446640-4c98-482a-ad9e-9469c66fdcc1)

### Exportação e Importação
![image](https://github.com/LeandroRochAlg/Analise-de-Dados/assets/87719561/8d329081-9be3-459c-916a-c7c4a0e9f825)

### Desemprego e IPCA
![image](https://github.com/LeandroRochAlg/Analise-de-Dados/assets/87719561/693d5a10-b69d-4437-983c-cb414d375b29)

### Commodities
![image](https://github.com/LeandroRochAlg/Analise-de-Dados/assets/87719561/d514bdac-51c0-496a-9a69-046d3cf51a11)

## Como Usar

1. **Instalação das Dependências**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Execução da Aplicação**:
   ```bash
   python app.py
   ```
   Acesse `http://localhost:8050` em seu navegador para ver o dashboard.

## Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para enviar pull requests com melhorias, novas funcionalidades, ou correções de bugs.
