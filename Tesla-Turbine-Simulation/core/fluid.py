from abc import ABC, abstractmethod

class BaseFluid(ABC):
    """
    Abstração que define as propriedades físicas de um fluido.
    Segue o Dependency Inversion Principle (DIP).
    """
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def density(self) -> float:
        """Retorna a densidade (rho) em kg/m³."""
        pass

    @property
    @abstractmethod
    def viscosity(self) -> float:
        """Retorna a viscosidade dinâmica (mu) em Pa·s ou kg/(m·s)."""
        pass

class Air(BaseFluid):
    def __init__(self, temperature_c: float = 25.0):
        self.temp = temperature_c

    @property
    def name(self) -> str:
        return f"Ar Comprimido ({self.temp}°C)"

    @property
    def density(self) -> float:
        # Simplificação para ar a 1 atm (aprox. 1.2 kg/m³)
        return 1.204

    @property
    def viscosity(self) -> float:
        # Viscosidade dinâmica aproximada do ar a 25°C
        return 1.84e-5

class Water(BaseFluid):
    @property
    def name(self) -> str:
        return "Água"

    @property
    def density(self) -> float:
        return 997.0

    @property
    def viscosity(self) -> float:
        return 8.9e-4

class Steam(BaseFluid):
    @property
    def name(self) -> str:
        return "Vapor de Baixa Pressão"

    @property
    def density(self) -> float:
        return 0.598  # Vapor saturado a 100°C/1atm aproximado

    @property
    def viscosity(self) -> float:
        return 1.2e-5
