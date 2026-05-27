import sys
import os

# Ajuste do PATH para módulos locais
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ui.app import TeslaTurbineApp

def main():
    print("Iniciando a Simulação da Turbina de Tesla (GUI)...")
    app = TeslaTurbineApp()
    app.mainloop()

if __name__ == "__main__":
    main()
