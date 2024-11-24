import streamlit as st
from pycbc.waveform import get_td_waveform
from pycbc.psd import aLIGOZeroDetHighPower
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

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

# Function to calculate ISCO radius
def calculate_isco(mass1, mass2):
    total_mass = mass1 + mass2  # Total mass in solar masses
    isco_radius = 6 * total_mass * 1.477  # ISCO radius in kilometers
    return isco_radius

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

    # Calculate and display ISCO radius
    isco_radius = calculate_isco(mass1, mass2)
    st.sidebar.markdown(f"**ISCO Radius:** {isco_radius:.2f} km")

    # Add save waveform feature
    if st.sidebar.button("Save Waveform Data"):
        waveform_df = pd.DataFrame({
            "Time (s)": hp.sample_times.numpy(),
            "h+": hp.numpy(),
            "hx": hc.numpy()
        })
        waveform_df.to_csv("waveform.csv", index=False)
        st.sidebar.success("Waveform data saved as 'waveform.csv'")

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

    # Plot detector sensitivity curve
    st.subheader("LIGO Detector Sensitivity Curve")
    psd = aLIGOZeroDetHighPower(len(hp), delta_f=1.0 / hp.duration, low_freq_cutoff=f_lower)
    freqs = np.linspace(0, 1.0 / (2 * delta_t), len(psd))
    fig_psd, ax_psd = plt.subplots()
    ax_psd.loglog(freqs[freqs > f_lower], psd[freqs > f_lower])
    ax_psd.set_title("aLIGO Zero-Detuned High Power Sensitivity")
    ax_psd.set_xlabel("Frequency (Hz)")
    ax_psd.set_ylabel("Strain Noise")
    ax_psd.grid(which='both', linestyle='--', linewidth=0.5)
    st.pyplot(fig_psd)

except Exception as e:
    st.error(f"Error generating time-domain waveform: {e}")
