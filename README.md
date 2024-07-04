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
![image](https://github.com/LeandroRochAlg/Analise-de-Dados/assets/87719561/e6488889-c2f9-4c53-a326-425c61f4ec84)

### Taxa de Câmbio e Volatilidade
![image](https://github.com/LeandroRochAlg/Analise-de-Dados/assets/87719561/b1b8e25c-7585-4bb1-89ed-abdbdd82f467)

### Exportação e Importação
![image](https://github.com/LeandroRochAlg/Analise-de-Dados/assets/87719561/06d31059-0c2d-4314-9a86-ca0b9c853f64)

### Desemprego e IPCA
![image](https://github.com/LeandroRochAlg/Analise-de-Dados/assets/87719561/7da9bb53-926f-4754-819b-78258b925c65)

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
