# Tesla Turbine Simulation

Este projeto é uma simulação física e interativa de uma **Turbina de Tesla**, desenvolvida no contexto da disciplina de **Física II**. A simulação modela matematicamente o comportamento fluido-mecânico de uma turbina de discos (sem pás), baseada na invenção de Nikola Tesla.

## 🚀 O que o projeto faz

O sistema possui um motor físico (`SimulationEngine`) que calcula e demonstra os princípios de funcionamento da turbina, simulando a interação entre fluidos e o rotor. As principais características calculadas e simuladas incluem:

* **Dinâmica de Fluidos:** Calcula as forças de arrasto viscoso e adesão da camada limite que impulsionam os discos. Calcula também o número de Reynolds.
* **Fluidos Suportados:** A simulação permite trabalhar com fluidos de diferentes densidades e viscosidades, incluindo **Ar Comprimido**, **Água** e **Vapor de Baixa Pressão**.
* **Física do Rotor:** Modelagem da geometria da turbina (ex: utilizando discos de CD comuns), calculando a massa, o espaçamento entre discos e o Momento de Inércia do sistema.
* **Desempenho (Torque e Eficiência):** Computa em tempo real o torque viscoso gerado, as perdas mecânicas (atrito nos rolamentos) e a eficiência global da máquina. A velocidade angular (RPM) é calculada ao longo do tempo.
* **Interface Gráfica (GUI):** Conta com uma aplicação com interface visual (`ui/app.py`) para facilitar o controle dos parâmetros e a visualização dos resultados.

## 📂 Estrutura do Projeto

* `Tesla-Turbine-Simulation/core/`: Núcleo da simulação. Contém as equações matemáticas em `engine.py` e as propriedades dos fluidos em `fluid.py`.
* `Tesla-Turbine-Simulation/factories/`: Padrões de projeto e configurações pré-definidas (ex: setup de turbina de CDs).
* `Tesla-Turbine-Simulation/ui/`: Componentes da interface gráfica da simulação.
* `Tesla-Turbine-Simulation/main.py`: Ponto de entrada da aplicação gráfica.
* `Tesla-Turbine-Simulation/test_simulation.py`: Script para testar o motor de simulação (MVP) executando no terminal e mostrando estatísticas (Rendimento, RPM final, Torques).

## ⚙️ Como Executar

**Interface Gráfica:**
Para iniciar a aplicação visual completa da simulação, execute:
```bash
python Tesla-Turbine-Simulation/main.py
```

**Teste de Motor via Terminal:**
Para rodar a simulação no modo texto e ver os logs físicos detalhados do motor (duração de 15s):
```bash
python Tesla-Turbine-Simulation/test_simulation.py
```