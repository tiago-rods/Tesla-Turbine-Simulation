# Tesla Turbine Simulation

Este projeto é uma simulação física e interativa de uma **Turbina de Tesla**, desenvolvida no contexto da disciplina de **Física II**. A simulação modela matematicamente o comportamento fluido-mecânico de uma turbina de discos (sem pás), baseada na invenção de Nikola Tesla.

## 🚀 O que o projeto faz

O sistema possui um motor físico (`SimulationEngine`) que calcula e demonstra os princípios de funcionamento da turbina, simulando a interação entre fluidos e o rotor. As principais características calculadas e simuladas incluem:

* **Dinâmica de Fluidos e Torque:** Calcula as forças de arrasto viscoso e adesão da camada limite que impulsionam os discos. Calcula também o número de Reynolds.
* **Física Realista (Leis da Termodinâmica):** A simulação foi rigorosamente calibrada com o *Limite da Equação de Euler para Turbomáquinas* ($T_{max} = \dot{m} \cdot r \cdot v$). Isso garante a conservação de momento, não permitindo que a turbina gere mais torque do que a energia cinética disponível na vazão restrita de fluido.
* **Perdas Físicas e Atrito:** Modelagem matemática das perdas reais no sistema:
  * **Eficiência do Bocal ($C_v$):** Perda de energia cinética devido ao atrito no bocal injetor antes mesmo do fluido atingir os discos.
  * **Atrito em Rolamentos:** Fricção mecânica no eixo da turbina, que escala com o giro e o alto momento de inércia dos discos pesados.
  * **Arrasto Aerodinâmico:** Perdas parasitas eólicas que dependem do quadrado da velocidade de rotação ($\omega^2$) e do tamanho do disco ($r^5$).
* **Fluidos e Materiais:** Suporte nativo para **Ar Comprimido**, **Água** e **Vapor de Baixa Pressão**. O simulador oferece duas opções de geometria prontas na interface:
  * **Protótipo de CDs:** Usado em experimentos amadores. Feito de plástico (Policarbonato), discos pequenos (6cm de raio) e movido a ar. Possui baixa inércia, RPM extremamente alto e eficiência física muito baixa (~9%).
  * **Padrão Industrial:** Discos grossos de aço (25cm de raio) tracionados por água de alta densidade. RPM menor, porém gerando altíssimo torque e uma eficiência teórica respeitável (~66%).
* **Interface Gráfica (GUI):** Conta com uma aplicação interativa para controle de pressão, seleção do modelo da turbina e acompanhamento de gráficos gerados dinamicamente em tempo real.

## 📂 Estrutura do Projeto

* `Tesla-Turbine-Simulation/core/`: Núcleo da simulação. Contém o `engine.py`, geometrias em `geometry.py`, fluidos em `fluid.py` e equações em `physics.py`.
* `Tesla-Turbine-Simulation/factories/`: Padrões de projeto com configurações pré-definidas (Preset de CDs vs Padrão Industrial).
* `Tesla-Turbine-Simulation/ui/`: Componentes da interface gráfica da simulação desenvolvida com `customtkinter`.
* `Tesla-Turbine-Simulation/main.py`: Ponto de entrada da aplicação gráfica.
* `Tesla-Turbine-Simulation/test_physics_equations.py`: Scripts unitários construídos em `pytest` que validam os limites termodinâmicos do sistema.

## ⚙️ Como Executar

**1. Instalação de Dependências:**
No diretório raiz do projeto, instale as bibliotecas necessárias usando o `pip`:
```bash
pip install -r requirements.txt
```

**2. Interface Gráfica Interativa (Recomendado):**
Para iniciar a aplicação visual completa da simulação, execute:
```bash
python Tesla-Turbine-Simulation/main.py
```

**3. Testes Físicos Isolados via Terminal:**
Se você quiser validar as físicas e limites de conservação da turbina diretamente pelo terminal, basta rodar a nossa suíte de testes:
```bash
python -m pytest Tesla-Turbine-Simulation/test_physics_equations.py -v
```