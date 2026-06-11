from factories.presets import TurbineSimulationPresetFactory
engine = TurbineSimulationPresetFactory.create_industrial_water_turbine()
engine.run_simulation(total_time=10.0, dt=0.05)
print("Max Efficiency:", max(engine.history['efficiency']))
