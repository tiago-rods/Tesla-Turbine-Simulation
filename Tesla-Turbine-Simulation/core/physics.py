import numpy as np
from .fluid import BaseFluid
from .geometry import TurbineGeometry

class TeslaTurbinePhysics:
    """
    Funções puras para cálculos de física de fluidos e termodinâmica.
    Garante DRY agrupando cálculos reusáveis.
    """
    @staticmethod
    def reynolds_number(fluid: BaseFluid, velocity: float, spacing: float) -> float:
        """
        Re = (rho * v * b) / mu
        """
        if fluid.viscosity == 0:
            return float('inf')
        return (fluid.density * velocity * spacing) / fluid.viscosity

    @staticmethod
    def tangential_fluid_velocity(inlet_pressure: float, fluid: BaseFluid) -> float:
        """
        Estima a velocidade tangencial de entrada do fluido no bocal usando a equação de Bernoulli simplificada:
        v = sqrt(2 * delta_P / rho)
        """
        if fluid.density <= 0:
            return 0.0
        return np.sqrt(2.0 * inlet_pressure / fluid.density)

    @staticmethod
    def viscous_torque_generated(
        geometry: TurbineGeometry,
        fluid: BaseFluid,
        inlet_pressure: float,
        rotor_angular_velocity: float
    ) -> float:
        """
        Calcula o torque viscoso exercido pelo fluido sobre os discos.
        Derivado da força de cisalhamento viscoso entre discos paralelos.
        """
        v_fluid_tangential = TeslaTurbinePhysics.tangential_fluid_velocity(inlet_pressure, fluid)
        r_in = geometry.outer_radius
        r_out = geometry.inner_radius
        b = geometry.disc_spacing
        N = geometry.num_discs
        mu = fluid.viscosity

        # Velocidade angular média do fluido assumida no canal
        omega_fluid = v_fluid_tangential / r_in

        # Se o rotor girar mais rápido que o fluido, o torque passa a ser negativo (freando)
        slip = omega_fluid - rotor_angular_velocity

        # Torque viscoso integrado sob a simplificação de perfil de velocidade linear na folga
        # T = N * integral de (r * dF_cisalhamento)
        # T_viscoso_aprox = (4 * pi * mu * N * (r_in^4 - r_out^4) / b) * slip
        factor = (4.0 * np.pi * mu * N * (r_in**4 - r_out**4)) / b
        return factor * slip

    @staticmethod
    def friction_losses_torque(
        geometry: TurbineGeometry,
        fluid: BaseFluid,
        rotor_angular_velocity: float
    ) -> float:
        """
        Mapeia perdas físicas:
        1. Atrito no rolamento (proporcional à rotação): T = f_bearing * omega
        2. Perdas por ventilação (arrasto do ar externo nos discos): T = C_f * rho * omega^2 * r^5
        """
        omega = abs(rotor_angular_velocity)
        
        # Coeficiente de arrasto aerodinâmico externo simplificado
        c_f = 0.005 
        windage_torque = c_f * fluid.density * (omega**2) * (geometry.outer_radius**5)

        # Torque de perdas por rolamento/fricção mecânica
        bearing_friction_coefficient = 1e-4
        bearing_torque = bearing_friction_coefficient * omega

        return windage_torque + bearing_torque

    @staticmethod
    def input_hydraulic_power(inlet_pressure: float, flow_rate: float) -> float:
        """
        P_in = delta_P * Q
        """
        return inlet_pressure * flow_rate

    @staticmethod
    def output_mechanical_power(torque: float, angular_velocity: float) -> float:
        """
        P_out = Torque * omega
        """
        return torque * angular_velocity

    @staticmethod
    def efficiency(power_out: float, power_in: float) -> float:
        """
        Rendimento (eta) = P_out / P_in
        """
        if power_in <= 0:
            return 0.0
        eff = power_out / power_in
        return max(0.0, min(eff, 1.0)) # Limitado entre 0 e 100% fisicamente
