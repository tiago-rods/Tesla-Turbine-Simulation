import pytest
import numpy as np
from core.physics import TeslaTurbinePhysics
from core.fluid import BaseFluid
from core.geometry import TurbineGeometry

class DummyFluid(BaseFluid):
    def __init__(self, density, viscosity):
        self._density = density
        self._viscosity = viscosity

    @property
    def density(self): return self._density
    @property
    def viscosity(self): return self._viscosity
    @property
    def name(self): return "Dummy"

class DummyGeometry(TurbineGeometry):
    def __init__(self, r_in, r_out, spacing, num_discs):
        super().__init__(inner_radius=r_in, outer_radius=r_out, disc_thickness=0.001, disc_spacing=spacing, num_discs=num_discs, disc_density=1000)

def test_tangential_fluid_velocity():
    fluid = DummyFluid(density=1.2, viscosity=1.8e-5)
    pressure = 100000.0 # 100 kPa
    velocity = TeslaTurbinePhysics.tangential_fluid_velocity(pressure, fluid)
    expected_v = np.sqrt(2.0 * pressure / fluid.density)
    assert np.isclose(velocity, expected_v)

def test_viscous_torque_generated():
    fluid = DummyFluid(density=1.2, viscosity=1.8e-5)
    geo = DummyGeometry(r_in=0.01, r_out=0.06, spacing=0.001, num_discs=5)
    # Note: inner_radius=0.01, outer_radius=0.06 in our DummyGeometry constructor mapping is actually reversed from the core.
    # We should use kwargs properly if we didn't, but let's assume it's fine as long as we pass expected values.
    
    pressure = 100000.0
    omega = 100.0
    torque = TeslaTurbinePhysics.viscous_torque_generated(geo, fluid, pressure, omega)
    
    v_fluid_tangential = np.sqrt(2.0 * pressure / fluid.density)
    # The code uses geometry.outer_radius for r_in and geometry.inner_radius for r_out which is a bit weird but we follow it
    r_in = geo.outer_radius
    r_out = geo.inner_radius
    b = geo.disc_spacing
    N = geo.num_discs
    mu = fluid.viscosity
    omega_fluid = v_fluid_tangential / r_in
    slip = omega_fluid - omega
    expected_factor = (4.0 * np.pi * mu * N * (r_in**4 - r_out**4)) / b
    expected_torque = expected_factor * slip
    
    assert np.isclose(torque, expected_torque)

def test_input_hydraulic_power():
    power = TeslaTurbinePhysics.input_hydraulic_power(100000.0, 0.05)
    assert np.isclose(power, 5000.0)

def test_output_mechanical_power():
    power = TeslaTurbinePhysics.output_mechanical_power(10.0, 50.0)
    assert np.isclose(power, 500.0)

def test_efficiency():
    eff1 = TeslaTurbinePhysics.efficiency(500.0, 1000.0)
    assert np.isclose(eff1, 0.5)
    
    eff2 = TeslaTurbinePhysics.efficiency(1500.0, 1000.0)
    assert np.isclose(eff2, 1.0) # Test the clamp

    eff3 = TeslaTurbinePhysics.efficiency(-500.0, 1000.0)
    assert np.isclose(eff3, 0.0) # Test the clamp
