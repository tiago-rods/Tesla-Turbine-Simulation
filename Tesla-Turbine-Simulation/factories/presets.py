from core.fluid import Air, Water, Steam
from core.geometry import TurbineGeometry
from core.engine import SimulationEngine

class TurbineSimulationPresetFactory:
    """
    Padrão Factory Method para inicializar simulações com configurações típicas.
    Facilita testes e simplifica o fluxo (DRY).
    """

    @staticmethod
    def create_cd_air_turbine() -> SimulationEngine:
        """
        Cria um protótipo clássico de demonstração física:
        Discos feitos de CDs reciclados (120mm de diâmetro) movidos a ar comprimido.
        """
        geom = TurbineGeometry(
            outer_radius=0.06,      # 60mm
            inner_radius=0.015,     # 15mm (raio do furo central aproximado)
            disc_spacing=0.001,     # 1mm
            num_discs=5,
            disc_thickness=0.0012,  # 1.2mm
            disc_density=1200.0     # Policarbonato
        )
        fluid = Air(temperature_c=25.0)
        # Pressão típica de compressor doméstico (~2 bar relativos = ~200000 Pa)
        # Vazão típica ~3 L/s (0.003 m³/s)
        return SimulationEngine(geom, fluid, inlet_pressure=200000.0, flow_rate=0.003)

    @staticmethod
    def create_industrial_water_turbine() -> SimulationEngine:
        """
        Cria uma turbina maior de metal para escoamento de água.
        """
        geom = TurbineGeometry(
            outer_radius=0.25,      # 250mm
            inner_radius=0.05,      # 50mm
            disc_spacing=0.0005,    # 0.5mm
            num_discs=20,
            disc_thickness=0.002,   # 2mm aço
            disc_density=7800.0     # Aço
        )
        fluid = Water()
        # Queda de pressão de ~5 bar (500000 Pa)
        # Vazão ~10 L/s (0.01 m³/s)
        return SimulationEngine(geom, fluid, inlet_pressure=500000.0, flow_rate=0.01)
