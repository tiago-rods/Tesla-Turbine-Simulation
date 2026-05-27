from abc import ABC, abstractmethod
from typing import Callable

class BaseSolver(ABC):
    """
    Interface para solucionadores de ODE (Equações Diferenciais Ordinárias).
    Aplica o Strategy Pattern.
    """
    @abstractmethod
    def step(self, y: float, dy_dt_func: Callable[[float], float], dt: float) -> float:
        """Avança o valor de y pelo passo de tempo dt."""
        pass

class EulerSolver(BaseSolver):
    """Método simples de Euler de 1ª ordem."""
    def step(self, y: float, dy_dt_func: Callable[[float], float], dt: float) -> float:
        return y + dy_dt_func(y) * dt

class RK4Solver(BaseSolver):
    """Método clássico Runge-Kutta de 4ª ordem (mais estável e preciso)."""
    def step(self, y: float, dy_dt_func: Callable[[float], float], dt: float) -> float:
        k1 = dy_dt_func(y)
        k2 = dy_dt_func(y + 0.5 * dt * k1)
        k3 = dy_dt_func(y + 0.5 * dt * k2)
        k4 = dy_dt_func(y + dt * k3)
        return y + (dt / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)
