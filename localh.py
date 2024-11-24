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

# Generate time-domain waveform
try:
    hp, hc = get_td_waveform(
        approximant=approximant,
        mass1=mass1,
        mass2=mass2,
        delta_t=delta_t,
        f_lower=f_lower,
        distance=distance,
    )

    # Calculate chirp mass and add it as a feature
    chirp_mass = ((mass1 * mass2)**(3/5)) / ((mass1 + mass2)**(1/5))
    st.sidebar.markdown(f"**Chirp Mass:** {chirp_mass:.2f} Solar Masses")

    # Plot time-domain waveform
    st.subheader("Generated Time-Domain Gravitational Waveform")
    fig_td, ax_td = plt.subplots()
    ax_td.plot(hp.sample_times, hp, label="h+ (plus polarization)")
    ax_td.plot(hc.sample_times, hc, label="hx (cross polarization)")
    ax_td.set_title("Time-Domain Gravitational Waveform")
    ax_td.set_xlabel("Time (s)")
    ax_td.set_ylabel("Strain")
    ax_td.legend()
    st.pyplot(fig_td)

except Exception as e:
    st.error(f"Error generating time-domain waveform: {e}")
