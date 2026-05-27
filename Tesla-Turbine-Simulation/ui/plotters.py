import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# pyrefly: ignore [missing-import]
import customtkinter as ctk

class SimulationPlotter:
    """
    Componente responsável por desenhar os gráficos da simulação.
    Encapsula o Matplotlib e integra com a interface Tkinter.
    """
    def __init__(self, parent_frame: ctk.CTkFrame):
        self.parent = parent_frame
        
        # Criação da figura e subplots (1 linha, 2 colunas)
        # Usando um estilo escuro nativo do matplotlib para combinar com CustomTkinter Dark
        plt.style.use('dark_background')
        self.fig, (self.ax_rpm, self.ax_torque) = plt.subplots(1, 2, figsize=(10, 4), dpi=100)
        self.fig.patch.set_facecolor('#2b2b2b') # Fundo para combinar com a UI

        # Canvas Tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.parent)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill=ctk.BOTH, expand=True, padx=10, pady=10)

    def update_plots(self, time_data: list, rpm_data: list, torque_gen: list, torque_loss: list):
        """
        Atualiza as curvas nos gráficos com base no histórico da simulação.
        """
        self.ax_rpm.clear()
        self.ax_torque.clear()

        # Configurações do Gráfico de RPM
        self.ax_rpm.plot(time_data, rpm_data, color='#00a8ff', linewidth=2, label='Rotação (RPM)')
        self.ax_rpm.set_title('Dinâmica de Rotação (Spin-up)', color='white')
        self.ax_rpm.set_xlabel('Tempo (s)', color='lightgray')
        self.ax_rpm.set_ylabel('RPM', color='lightgray')
        self.ax_rpm.grid(True, linestyle='--', alpha=0.3)
        self.ax_rpm.legend()

        # Configurações do Gráfico de Torque (Gerado vs Perdas)
        self.ax_torque.plot(rpm_data, torque_gen, color='#44bd32', linewidth=2, label='Torque Viscoso')
        self.ax_torque.plot(rpm_data, torque_loss, color='#e84118', linewidth=2, label='Perdas Mecânicas')
        self.ax_torque.set_title('Torque vs Rotação', color='white')
        self.ax_torque.set_xlabel('Rotação (RPM)', color='lightgray')
        self.ax_torque.set_ylabel('Torque (N·m)', color='lightgray')
        self.ax_torque.grid(True, linestyle='--', alpha=0.3)
        self.ax_torque.legend()

        self.fig.tight_layout()
        self.canvas.draw()
