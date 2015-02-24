simuladorA
==========

Este é um projeto de simulador de sistemas de distribuição de energia elétrica, que tem como objetivo servir de base gráfica para construção de modelos de redes elétricas bem como de seus equipamentos.

Inicialmente o simulador irá possuir as funcionalidades de desenho da rede e arquivamento das informações dos componentes da rede no formato xml e obdecendo as perdeterminações do padrão CIM (Common Information Model).


## Dependências

Este software tem como dependências o interpretador Python 2.7 e os seguintes pacotes:
* PySide
* Numpy

## Versão

0.2

## Como utilizar

Em ambiente linux, com as dependências instaladas, vá até a pasta clonada deste repositório e execute o seguinte comando:

$python simulador.py

## Funcionalidades

Essa versão do simulador tem simplesmente a funcionalidade de desenho dos componentes da rede no diagrama gráfico, com os seguintes componentes:
- Religador;
- Barra;
- Linha;
- Nó de carga;

Algumas funcionalidades são:
- Alinhamento dos itens gráficos;
- Salvar diagrama em arquivo do tipo xml;
- Integração parcial com o padrão CIM;

## Bugs

- [ ] Algoritmo de alimnhamento com erro quando a linha contém nós de carga;
- [ ] Erros gráficos quando na inclusão dos nós de carga;

## Funcionalidades a serem implementadas

- [ ] Criar as janelas para inserir os parâmetros de cada componente;
- [ ] Salvar as informações de parâmetros dos componentes em xml utilizando o padrão CIM
- [ ] Integrar a representação gráfica dos componentes com a estrutura de dados desenvolvida para representar a manipular a rede elétrica;

## Observações

* As funcionalidades descritas aqui estão previstas para a versão 0.3 do simulador;
* O nome do simulador ainda não está definido;