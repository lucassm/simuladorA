simuladorA
==========

Este é um projeto de simulador de sistemas de distribuição de energia elétrica, que tem como objetivo servir de base gráfica para construção de modelos de redes elétricas bem como de seus equipamentos.

Inicialmente o simulador irá possuir as funcionalidades de desenho da rede e arquivamento das informações dos componentes da rede no formato xml e obdecendo as perdeterminações do padrão CIM (Common Information Model).


## Dependências

Este software tem como dependências o interpretador Python 2.7 e os seguintes pacotes:
* PySide
* Numpy

## Versão

0.1

## Funcionalidades

Essa versão do simulador tem simplesmente a funcionalidade de desenho dos componentes da rede no diagrama gráfico

## Bugs

* Diagrama com erros ao abrir arquivo xml com informações da rede;
* Os menus não abrem ao carregar o arquivo xml;
* Erro no alinhamento dos componentes qundo um dos componentes está conectado a uma barra;
* Dificuldades para selecionar as linhas que conectam um componente a outro;
* O componente religador pode ter quantas conexões quanto queira, enquanto só deveriam ser permitidas duas conexões;

## Funcionalidades a serem implementadas

* Criar as janelas para inserir os parâmetros de cada componente;
* Criar o componente 'Nó de carga' que pode ser inserido separadamente no diagrama ou na linha que conecta dois religadores;
* Salvar as informações de parâmetros dos componentes em xml utilizando o padrão CIM

## Observações

* As funcionalidades descritas aqui estão previstas para a versão 0.2 do simulador;
* O nome do simulador ainda não está definido;