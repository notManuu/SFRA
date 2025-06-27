🌀 SFRA Transformer Fault Analysis — Visual Simulator with Streamlit
Este proyecto es una herramienta interactiva desarrollada en Python + Streamlit que simula las pruebas SFRA (Sweep Frequency Response Analysis) utilizadas para evaluar la integridad estructural de transformadores eléctricos.

🔍 ¿Qué hace esta app?
Simula las pruebas ACA, ACC, IC e II sobre un transformador modelado con componentes RLC y capacitancias interdevanado.

Compara la respuesta en frecuencia de un transformador sano con múltiples escenarios de fallas típicas como:

Cortocircuito parcial de devanado

Aumento de capacitancia entre bobinas

Mayor fuga magnética

Reducción de vueltas (secundario)

Detecta automáticamente las frecuencias de divergencia entre la respuesta sana y fallida con base en un umbral dB configurable.

Permite ajustar todos los parámetros físicos y eléctricos del transformador desde la interfaz.

🧪 Pruebas SFRA incluidas
ACA: Primario a tierra, secundario abierto

ACC: Primario a tierra, secundario en corto

IC: Acoplamiento capacitivo entre devanados

II: Acoplamiento inductivo entre devanados
