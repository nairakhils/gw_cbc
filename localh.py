import streamlit as st
from pycbc.waveform import get_td_waveform
import matplotlib.pyplot as plt

# Web app title
st.title("Gravitational Waveform Visualizer")
st.sidebar.header("Waveform Parameters")

# Sidebar inputs for waveform parameters
mass1 = st.sidebar.slider("Mass 1 (Solar Masses)", 1, 100, 30)
mass2 = st.sidebar.slider("Mass 2 (Solar Masses)", 1, 100, 30)

approximant = st.sidebar.selectbox(
    "Waveform Approximant",
    [
        "SEOBNRv4", "IMRPhenomPv2", "IMRPhenomD", "TaylorT4", "TaylorF2"
    ],
)

distance = st.sidebar.slider("Distance (Megaparsecs)", 1, 1000, 100)

delta_t = st.sidebar.select_slider(
    "Time Step (delta_t)", options=[1/4096, 1/8192, 1/16384], value=1/4096
)

f_lower = st.sidebar.slider("Lower Frequency (Hz)", 10, 100, 30)

# Generate waveform
try:
    hp, hc = get_td_waveform(
        approximant=approximant,
        mass1=mass1,
        mass2=mass2,
        delta_t=delta_t,
        f_lower=f_lower,
        distance=distance,
    )

    # Plot waveform
    st.subheader("Generated Gravitational Waveform")
    fig, ax = plt.subplots()
    ax.plot(hp.sample_times, hp, label="h+ (plus polarization)")
    ax.plot(hc.sample_times, hc, label="hx (cross polarization)")
    ax.set_title("Gravitational Waveform")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Strain")
    ax.legend()
    st.pyplot(fig)

except Exception as e:
    st.error(f"Error generating waveform: {e}")
