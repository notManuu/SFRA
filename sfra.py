import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("Comparación SFRA: Sano vs Fallas")

# Parámetros base del transformador - barra lateral
st.sidebar.header("Transformador Sano")
N_p = st.sidebar.number_input("Vueltas primario (N_p)", value=160.0)
N_s = st.sidebar.number_input("Vueltas secundario (N_s)", value=20.0)
A_core = st.sidebar.number_input("Área del núcleo (m²)", value=0.01)
d = st.sidebar.number_input("Espacio entre devanados d (m)", value=0.005)

st.sidebar.header("Parámetros RLC Base")
R_p = st.sidebar.number_input("Resistencia primario R_p (Ω)", value=5.0)
L_fp = st.sidebar.number_input("Inductancia fuga primario L_fp (H)", value=0.02)
L_m = st.sidebar.number_input("Inductancia magnetización L_m (H)", value=2.0)
C_p = st.sidebar.number_input("Capacitancia primario C_p (F)", value=1e-9)
C_s = st.sidebar.number_input("Capacitancia secundario C_s (F)", value=1e-9)
C_ps = st.sidebar.number_input("Capacitancia inter-devanados C_ps (F)", value=5e-11)

st.sidebar.header("Configuración de Barrido SFRA")
f_min = st.sidebar.number_input("Frecuencia mínima (Hz)", value=10.0)
f_max = st.sidebar.number_input("Frecuencia máxima (Hz)", value=1e6)
points = st.sidebar.number_input("Puntos de barrido", value=2000)
threshold = st.sidebar.number_input("Umbral de diferencia (dB)", value=3.0)

# Selección de pruebas y fallas - área principal
test = st.selectbox("Selecciona la prueba SFRA a comparar:", ["ACA", "ACC", "IC", "II"])
faults = st.multiselect(
    "Selecciona las fallas a comparar:",
    ["Cortocircuito de devanado", "Incremento de capacitancia inter-devanado", "Aumento de fuga magnética", "Pérdida de vueltas secundario"]
)

# Eje de frecuencias
g = np.logspace(np.log10(f_min), np.log10(f_max), int(points))
omega = 2 * np.pi * g

# Definición de funciones SFRA

def H_ACA(params):
    R_p, L_fp, L_m, C_p, C_ps, C_s = params
    Z_Rp = R_p
    Z_Lfp = 1j * omega * L_fp
    Z_Lm = 1j * omega * L_m
    Z_Cp = 1 / (1j * omega * C_p)
    Z_Cps = 1 / (1j * omega * C_ps)
    Z_mag = 1 / (1/Z_Lm + 1/Z_Cp)
    Z_total = Z_Rp + Z_Lfp + Z_Cps + Z_mag
    return Z_Cps / Z_total


def H_ACC(params):
    R_p, L_fp, *_ = params
    Z_total = R_p + 1j * omega * L_fp
    return (1j * omega * L_fp) / Z_total


def H_IC(params):
    R_p, L_fp, *_ , C_ps, _ = params
    Z_Cps = 1 / (1j * omega * C_ps)
    Z_total = R_p + 1j * omega * L_fp + Z_Cps
    return Z_Cps / Z_total


def H_II(params):
    R_p, L_fp, *_ , C_ps, _ = params
    Z_Cps = 1 / (1j * omega * C_ps)
    Z_total = R_p + 1j * omega * L_fp + Z_Cps
    return (1j * omega * L_fp) / Z_total

# Mapa de pruebas a funciones
H_funcs = {"ACA": H_ACA, "ACC": H_ACC, "IC": H_IC, "II": H_II}

# Dataset base (sano)
base_params = (R_p, L_fp, L_m, C_p, C_ps, C_s)
datasets = {"Sano": base_params}

# Generar parámetros con cada falla seleccionada
for f in faults:
    Rf, Lf, Lmf, Cp_f, Cps_f, Cs_f = base_params
    if f == "Cortocircuito de devanado":
        Lf *= 0.5
    elif f == "Incremento de capacitancia inter-devanado":
        Cps_f *= 2
    elif f == "Aumento de fuga magnética":
        Lmf *= 0.5
    elif f == "Pérdida de vueltas secundario":
        Lmf *= 0.9
        Cps_f *= 0.9
    datasets[f] = (Rf, Lf, Lmf, Cp_f, Cps_f, Cs_f)

# Graficar respuestas SFRA
fig, ax = plt.subplots(figsize=(10,6))
ref_mag = None
divergences = {}

for label, params in datasets.items():
    H = H_funcs[test](params)
    mag = 20 * np.log10(np.abs(H))
    ax.semilogx(g, mag, label=label)
    if label == "Sano":
        ref_mag = mag
    else:
        diff = np.abs(mag - ref_mag)
        idx = np.where(diff > threshold)[0]
        divergences[label] = g[idx[0]] if idx.size > 0 else None

ax.set_xlabel('Frecuencia (Hz)')
ax.set_ylabel('Magnitud (dB)')
ax.grid(True, which='both', ls='--')
ax.legend()
st.pyplot(fig)

# Mostrar puntos de divergencia
st.markdown("---")
st.write(f"Umbral de diferencia: {threshold} dB respecto a transformador sano ({test})")
for label, freq in divergences.items():
    if freq:
        st.write(f"- {label} diverge en: {freq:.1f} Hz")
    else:
        st.write(f"- {label}: no supera el umbral de {threshold} dB")
