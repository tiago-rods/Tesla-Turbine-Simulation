# pyrefly: ignore [missing-import]
import csv
from tkinter import filedialog, messagebox
# pyrefly: ignore [missing-import]
import customtkinter as ctk
from .plotters import SimulationPlotter
from core.geometry import TurbineGeometry
from core.fluid import Air, Water, Steam
from core.engine import SimulationEngine

class TeslaTurbineApp(ctk.CTk):
    """
    Interface Gráfica (GUI) da Simulação da Turbina de Tesla (Sprint 2 MVP).
    """
    def __init__(self):
        super().__init__()

        self.title("Simulação - Turbina de Tesla (Física II)")
        self.geometry("1100x650")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Configuração do Layout Grid Principal (1 linha, 2 colunas)
        self.grid_columnconfigure(0, weight=1) # Coluna de Controles (esquerda)
        self.grid_columnconfigure(1, weight=3) # Coluna de Gráficos (direita)
        self.grid_rowconfigure(0, weight=1)

        # 1. Painel de Controle (Esquerda)
        self.control_frame = ctk.CTkFrame(self)
        self.control_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self._build_controls()

        # 2. Painel de Gráficos (Direita)
        self.plot_frame = ctk.CTkFrame(self)
        self.plot_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.plotter = SimulationPlotter(self.plot_frame)

        # Motor de simulação
        self.engine = None
        self._run_simulation() # Roda a primeira simulação inicial

    def _build_controls(self):
        """Constrói os widgets de controle (Sliders)."""
        ctk.CTkLabel(self.control_frame, text="Parâmetros Físicos", font=("Inter", 20, "bold")).pack(pady=10)

        # Fluido
        ctk.CTkLabel(self.control_frame, text="Tipo de Fluido:").pack(anchor="w", padx=20, pady=(10, 0))
        self.fluid_var = ctk.StringVar(value="Ar Comprimido")
        self.fluid_combo = ctk.CTkComboBox(
            self.control_frame, 
            values=["Ar Comprimido", "Água", "Vapor de Baixa Pressão"],
            variable=self.fluid_var,
            command=lambda _: self._run_simulation()
        )
        self.fluid_combo.pack(fill="x", padx=20, pady=5)

        # Pressão de Entrada
        self.pressure_val = ctk.DoubleVar(value=200.0) # kPa
        ctk.CTkLabel(self.control_frame, text="Pressão Entrada (kPa):").pack(anchor="w", padx=20, pady=(10, 0))
        self.lbl_pressure = ctk.CTkLabel(self.control_frame, text="200.0 kPa")
        self.lbl_pressure.pack(anchor="e", padx=20)
        self.slider_pressure = ctk.CTkSlider(
            self.control_frame, from_=50.0, to=1000.0, variable=self.pressure_val,
            command=self._update_pressure_label
        )
        self.slider_pressure.pack(fill="x", padx=20)

        # Espaçamento (b)
        self.spacing_val = ctk.DoubleVar(value=1.0) # mm
        ctk.CTkLabel(self.control_frame, text="Espaçamento b (mm):").pack(anchor="w", padx=20, pady=(10, 0))
        self.lbl_spacing = ctk.CTkLabel(self.control_frame, text="1.0 mm")
        self.lbl_spacing.pack(anchor="e", padx=20)
        self.slider_spacing = ctk.CTkSlider(
            self.control_frame, from_=0.1, to=5.0, variable=self.spacing_val,
            command=self._update_spacing_label
        )
        self.slider_spacing.pack(fill="x", padx=20)

        # Quantidade de Discos (N)
        self.discs_val = ctk.IntVar(value=5)
        ctk.CTkLabel(self.control_frame, text="Quantidade de Discos (N):").pack(anchor="w", padx=20, pady=(10, 0))
        self.lbl_discs = ctk.CTkLabel(self.control_frame, text="5")
        self.lbl_discs.pack(anchor="e", padx=20)
        self.slider_discs = ctk.CTkSlider(
            self.control_frame, from_=1, to=20, number_of_steps=19, variable=self.discs_val,
            command=self._update_discs_label
        )
        self.slider_discs.pack(fill="x", padx=20)

        # Botão Simular
        self.btn_simulate = ctk.CTkButton(self.control_frame, text="Re-Simular", command=self._run_simulation)
        self.btn_simulate.pack(fill="x", padx=20, pady=10)

        # Botões de Análise (Sprint 3)
        self.frame_analysis = ctk.CTkFrame(self.control_frame, fg_color="transparent")
        self.frame_analysis.pack(fill="x", padx=20, pady=5)
        
        self.btn_save_curve = ctk.CTkButton(self.frame_analysis, text="Salvar Baseline", command=self._save_baseline, width=100)
        self.btn_save_curve.pack(side="left", padx=(0, 5), expand=True)
        
        self.btn_clear_curve = ctk.CTkButton(self.frame_analysis, text="Limpar Baseline", command=self._clear_baseline, width=100, fg_color="gray")
        self.btn_clear_curve.pack(side="left", padx=(5, 0), expand=True)

        self.btn_export = ctk.CTkButton(self.control_frame, text="Exportar CSV (Relatório)", command=self._export_csv, fg_color="#27ae60", hover_color="#2ecc71")
        self.btn_export.pack(fill="x", padx=20, pady=10)

        # Labels de Resultados
        self.lbl_result_rpm = ctk.CTkLabel(self.control_frame, text="RPM Máximo: --", font=("Inter", 14, "bold"))
        self.lbl_result_rpm.pack(pady=2)
        
        self.lbl_result_eff = ctk.CTkLabel(self.control_frame, text="Rendimento Máximo: --", font=("Inter", 14, "bold"))
        self.lbl_result_eff.pack(pady=2)

        self.lbl_result_loss = ctk.CTkLabel(self.control_frame, text="Perda Térmica/Viscosa: -- W", font=("Inter", 12))
        self.lbl_result_loss.pack(pady=2)

    def _update_pressure_label(self, value):
        self.lbl_pressure.configure(text=f"{float(value):.1f} kPa")
    
    def _update_spacing_label(self, value):
        self.lbl_spacing.configure(text=f"{float(value):.2f} mm")

    def _update_discs_label(self, value):
        self.lbl_discs.configure(text=f"{int(value)}")

    def _get_selected_fluid(self):
        sel = self.fluid_var.get()
        if sel == "Água":
            return Water()
        elif sel == "Vapor de Baixa Pressão":
            return Steam()
        return Air()

    def _run_simulation(self):
        """Atualiza modelo com os dados da UI e dispara simulação no Engine."""
        fluid = self._get_selected_fluid()
        pressure_pa = self.pressure_val.get() * 1000.0 # kPa para Pa
        spacing_m = self.spacing_val.get() / 1000.0 # mm para m
        discs = int(self.discs_val.get())

        geom = TurbineGeometry(
            outer_radius=0.06,
            inner_radius=0.015,
            disc_spacing=spacing_m,
            num_discs=discs,
            disc_thickness=0.0012,
            disc_density=1200.0
        )
        
        # Vazão aproximada em função da pressão para manter MVP simples (Q ~ P^0.5)
        flow_rate = 0.003 * (pressure_pa / 200000.0)**0.5

        self.engine = SimulationEngine(geom, fluid, inlet_pressure=pressure_pa, flow_rate=flow_rate)
        
        # Roda simulação de 15 segundos
        self.engine.run_simulation(total_time=15.0, dt=0.05)

        # Atualiza gráficos
        self.plotter.update_plots(
            self.engine.history["time"],
            self.engine.history["rpm"],
            self.engine.history["torque_gen"],
            self.engine.history["torque_losses"]
        )

        # Atualiza métricas na UI
        max_rpm = max(self.engine.history["rpm"])
        max_eff = max(self.engine.history["efficiency"])
        
        # Perdas = Power In - Power Out no estado estacionário final
        p_in = self.engine.history["power_in"][-1]
        p_out = self.engine.history["power_out"][-1]
        loss_w = p_in - p_out

        self.lbl_result_rpm.configure(text=f"RPM Máximo: {max_rpm:.1f}")
        self.lbl_result_eff.configure(text=f"Rendimento Máximo: {max_eff:.1f} %")
        self.lbl_result_loss.configure(text=f"Perda Térmica/Viscosa: {loss_w:.1f} W")

    def _save_baseline(self):
        if self.engine:
            self.plotter.save_baseline(
                self.engine.history["time"],
                self.engine.history["rpm"],
                self.engine.history["torque_gen"],
                self.engine.history["torque_losses"]
            )
            self._run_simulation() # Re-renderiza para mostrar a baseline cinza
            
    def _clear_baseline(self):
        self.plotter.clear_baseline()
        self._run_simulation()

    def _export_csv(self):
        if not self.engine:
            return
            
        filepath = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")],
            title="Exportar Dados da Simulação"
        )
        
        if filepath:
            try:
                with open(filepath, mode='w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(["Tempo (s)", "RPM", "Torque Gerado (N.m)", "Perdas (N.m)", "Potência Entrada (W)", "Potência Saída (W)", "Rendimento (%)", "Reynolds"])
                    
                    hist = self.engine.history
                    for i in range(len(hist["time"])):
                        writer.writerow([
                            f"{hist['time'][i]:.4f}",
                            f"{hist['rpm'][i]:.2f}",
                            f"{hist['torque_gen'][i]:.6f}",
                            f"{hist['torque_losses'][i]:.6f}",
                            f"{hist['power_in'][i]:.2f}",
                            f"{hist['power_out'][i]:.2f}",
                            f"{hist['efficiency'][i]:.2f}",
                            f"{hist['reynolds'][i]:.1f}"
                        ])
                messagebox.showinfo("Sucesso", f"Dados exportados para {filepath}")
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao exportar CSV:\n{str(e)}")
