import sys
import os

# Adiciona o diretório atual ao path para importações funcionarem corretamente
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.engine import SimulationEngine
from factories.presets import TurbineSimulationPresetFactory

def main():
    print("=== Testando Motor de Simulação da Turbina de Tesla (MVP) ===")
    
    # Cria simulação da turbina de CD movida a ar
    engine = TurbineSimulationPresetFactory.create_cd_air_turbine()
    
    print(f"Fluido utilizado: {engine.fluid.name}")
    print(f"Massa de um disco de CD: {engine.geometry.disc_mass * 1000:.2f} g")
    print(f"Momento de Inércia do rotor ({engine.geometry.num_discs} discos): {engine.geometry.moment_of_inertia:.6f} kg·m²")
    print(f"Espaçamento entre discos: {engine.geometry.disc_spacing * 1000:.2f} mm")
    print(f"Pressão de entrada: {engine.inlet_pressure / 1000:.1f} kPa")
    
    # Rodar simulação por 15 segundos com passo de tempo de 0.05 segundos
    print("\nExecutando simulação de 15 segundos...")
    engine.run_simulation(total_time=15.0, dt=0.05)
    
    print("\nResultados finais obtidos:")
    print(f"Tempo total simulado: {engine.history['time'][-1]:.2f} s")
    print(f"Velocidade final alcançada: {engine.history['rpm'][-1]:.1f} RPM")
    print(f"Torque viscoso final: {engine.history['torque_gen'][-1]:.6f} N·m")
    print(f"Perdas mecânicas finais: {engine.history['torque_losses'][-1]:.6f} N·m")
    print(f"Rendimento final: {engine.history['efficiency'][-1]:.2f}%")
    print(f"Número de Reynolds no escoamento: {engine.history['reynolds'][-1]:.1f}")
    
    print("\nSimulação concluída com sucesso! O motor físico está pronto.")

if __name__ == "__main__":
    main()
