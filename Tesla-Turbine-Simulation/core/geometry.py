import numpy as np

class TurbineGeometry:
    """
    Representa a geometria física do rotor da Turbina de Tesla.
    Segue Single Responsibility Principle (SRP).
    """
    def __init__(
        self,
        outer_radius: float = 0.06,      # r_in (m) - ex: raio de um CD (6cm)
        inner_radius: float = 0.015,     # r_out (m) - raio de saída central (1.5cm)
        disc_spacing: float = 0.001,     # b (m) - espaçamento (1mm)
        num_discs: int = 5,              # N - número de discos
        disc_thickness: float = 0.0012,  # Espessura do disco (1.2mm para CD)
        disc_density: float = 1200.0,    # Densidade do material (Policarbonato/CD = ~1200 kg/m³)
    ):
        self.outer_radius = outer_radius
        self.inner_radius = inner_radius
        self.disc_spacing = disc_spacing
        self.num_discs = num_discs
        self.disc_thickness = disc_thickness
        self.disc_density = disc_density

    @property
    def disc_volume(self) -> float:
        """Calcula o volume de um único disco (cilindro vazado)."""
        return np.pi * (self.outer_radius**2 - self.inner_radius**2) * self.disc_thickness

    @property
    def disc_mass(self) -> float:
        """Calcula a massa de um único disco."""
        return self.disc_volume * self.disc_density

    @property
    def moment_of_inertia(self) -> float:
        """
        Calcula o momento de inércia (J) do rotor composto por N discos.
        J = N * (1/2 * m * (r_in² + r_out²))
        """
        single_inertia = 0.5 * self.disc_mass * (self.outer_radius**2 + self.inner_radius**2)
        return self.num_discs * single_inertia
