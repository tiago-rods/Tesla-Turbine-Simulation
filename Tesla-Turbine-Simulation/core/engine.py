from typing import List, Dict, Any
from .fluid import BaseFluid
from .geometry import TurbineGeometry
from .physics import TeslaTurbinePhysics
from .solvers import BaseSolver, RK4Solver

class SimulationEngine:
    """
    Motor de Simulação Principal.
    Controla o estado físico da turbina e avança o tempo usando resolvedores (solvers).
    """
    def __init__(
        self,
        geometry: TurbineGeometry,
        fluid: BaseFluid,
        inlet_pressure: float = 101325.0, # delta_P de entrada em Pascal (1 atm = ~101325 Pa)
        flow_rate: float = 0.005,         # Q em m³/s
        solver: BaseSolver = None
    ):
        self.geometry = geometry
        self.fluid = fluid
        self.inlet_pressure = inlet_pressure
        self.flow_rate = flow_rate
        
        # Padrão: Runge-Kutta 4
        self.solver = solver if solver else RK4Solver()

        # Estados da turbina
        self.angular_velocity = 0.0  # omega (rad/s)
        self.time = 0.0              # t (s)

        # Histórico para geração de gráficos
        self.history: Dict[str, List[float]] = {
            "time": [],
            "rpm": [],
            "torque_gen": [],
            "torque_losses": [],
            "power_in": [],
            "power_out": [],
            "efficiency": [],
            "reynolds": []
        }

    @property
    def rpm(self) -> float:
        """Converte rad/s para RPM."""
        return self.angular_velocity * (60.0 / (2.0 * 3.141592653589793))

    def reset(self):
        """Reinicia os estados da simulação."""
        self.angular_velocity = 0.0
        self.time = 0.0
        for key in self.history:
            self.history[key].clear()

    def get_acceleration(self, omega: float) -> float:
        """
        Calcula a aceleração angular alpha = (T_gerado - T_perdas) / J
        Equação fundamental de dinâmica rotacional da turbina.
        """
        t_gen = TeslaTurbinePhysics.viscous_torque_generated(
            self.geometry, self.fluid, self.inlet_pressure, omega
        )
        t_losses = TeslaTurbinePhysics.friction_losses_torque(
            self.geometry, self.fluid, omega
        )
        
        inertia = self.geometry.moment_of_inertia
        if inertia <= 0:
            return 0.0
        
        return (t_gen - t_losses) / inertia

    def step(self, dt: float):
        """Avança a simulação em um passo de tempo dt."""
        # Salva o estado atual no histórico antes do passo
        t_gen = TeslaTurbinePhysics.viscous_torque_generated(
            self.geometry, self.fluid, self.inlet_pressure, self.angular_velocity
        )
        t_losses = TeslaTurbinePhysics.friction_losses_torque(
            self.geometry, self.fluid, self.angular_velocity
        )
        
        v_fluid_tangential = TeslaTurbinePhysics.tangential_fluid_velocity(self.inlet_pressure, self.fluid)
        reynolds = TeslaTurbinePhysics.reynolds_number(self.fluid, v_fluid_tangential, self.geometry.disc_spacing)
        
        p_in = TeslaTurbinePhysics.input_hydraulic_power(self.inlet_pressure, self.flow_rate)
        # Torque útil líquido é o gerado menos perdas
        t_net = max(0.0, t_gen - t_losses)
        p_out = TeslaTurbinePhysics.output_mechanical_power(t_net, self.angular_velocity)
        eff = TeslaTurbinePhysics.efficiency(p_out, p_in)

        self.history["time"].append(self.time)
        self.history["rpm"].append(self.rpm)
        self.history["torque_gen"].append(t_gen)
        self.history["torque_losses"].append(t_losses)
        self.history["power_in"].append(p_in)
        self.history["power_out"].append(p_out)
        self.history["efficiency"].append(eff * 100.0) # em percentual
        self.history["reynolds"].append(reynolds)

        # Atualiza a velocidade angular usando o integrador ODE (Strategy Pattern)
        self.angular_velocity = self.solver.step(
            self.angular_velocity,
            self.get_acceleration,
            dt
        )
        # Impede rotação reversa decorrente de aproximações de perdas se parada
        if self.angular_velocity < 0:
            self.angular_velocity = 0.0

        self.time += dt

    def run_simulation(self, total_time: float, dt: float):
        """Executa a simulação inteira em lote até total_time."""
        self.reset()
        steps = int(total_time / dt)
        for _ in range(steps):
            self.step(dt)
