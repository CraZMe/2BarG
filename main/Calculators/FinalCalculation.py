import numpy as np
from scipy.integrate import trapz, cumtrapz

from main.Analysis import SignalProcessing
from main.Calculators import BetaInt
from main.Calculators.IR_calibration import IR_calibration
from main.Utilities.TwoDimVec import TwoDimVec


def final_calculation(CA):
    e_incid = []
    e_reflected = []
    e_trans = []
    striker_velocity = []
    v_in = []
    v_out = []
    F_in = []
    F_out = []
    eng_stress = []
    eng_strain_rate = []

    incid_strain = []
    trans_strain = []

    bar_surface = np.pi * (CA.bar_diameter ** 2) / 4  # [m^2]
    specimen_surface = np.pi * (CA.spec_diam ** 2) / 4  # [m^2]

    time = []

    for i in range(len(CA.corr_incid.y)):
        """
            Some physical properties (in vectors):
        """
        time.append((i + 1) * CA.tpp)

        #   Strains
        e_incid.append((4 * CA.corr_incid.y[i]) / (CA.gage_factor * CA.bridge_tension))  # [strain]
        e_reflected.append((4 * CA.corr_refle.y[i]) / (CA.gage_factor * CA.bridge_tension))  # [strain]
        e_trans.append((4 * CA.corr_trans.y[i]) / (CA.gage_factor * CA.bridge_tension))  # [strain]

        incid_strain.append((4 * CA.incid_og.y[i]) / (CA.gage_factor * CA.bridge_tension))
        trans_strain.append((4 * CA.trans_og.y[i]) / (CA.gage_factor * CA.bridge_tension))

        #   Velocities
        striker_velocity.append(-2 * e_incid[i] * CA.sound_velocity)

        v_in.append((-1) * CA.sound_velocity * (e_incid[i] - e_reflected[i]))
        v_out.append((-1) * CA.sound_velocity * e_trans[i])

        #   Forces
        F_in.append((-1) * CA.young_modulus * bar_surface * (e_incid[i] + e_reflected[i]))
        F_out.append((-1) * CA.young_modulus * bar_surface * e_trans[i])

        #   Engineering Stress
        eng_stress.append(abs(F_out[i] / specimen_surface) / (10 ** 6))  # MPa
        eng_strain_rate.append((2 * CA.sound_velocity / CA.specimen_length) * e_reflected[i])

    #   Displacements
    u_in = cumtrapz(v_in, time)
    u_out = cumtrapz(v_out, time)
    eng_strain = cumtrapz(eng_strain_rate, time)
    idx = 0

    for strain in eng_strain:
        if strain >= 1:
            break
        idx += 1

    if idx == 0:
        idx = len(eng_strain)

    eng_strain = abs(eng_strain[:idx])
    eng_stress = eng_stress[:idx]

    #   Calculate the average (mean) striker velocity:
    CA.mean_striker_velocity = SignalProcessing.mean_of_signal(striker_velocity[:idx], CA.prominence_percent,
                                                                 CA.mode, CA.spacing)

    if CA.mean_striker_velocity == -1:
        print("Unable to calcualate Mean Striker Velocity.")

    #   Make all vectors the same length:
    F_in = F_in[:idx]
    F_out = F_out[:idx]
    u_in = u_in[:idx]
    u_out = u_out[:idx]
    v_in = v_in[:idx]
    v_out = v_out[:idx]
    incid_strain = incid_strain[:idx]
    trans_strain = trans_strain[:idx]
    CA.corr_incid.y = CA.corr_incid.y[:idx]
    CA.corr_refle.y = CA.corr_refle.y[:idx]
    CA.corr_trans.y = CA.corr_trans.y[:idx]
    CA.time = time[:idx]

    CA.F_in = F_in
    CA.F_out = F_out
    CA.u_in = u_in
    CA.u_out = u_out
    CA.v_in = v_in
    CA.v_out = v_out

    CA.incid = TwoDimVec(time, incid_strain)
    CA.trans = TwoDimVec(time, trans_strain)

    n = len(CA.trans_og.y) - 1
    CA.trans_og.y = CA.trans_og.y[:n]
    CA.trans_og.x = CA.trans_og.x[:n]

    CA.incid_og.y = CA.incid_og.y[:n]
    CA.incid_og.x = CA.incid_og.x[:n]

    strain = []
    for value in eng_strain:
        strain.append(abs(value))

    surf_spec_inst = []
    true_stress = []
    true_strain = []

    #   True stress // strain calculation:
    if CA.mode == "compression":
        K = -1
    else:
        K = 1

    for i in range(idx):
        surf_spec_inst.append(abs(specimen_surface / (1 + K * strain[i])))
        true_stress.append(abs(eng_stress[i] * (1 + K * strain[i])))
        true_strain.append(abs(np.log(1 + K * strain[i])))

    CA.true_stress_strain = [true_strain, true_stress]
    CA.eng_stress_strain = [eng_strain, eng_stress]

    CA.mean_strain_rate = SignalProcessing.mean_of_signal(eng_strain_rate[:-1], CA.prominence_percent, CA.mode,
                                                            CA.spacing)

    if CA.thermal_analysis:
        CA.IR_temperature = IR_calibration(CA.IR_CAL.y, CA.IR_CAL.x,
                                           CA.TC_CAL.y, CA.TC_CAL.x,
                                           CA.IR_EXP.y)

        print("beta_int calculation starting...")
        BetaInt.beta_int(CA, true_strain, true_stress)
        print("beta_int calculation CMPLT.")

    return True