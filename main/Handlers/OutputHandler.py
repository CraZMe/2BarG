from numpy import transpose, savetxt, array
import os

import plotly.graph_objects as go
from plotly.subplots import make_subplots

"""
            These function save the data and create the final report that opens once an experiment was chosen.
            The code is very long and very dull in content: it is only file saving from array vectors,
            and then some plotting of that data, in multiple ways, depending on the experiment & specimen modes.
            
            CA = CoreAnalyzer object
"""


def save_data_and_report(CA, exp_num, parameters, bar_num):

    micro_sec = [t * 1e6 for t in CA.time]

    if bar_num == 1:
        if CA.specimen_mode == "regular":
            vectors = [CA.incid_og.y, CA.incid_og.x]
            df = transpose(array(vectors))
            filepath = CA.path_folder + "/Exp #" + str(exp_num) + '/Raw Signal.csv'
            savetxt(filepath, df, delimiter=',', header='Incident [V], time [s]',
                       fmt='%s')

            vectors = [CA.corr_incid.y,
                       CA.corr_refle.y,
                       CA.time]
            df = transpose(array(vectors))
            filepath = CA.path_folder + "/Exp #" + str(exp_num) + '/Corrected Signals.csv'
            savetxt(filepath, df, delimiter=',',
                       header='Incident [V], Reflected [V], time [s]',
                       fmt='%s')

            vectors = [CA.u_in, CA.time]
            df = transpose(array(vectors))
            filepath = CA.path_folder + "/Exp #" + str(exp_num) + '/Displacement.csv'
            savetxt(filepath, df, delimiter=',', header='u_in [m], time [s]', fmt='%s')

            vectors = [CA.true_stress_strain[0], CA.true_stress_strain[1]]
            df = transpose(array(vectors))
            filepath = CA.path_folder + "/Exp #" + str(exp_num) + '/Stress-Strain True.csv'
            savetxt(filepath, df, delimiter=',', header='Strain, Stress', fmt='%s')

            vectors = [CA.eng_stress_strain[0], CA.eng_stress_strain[1]]
            df = transpose(array(vectors))
            filepath = CA.path_folder + "/Exp #" + str(exp_num) + '/Stress-Strain Engineering.csv'
            savetxt(filepath, df, delimiter=',', header='Strain, Stress', fmt='%s')

            vectors = [CA.F_in, CA.time]
            df = transpose(array(vectors))
            filepath = CA.path_folder + "/Exp #" + str(exp_num) + '/Force.csv'
            savetxt(filepath, df, delimiter=',', header='F_in [N], time [s]', fmt='%s')

            vectors = [CA.v_in, CA.time]
            df = transpose(array(vectors))
            filepath = CA.path_folder + "/Exp #" + str(exp_num) + '/Velocity.csv'
            savetxt(filepath, df, delimiter=',', header='v_in [m/s], time [s]', fmt='%s')

            fig = go.FigureWidget(
                [
                    go.Scatter(name=r'$Incident$', y=CA.incid_og.y, x=CA.incid_og.x,
                               mode=r'lines', visible=False),

                    go.Scatter(name=r'$Incident$', y=CA.corr_incid.y, x=micro_sec,
                               mode='lines', visible=False),
                    go.Scatter(name=r'$Reflected$', y=CA.corr_refle.y, x=micro_sec,
                               mode='lines', visible=False),

                    go.Scatter(name=r'$U_{in}$', y=CA.u_in, x=micro_sec,
                               mode='lines', visible=False),

                    go.Scatter(name=r'$\sigma_{Engineering}$', y=CA.eng_stress_strain[1],
                               x=CA.eng_stress_strain[0], mode='lines'),
                    go.Scatter(name=r'$True$', y=CA.true_stress_strain[1],
                               x=CA.true_stress_strain[0], mode='lines'),

                    go.Scatter(name=r'$F_{in}$', y=CA.F_in, x=micro_sec,
                               mode='lines', visible=False),

                    go.Scatter(name=r'$V_{in}$', y=CA.v_in, x=micro_sec,
                               mode='lines', visible=False)

                ]
            )

            fig.update_layout(title_x=0.45, template='none',
                              font=dict(family="Times New Roman", size=25),
                              legend=dict(yanchor='top', xanchor='right', y=1.1, x=1,
                                          font=dict(size=30)),
                              margin=dict(l=150, r=500, t=200, b=250),
                              updatemenus=[go.layout.Updatemenu(
                                  active=3,
                                  buttons=list(
                                      [dict(label='Raw Signal',
                                            method='update',
                                            args=[{'visible': [True] + [False] * 7},
                                                  {'title': 'Raw Signals',
                                                   'xaxis': {'title': r'$Time [μs]$'},
                                                   'yaxis': {'title': r'$Amplitude [V]$'},
                                                   'showlegend': True}]),

                                       dict(label='Corrected Signals',
                                            method='update',
                                            args=[{'visible': [False] + [True] * 2 + [False] * 5},
                                                  {'title': r'$Corrected Signals$',
                                                   'xaxis': {'title': r'$Time [μs]$'},
                                                   'yaxis': {'title': r'$Amplitude [V]$'},
                                                   'showlegend': True}]),

                                       dict(label='Displacement',
                                            method='update',
                                            args=[{'visible': [False] * 3 + [True] + [False] * 4},
                                                  {'title': r'$Displacement$',
                                                   'xaxis': {'title': r'$Time [μs]$'},
                                                   'yaxis': {'title': r'$Displacement [m]$'},
                                                   'showlegend': True}]),

                                       dict(label='Stress - Strain',
                                            method='update',
                                            args=[{'visible': [False] * 4 + [True] * 2 + [False] * 2},
                                                  {'title': r'$Stress - Strain$',
                                                   'xaxis': {'title': r'$\epsilon [strain]$'},
                                                   'yaxis': {'title': r'$Stress [MPa]$'},
                                                   'showlegend': True}]),

                                       dict(label='Force',
                                            method='update',
                                            args=[{'visible': [False] * 6 + [True] + [False]},
                                                  {'title': r'$Forces$',
                                                   'xaxis': {'title': r'$Time [μs]$'},
                                                   'yaxis': {'title': r'$Force [N]$'},
                                                   'showlegend': True}]),

                                       dict(label='Velocity',
                                            method='update',
                                            args=[{'visible': [False] * 7 + [True]},
                                                  {'title': r'$Velocity$',
                                                   'xaxis': {'title': r'$Time [μs]$'},
                                                   'yaxis': {'title': r'$Velocity [m/s]$'},
                                                   'showlegend': True}]

                                            ),
                                       ]),
                                  x=0.9, y=1.1
                              )
                              ])

        if CA.specimen_mode == "shear":
            vectors = [CA.strain.y, CA.time]
            df = transpose(array(vectors))
            filepath = CA.path_folder + "/Exp #" + str(exp_num) + '/Bar Strain.csv'
            savetxt(filepath, df, delimiter=',',
                       header='incident strain, time [s]',
                       fmt='%s')

            vectors = [CA.incid_og.y, CA.incid_og.x]
            df = transpose(array(vectors))
            filepath = CA.path_folder + "/Exp #" + str(exp_num) + '/Raw Signal.csv'
            savetxt(filepath, df, delimiter=',', header='Incident [V], time [s]',
                       fmt='%s')

            vectors = [CA.corr_incid.y,
                       CA.corr_refle.y,
                       CA.time]

            df = transpose(array(vectors))
            filepath = CA.path_folder + "/Exp #" + str(exp_num) + '/Corrected Signals.csv'
            savetxt(filepath, df, delimiter=',',
                       header='Incident [V], Reflected [V], time [s]',
                       fmt='%s')

            vectors = [CA.u_in, CA.time]
            df = transpose(array(vectors))
            filepath = CA.path_folder + "/Exp #" + str(exp_num) + '/Displacement.csv'
            savetxt(filepath, df, delimiter=',', header='u_in [m], time [s]', fmt='%s')

            vectors = [CA.F_in, CA.time]
            df = transpose(array(vectors))
            filepath = CA.path_folder + "/Exp #" + str(exp_num) + '/Forces.csv'
            savetxt(filepath, df, delimiter=',', header='F_in [N], time [s]', fmt='%s')

            vectors = [CA.v_in, CA.time]
            df = transpose(array(vectors))
            filepath = CA.path_folder + "/Exp #" + str(exp_num) + '/Velocity.csv'
            savetxt(filepath, df, delimiter=',', header='v_in [m/s], time [s]', fmt='%s')

            fig = go.FigureWidget(
                [
                    go.Scatter(name=r'$Incident$', y=CA.incid_og.y, x=CA.incid_og.x,
                               mode='lines', visible=False),

                    go.Scatter(name=r'$Incident$', y=CA.corr_incid.y, x=micro_sec,
                               mode='lines', visible=False),
                    go.Scatter(name=r'$Reflected$', y=CA.corr_refle.y, x=micro_sec,
                               mode='lines', visible=False),

                    go.Scatter(name=r'$U_{in}$', y=CA.u_in, x=micro_sec,
                               mode='lines', visible=False),

                    go.Scatter(name=r'$F_{in}$', y=CA.F_in, x=micro_sec,
                               mode='lines', visible=True),

                    go.Scatter(name=r'$V_{in}$', y=CA.v_in, x=micro_sec,
                               mode='lines', visible=False),

                ]
            )

            fig.update_layout(title_x=0.45, template='none',
                              font=dict(family="Times New Roman", size=25),
                              legend=dict(yanchor='top', xanchor='right', y=1.1, x=1,
                                          font=dict(size=30)),
                              margin=dict(l=150, r=500, t=200, b=250),
                              updatemenus=[go.layout.Updatemenu(
                                  active=3,
                                  buttons=list(
                                      [dict(label='Raw Signal',
                                            method='update',
                                            args=[{'visible': [True] + [False] * 5},
                                                  {'title': r'$Raw Signals$',
                                                   'xaxis': {'title': r'$Time [μs]$'},
                                                   'yaxis': {'title': r'$Amplitude [V]$'},
                                                   'showlegend': True}]),

                                       dict(label='Corrected Signals',
                                            method='update',
                                            args=[{'visible': [False] + [True] * 2 + [False] * 3},
                                                  {'title': r'$Corrected Signals$',
                                                   'xaxis': {'title': r'$Time [μs]$'},
                                                   'yaxis': {'title': r'$Amplitude [V]$'},
                                                   'showlegend': True}]),

                                       dict(label='Displacement',
                                            method='update',
                                            args=[{'visible': [False] * 3 + [True] + [False] * 2},
                                                  {'title': r'$Displacement$',
                                                   'xaxis': {'title': r'$Time [μs]$'},
                                                   'yaxis': {'title': r'$Displacement [m]$'},
                                                   'showlegend': True}]),

                                       dict(label='Forces',
                                            method='update',
                                            args=[{'visible': [False] * 4 + [True] + [False]},
                                                  {'title': r'$Force$',
                                                   'xaxis': {'title': r'$Time [μs]$'},
                                                   'yaxis': {'title': r'$Force [N]$'},
                                                   'showlegend': True}]),

                                       dict(label='Velocities',
                                            method='update',
                                            args=[{'visible': [False] * 5 + [True]},
                                                  {'title': r'$Velocity$',
                                                   'xaxis': {'title': r'$Time [μs]$'},
                                                   'yaxis': {'title': r'$Velocity [m/s]$'},
                                                   'showlegend': True}]

                                            ),
                                       ]),
                                  x=0.9, y=1.1
                              )
                              ])
        try:
            fig.add_annotation(dict(font=dict(color='red', size=16),
                                    font_family="Garamound",
                                    x=1,
                                    y=0.1,
                                    showarrow=False,
                                    text="Average Strain Rate: " + str(int(CA.mean_strain_rate)) + " [1/s]",
                                    textangle=0,
                                    xanchor='left',
                                    xref="paper",
                                    yref="paper"))
        except:
            print("mean strain rate could not be calculated.")

        fig.add_annotation(dict(font=dict(color='black', size=16),
                                font_family="Garamound",
                                x=1,
                                y=0.37,
                                showarrow=False,
                                font_color='blue',
                                text="<b>Experiment Parameters:<b>                   ",
                                textangle=0,
                                xanchor='left',
                                xref="paper",
                                yref="paper"))

        fig.add_annotation(dict(font=dict(color='black', size=14),
                                font_family="Garamound",
                                x=1,
                                y=0.32,
                                showarrow=False,
                                text="Specimen Diameter: " + str(parameters[0][1]) + " [m]",
                                textangle=0,
                                xanchor='left',
                                xref="paper",
                                yref="paper"))

        fig.add_annotation(dict(font=dict(color='black', size=14),
                                font_family="Garamound",
                                x=1,
                                y=0.29,
                                showarrow=False,
                                text="Specimen Length: " + str(parameters[1][1]) + " [m]",
                                textangle=0,
                                xanchor='left',
                                xref="paper",
                                yref="paper"))

        fig.add_annotation(dict(font=dict(color='black', size=14),
                                font_family="Garamound",
                                x=1,
                                y=0.26,
                                showarrow=False,
                                text="Bar Diameter: " + str(parameters[2][1]) + " [m]",
                                textangle=0,
                                xanchor='left',
                                xref="paper",
                                yref="paper"))

        fig.add_annotation(dict(font=dict(color='black', size=14),
                                font_family="Garamound",
                                x=1,
                                y=0.23,
                                showarrow=False,
                                text="Young's Modulus: " + str(parameters[3][1] / (10 ** 9)) + " [GPa]",
                                textangle=0,
                                xanchor='left',
                                xref="paper",
                                yref="paper"))

        fig.add_annotation(dict(font=dict(color='black', size=14),
                                font_family="Garamound",
                                x=1,
                                y=0.2,
                                showarrow=False,
                                text="Sound Velocity in Bar: " + str(parameters[6][1]) + " [m/s]",
                                textangle=0,
                                xanchor='left',
                                xref="paper",
                                yref="paper"))

        fig.add_annotation(dict(font=dict(color='black', size=14),
                                font_family="Garamound",
                                x=1,
                                y=0.17,
                                showarrow=False,
                                text="Bridge Tension: " + str(parameters[8][1]) + " [V]",
                                textangle=0,
                                xanchor='left',
                                xref="paper",
                                yref="paper"))

        fig.add_annotation(dict(font=dict(color='black', size=14),
                                font_family="Garamound",
                                x=1,
                                y=0.14,
                                showarrow=False,
                                text="Striker Velocity: " + str("%.2f" % CA.mean_striker_velocity) + " [m/s]",
                                textangle=0,
                                xanchor='left',
                                xref="paper",
                                yref="paper"))

        fig.add_annotation(dict(font=dict(color='black', size=18),
                                font_family="Garamound",
                                x=1,
                                y=0.6,
                                showarrow=False,
                                text="<b>Experiment no. " + str(exp_num) + "<b>",
                                textangle=0,
                                xanchor='left',
                                xref="paper",
                                yref="paper"))

        fig.add_annotation(dict(font=dict(color='black', size=14),
                                font_family="Garamound",
                                x=1,
                                y=0.56,
                                showarrow=False,
                                text="Specimen type: " + str(CA.specimen_mode),
                                textangle=0,
                                xanchor='left',
                                xref="paper",
                                yref="paper"))

        fig.add_annotation(dict(font=dict(color='black', size=14),
                                font_family="Garamound",
                                x=1,
                                y=0.54,
                                showarrow=False,
                                text="Experiment mode: " + str(CA.mode),
                                textangle=0,
                                xanchor='left',
                                xref="paper",
                                yref="paper"))

        fig.add_annotation(dict(font=dict(color='black', size=20),
                                font_family="Garamound",
                                x=1,
                                y=0.8,
                                showarrow=False,
                                text="main Analysis Report",
                                textangle=0,
                                xanchor='left',
                                xref="paper",
                                yref="paper"))

        fig.update_layout(margin=dict(r=250))
        fig.write_html(CA.path_folder + "\Exp " + str(exp_num) + '.html',
                       auto_open=CA.auto_open_report,
                       include_mathjax='cdn')

    elif bar_num == 2:
        if CA.specimen_mode == "regular":
            vectors = [CA.incid_og.y, CA.trans_og.y, CA.incid_og.x]
            df = transpose(array(vectors))
            filepath = CA.path_folder + "/Exp #" + str(exp_num) + '/Raw Signals.csv'
            savetxt(filepath, df, delimiter=',', header='Incident [V], Transmitted [V], time [s]',
                       fmt='%s')

            vectors = [CA.corr_incid.y,
                       CA.corr_refle.y,
                       CA.corr_trans.y,
                       CA.time]
            df = transpose(array(vectors))
            filepath = CA.path_folder + "/Exp #" + str(exp_num) + '/Corrected Signals.csv'
            savetxt(filepath, df, delimiter=',',
                       header='Incident [V], Reflected [V], Transmitted [V], time [s]',
                       fmt='%s')

            vectors = [CA.u_in, CA.u_out, CA.time]
            df = transpose(array(vectors))
            filepath = CA.path_folder + "/Exp #" + str(exp_num) + '/Displacements.csv'
            savetxt(filepath, df, delimiter=',', header='u_in [m], u_out [m], time [s]', fmt='%s')

            vectors = [CA.true_stress_strain[0], CA.true_stress_strain[1]]
            df = transpose(array(vectors))
            filepath = CA.path_folder + "/Exp #" + str(exp_num) + '/Stress-Strain True.csv'
            savetxt(filepath, df, delimiter=',', header='Strain, Stress', fmt='%s')

            vectors = [CA.eng_stress_strain[0], CA.eng_stress_strain[1]]
            df = transpose(array(vectors))
            filepath = CA.path_folder + "/Exp #" + str(exp_num) + '/Stress-Strain Engineering.csv'
            savetxt(filepath, df, delimiter=',', header='Strain, Stress', fmt='%s')

            vectors = [CA.F_in, CA.F_out, CA.time]
            df = transpose(array(vectors))
            filepath = CA.path_folder + "/Exp #" + str(exp_num) + '/Forces.csv'
            savetxt(filepath, df, delimiter=',', header='F_in [N], F_out [N], time [s]', fmt='%s')

            vectors = [CA.v_in, CA.v_out, CA.time]
            df = transpose(array(vectors))
            filepath = CA.path_folder + "/Exp #" + str(exp_num) + '/Velocities.csv'
            savetxt(filepath, df, delimiter=',', header='v_in [m/s], v_out [m/s], time [s]', fmt='%s')

            fig = make_subplots()
            fig.add_trace(go.Scatter(name=r'$Incident$', y=CA.incid_og.y, x=CA.incid_og.x,
                       mode='lines', visible=False))
            fig.add_trace(go.Scatter(name=r'$Transmitted$', y=CA.trans_og.y, x=CA.trans_og.x,
                       mode='lines', visible=False))

            fig.add_trace(go.Scatter(name=r'$Incident$', y=CA.corr_incid.y, x=micro_sec,
                       mode='lines', visible=False))
            fig.add_trace(go.Scatter(name=r'$Transmitted$', y=CA.corr_trans.y, x=micro_sec,
                       mode='lines', visible=False))
            fig.add_trace(go.Scatter(name=r'$Reflected$', y=CA.corr_refle.y, x=micro_sec,
                       mode='lines', visible=False))

            fig.add_trace(go.Scatter(name=r'$U_{in}$', y=CA.u_in, x=micro_sec,
                       mode='lines', visible=False))
            fig.add_trace(go.Scatter(name=r'$U_{out}$', y=CA.u_out, x=micro_sec,
                       mode='lines', visible=False))

            fig.add_trace(go.Scatter(name=r'$\sigma_{Engineering}$', y=CA.eng_stress_strain[1],
                       x=CA.eng_stress_strain[0], mode='lines'))
            fig.add_trace(go.Scatter(name=r'$\sigma_{True}$', y=CA.true_stress_strain[1],
                       x=CA.true_stress_strain[0], mode='lines'))

            fig.add_trace(go.Scatter(name='$F_{in}$', y=CA.F_in, x=micro_sec,
                       mode='lines', visible=False))
            fig.add_trace(go.Scatter(name=r'$F_{out}$', y=CA.F_out, x=micro_sec,
                       mode='lines', visible=False))

            fig.add_trace(go.Scatter(name=r'$V_{in}$', y=CA.v_in, x=micro_sec,
                       mode='lines', visible=False))
            fig.add_trace(go.Scatter(name=r'$V_{out}$', y=CA.v_out, x=micro_sec,
                       mode='lines', visible=False))

            fig.update_layout(title_x=0.45, template='none',
                              font=dict(family="Times New Roman", size=25),
                              legend=dict(yanchor='top', xanchor='right', y=1.1, x=1,
                                          font=dict(size=30)),
                              margin=dict(l=150, r=500, t=200, b=250),
                              updatemenus=[go.layout.Updatemenu(
                                  active=3,
                                  buttons=list(
                                      [dict(label='Raw Signals',
                                            method='update',
                                            args=[{'visible': [True, True] + [False] * 11},
                                                  {'title': r'$Raw Signals$',
                                                   'xaxis': {'title': r'$Time [μs]$'},
                                                   'yaxis': {'title': r'$Amplitude [V]$'},
                                                   'showlegend': True}]),

                                       dict(label='Corrected Signals',
                                            method='update',
                                            args=[{'visible': [False] * 2 + [True] * 3 + [False] * 8},
                                                  {'title': r'$Corrected Signals$',
                                                   'xaxis': {'title': r'$Time [μs]$'},
                                                   'yaxis': {'title': r'$Amplitude [V]$'},
                                                   'showlegend': True}]),

                                       dict(label='Displacements',
                                            method='update',
                                            args=[{'visible': [False] * 5 + [True] * 2 + [False] * 6},
                                                  {'title': r'$Displacements$',
                                                   'xaxis': {'title': r'$Time [μs]$'},
                                                   'yaxis': {'title': r'$Displacement [m]$'},
                                                   'showlegend': True}]),

                                       dict(label='Stress - Strain',
                                            method='update',
                                            args=[{'visible': [False] * 7 + [True] * 2 + [False] * 4},
                                                  {'title': r'$Stress - Strain$',
                                                   'xaxis': {'title': r'$\epsilon [strain]$'},
                                                   'yaxis': {'title': 'Stress [MPa]'},
                                                   'showlegend': True}]),

                                       dict(label='Forces',
                                            method='update',
                                            args=[{'visible': [False] * 9 + [True] * 2 + [False] * 2},
                                                  {'title': r'$Forces$',
                                                   'xaxis': {'title': r'$Time [μs]$'},
                                                   'yaxis': {'title': r'$Force [N]$'},
                                                   'showlegend': True}]),

                                       dict(label='Velocities',
                                            method='update',
                                            args=[{'visible': [False] * 11 + [True] * 2},
                                                  {'title': r'$Velocities$',
                                                   'xaxis': {'title': r'$Time [μs]$'},
                                                   'yaxis': {'title': r'$Velocity [m/s]$'},
                                                   'showlegend': True}]

                                            ),
                                       ]),
                                  x=0.1, y=1.1
                              )
                              ])

        if CA.specimen_mode == "shear":
            vectors = [CA.strain.y, CA.trans.y, CA.time]
            df = transpose(array(vectors))
            filepath = CA.path_folder + "/Exp #" + str(exp_num) + '/Bar Strains.csv'
            savetxt(filepath, df, delimiter=',',
                       header='incident strain, transmitted strain, time [s]',
                       fmt='%s')

            vectors = [CA.incid_og.y, CA.trans_og.y, CA.incid_og.x]
            df = transpose(array(vectors))
            filepath = CA.path_folder + "/Exp #" + str(exp_num) + '/Raw Signals.csv'
            savetxt(filepath, df, delimiter=',', header='Incident [V], Transmitted [V], time [s]',
                       fmt='%s')

            vectors = [CA.corr_incid.y,
                       CA.corr_refle.y,
                       CA.corr_trans.y,
                       CA.time]
            df = transpose(array(vectors))
            filepath = CA.path_folder + "/Exp #" + str(exp_num) + '/Corrected Signals.csv'
            savetxt(filepath, df, delimiter=',',
                       header='Incident [V], Reflected [V], Transmitted [V], time [s]',
                       fmt='%s')

            vectors = [CA.u_in, CA.u_out, CA.time]
            df = transpose(array(vectors))
            filepath = CA.path_folder + "/Exp #" + str(exp_num) + '/Displacements.csv'
            savetxt(filepath, df, delimiter=',', header='u_in [m], u_out [m], time [s]', fmt='%s')

            vectors = [CA.F_in, CA.F_out, CA.time]
            df = transpose(array(vectors))
            filepath = CA.path_folder + "/Exp #" + str(exp_num) + '/Forces.csv'
            savetxt(filepath, df, delimiter=',', header='F_in [N], F_out [N], time [s]', fmt='%s')

            vectors = [CA.v_in, CA.v_out, CA.time]
            df = transpose(array(vectors))
            filepath = CA.path_folder + "/Exp #" + str(exp_num) + '/Velocities.csv'
            savetxt(filepath, df, delimiter=',', header='v_in [m/s], v_out [m/s], time [s]', fmt='%s')

            fig = make_subplots()
            fig.add_trace(go.Scatter(name=r'$Incident$', y=CA.incid_og.y, x=CA.incid_og.x,
                               mode='lines', visible=False))
            fig.add_trace(go.Scatter(name=r'$Transmitted$', y=CA.trans_og.y, x=CA.trans_og.x,
                               mode='lines', visible=False))

            fig.add_trace(go.Scatter(name=r'$Incident$', y=CA.corr_incid.y, x=micro_sec,
                       mode='lines', visible=False))
            fig.add_trace(go.Scatter(name=r'$Transmitted$', y=CA.corr_trans.y, x=micro_sec,
                       mode='lines', visible=False))
            fig.add_trace(go.Scatter(name=r'$Reflected$', y=CA.corr_refle.y, x=micro_sec,
                       mode='lines', visible=False))

            fig.add_trace(go.Scatter(name=r'$U_{in}$', y=CA.u_in, x=micro_sec,
                       mode='lines', visible=False))
            fig.add_trace(go.Scatter(name=r'$U_{out}$', y=CA.u_out, x=micro_sec,
                       mode='lines', visible=False))

            fig.add_trace(go.Scatter(name=r'$F_{in}$', y=CA.F_in, x=micro_sec,
                       mode='lines', visible=True))
            fig.add_trace(go.Scatter(name=r'$F_{out}$', y=CA.F_out, x=micro_sec,
                       mode='lines', visible=True))

            fig.add_trace(go.Scatter(name=r'$V_{in}$', y=CA.v_in, x=micro_sec,
                       mode='lines', visible=False))
            fig.add_trace(go.Scatter(name=r'$V_{out}$', y=CA.v_out, x=micro_sec,
                       mode='lines', visible=False))

            fig.update_layout(title_x=0.45, template='none',
                              font=dict(family="Times New Roman", size=25),
                              legend=dict(yanchor='top', xanchor='right', y=1.1, x=1,
                                          font=dict(size=30)),
                              margin=dict(l=150, r=500, t=200, b=250),
                              updatemenus=[go.layout.Updatemenu(
                                  active=3,
                                  buttons=list(
                                      [dict(label='Raw Signals',
                                            method='update',
                                            args=[{'visible': [True, True] + [False] * 9},
                                                  {'title': r'$Raw Signals$',
                                                   'xaxis': {'title': r'$Time [μs]$'},
                                                   'yaxis': {'title': r'$Amplitude [V]$'},
                                                   'showlegend': True}]),

                                       dict(label='Corrected Signals',
                                            method='update',
                                            args=[{'visible': [False] * 2 + [True] * 3 + [False] * 6},
                                                  {'title': r'$Corrected Signals$',
                                                   'xaxis': {'title': r'$Time [μs]$'},
                                                   'yaxis': {'title': r'$Amplitude [V]$'},
                                                   'showlegend': True}]),

                                       dict(label='Displacement',
                                            method='update',
                                            args=[{'visible': [False] * 5 + [True] * 2 + [False] * 4},
                                                  {'title': r'$Displacements$',
                                                   'xaxis': {'title': r'$Time [μs]$'},
                                                   'yaxis': {'title': r'$Displacement [m]$'},
                                                   'showlegend': True}]),

                                       dict(label='Forces',
                                            method='update',
                                            args=[{'visible': [False] * 7 + [True] * 2 + [False] * 2},
                                                  {'title': r'$Forces$',
                                                   'xaxis': {'title': r'$Time [μs]$'},
                                                   'yaxis': {'title': r'$Force [N]$'},
                                                   'showlegend': True}]),

                                       dict(label='Velocities',
                                            method='update',
                                            args=[{'visible': [False] * 9 + [True] * 2},
                                                  {'title': r'$Velocities$',
                                                   'xaxis': {'title': r'$Time [μs]$'},
                                                   'yaxis': {'title': r'$Velocity [m/s]$'},
                                                   'showlegend': True}]

                                            ),
                                       ]),
                                  x=0.1, y=1.1)
                              ])
        try:
            fig.add_annotation(dict(font=dict(color='red', size=16),
                                    font_family="Garamound",
                                    x=1.02,
                                    y=0.1,
                                    showarrow=False,
                                    text="Average Strain Rate: " + str(int(CA.mean_strain_rate)) + " [1/s]",
                                    textangle=0,
                                    xanchor='left',
                                    xref="paper",
                                    yref="paper"))
        except:
            print("Mean Strain Rate could not be calcualted")

        fig.add_annotation(dict(font=dict(color='black', size=16),
                                font_family="Garamound",
                                x=1.02,
                                y=0.37,
                                showarrow=False,
                                font_color='blue',
                                text="<b>Experiment Parameters:<b>                   ",
                                textangle=0,
                                xanchor='left',
                                xref="paper",
                                yref="paper"))

        fig.add_annotation(dict(font=dict(color='black', size=14),
                                font_family="Garamound",
                                x=1.02,
                                y=0.32,
                                showarrow=False,
                                text="Specimen Diameter: " + str(parameters[0][1]) + " [m]",
                                textangle=0,
                                xanchor='left',
                                xref="paper",
                                yref="paper"))

        fig.add_annotation(dict(font=dict(color='black', size=14),
                                font_family="Garamound",
                                x=1.02,
                                y=0.29,
                                showarrow=False,
                                text="Specimen Length: " + str(parameters[1][1]) + " [m]",
                                textangle=0,
                                xanchor='left',
                                xref="paper",
                                yref="paper"))

        fig.add_annotation(dict(font=dict(color='black', size=14),
                                font_family="Garamound",
                                x=1.02,
                                y=0.26,
                                showarrow=False,
                                text="Bar Diameter: " + str(parameters[2][1]) + " [m]",
                                textangle=0,
                                xanchor='left',
                                xref="paper",
                                yref="paper"))

        fig.add_annotation(dict(font=dict(color='black', size=14),
                                font_family="Garamound",
                                x=1.02,
                                y=0.23,
                                showarrow=False,
                                text="Young's Modulus: " + str(parameters[3][1] / (10 ** 9)) + " [GPa]",
                                textangle=0,
                                xanchor='left',
                                xref="paper",
                                yref="paper"))

        fig.add_annotation(dict(font=dict(color='black', size=14),
                                font_family="Garamound",
                                x=1.02,
                                y=0.2,
                                showarrow=False,
                                text="Sound Velocity in Bar: " + str(parameters[6][1]) + " [m/s]",
                                textangle=0,
                                xanchor='left',
                                xref="paper",
                                yref="paper"))

        fig.add_annotation(dict(font=dict(color='black', size=14),
                                font_family="Garamound",
                                x=1.02,
                                y=0.17,
                                showarrow=False,
                                text="Bridge Tension: " + str(parameters[8][1]) + " [V]",
                                textangle=0,
                                xanchor='left',
                                xref="paper",
                                yref="paper"))

        fig.add_annotation(
                                dict(font=dict(color='black', size=14),
                                     font_family="Garamound",
                                     x=1.02,
                                     y=0.14,
                                     showarrow=False,
                                text="Striker Velocity: " + str("%.2f" % CA.mean_striker_velocity) + " [m/s]",
                                textangle=0,
                                xanchor='left',
                                xref="paper",
                                yref="paper"))

        fig.add_annotation(dict(font=dict(color='black', size=18),
                                font_family="Garamound",
                                x=1.02,
                                y=0.6,
                                showarrow=False,
                                text="<b>Experiment no. " + str(exp_num) + "<b>",
                                textangle=0,
                                xanchor='left',
                                xref="paper",
                                yref="paper"))

        fig.add_annotation(dict(font=dict(color='black', size=14),
                                font_family="Garamound",
                                x=1.02,
                                y=0.56,
                                showarrow=False,
                                text="Specimen type: " + str(CA.specimen_mode),
                                textangle=0,
                                xanchor='left',
                                xref="paper",
                                yref="paper"))

        fig.add_annotation(dict(font=dict(color='black', size=14),
                                font_family="Garamound",
                                x=1.02,
                                y=0.54,
                                showarrow=False,
                                text="Experiment mode: " + str(CA.mode),
                                textangle=0,
                                xanchor='left',
                                xref="paper",
                                yref="paper"))

        fig.add_annotation(dict(font=dict(color='black', size=20),
                                font_family="Garamound",
                                x=1.02,
                                y=0.8,
                                showarrow=False,
                                text="main Analysis Report",
                                textangle=0,
                                xanchor='left',
                                xref="paper",
                                yref="paper"))

        fig.update_layout(margin=dict(r=250))
        fig.write_html(CA.path_folder + "\Exp " + str(exp_num) + '.html',
                       auto_open=CA.auto_open_report,
                       include_mathjax='cdn')
    f_path = CA.path_folder + "\Exp #" + str(exp_num) + "\Parameters.txt"

    if os.path.isfile(f_path):
        os.remove(f_path)
    f = open(f_path, 'x')
    f = open(f_path, 'r+')
    f.truncate(0)
    s = ""

    s += str(parameters[0][0]) + ": " + str(parameters[0][1]) + " [m]" + "\n"
    s += str(parameters[1][0]) + ": " + str(parameters[1][1]) + " [m]" + "\n"
    s += str(parameters[2][0]) + ": " + str(parameters[2][1]) + " [m]" + "\n"
    s += str(parameters[3][0]) + ": " + str(parameters[3][1] / (10 ** 9)) + " [GPa]" + "\n"
    s += str(parameters[4][0]) + ": " + str(parameters[4][1]) + " [m]" + "\n"
    s += str(parameters[5][0]) + ": " + str(parameters[5][1]) + " [m]" + "\n"
    s += str(parameters[6][0]) + ": " + str(parameters[6][1]) + " [m/s]" + "\n"
    s += str(parameters[7][0]) + ": " + str(parameters[7][1]) + "\n"
    s += str(parameters[8][0]) + ": " + str(parameters[8][1]) + " [V]" + "\n"
    s += "Spacing: " + str(CA.spacing) + " Points" + "\n"
    s += "Prominence: " + str(CA.prominence_percent * 100) + "%" + "\n"
    s += "Curve Smoothing Parameter: " + str(CA.smooth_value * 100) + "\n"
    s += "Average Strain Rate: " + str(CA.mean_strain_rate) + "[1/s]"
    s += "\n"  # For some reason, there is a problem without a new line at the end of the defaults file.
    f.write(s)
    f.close()


def save_data_and_report_thermal(CA, exp_num, parameters, bar_num):
    micro_sec = [t * 1e6 for t in CA.time]
    os.makedirs(CA.path_folder + "\Analysis Results")

    if bar_num == 1:
        if CA.specimen_mode == "regular":
            vectors = [CA.incid_og.y, CA.incid_og.x]
            df = transpose(array(vectors))
            filepath = CA.path_folder + "/Exp #" + str(exp_num) + '/Raw Signal.csv'
            savetxt(filepath, df, delimiter=',', header='Incident [V], time [s]',
                       fmt='%s')

            vectors = [CA.corr_incid.y,
                       CA.corr_refle.y,
                       CA.time]
            df = transpose(array(vectors))
            filepath = CA.path_folder + "/Exp #" + str(exp_num) + '/Corrected Signals.csv'
            savetxt(filepath, df, delimiter=',',
                       header='Incident [V], Reflected [V], time [s]',
                       fmt='%s')

            vectors = [CA.u_in, CA.time]
            df = transpose(array(vectors))
            filepath = CA.path_folder + "/Exp #" + str(exp_num) + '/Displacement.csv'
            savetxt(filepath, df, delimiter=',', header='u_in [m], time [s]', fmt='%s')

            vectors = [CA.true_stress_strain[0], CA.true_stress_strain[1]]
            df = transpose(array(vectors))
            filepath = CA.path_folder + "/Exp #" + str(exp_num) + '/Stress-Strain True.csv'
            savetxt(filepath, df, delimiter=',', header='Strain, Stress', fmt='%s')

            vectors = [CA.eng_stress_strain[0], CA.eng_stress_strain[1]]
            df = transpose(array(vectors))
            filepath = CA.path_folder + "/Exp #" + str(exp_num) + '/Stress-Strain Engineering.csv'
            savetxt(filepath, df, delimiter=',', header='Strain, Stress', fmt='%s')

            vectors = [CA.F_in, CA.time]
            df = transpose(array(vectors))
            filepath = CA.path_folder + "/Exp #" + str(exp_num) + '/Force.csv'
            savetxt(filepath, df, delimiter=',', header='F_in [N], time [s]', fmt='%s')

            vectors = [CA.v_in, CA.time]
            df = transpose(array(vectors))
            filepath = CA.path_folder + "/Exp #" + str(exp_num) + '/Velocity.csv'
            savetxt(filepath, df, delimiter=',', header='v_in [m/s], time [s]', fmt='%s')

            fig = go.FigureWidget(
                [
                    go.Scatter(name=r'$Incident$', y=CA.incid_og.y, x=CA.incid_og.x,
                               mode=r'lines', visible=False),

                    go.Scatter(name=r'$Incident$', y=CA.corr_incid.y, x=micro_sec,
                               mode='lines', visible=False),
                    go.Scatter(name=r'$Reflected$', y=CA.corr_refle.y, x=micro_sec,
                               mode='lines', visible=False),

                    go.Scatter(name=r'$U_{in}$', y=CA.u_in, x=micro_sec,
                               mode='lines', visible=False),

                    go.Scatter(name=r'$\sigma_{Engineering}$', y=CA.eng_stress_strain[1],
                               x=CA.eng_stress_strain[0], mode='lines'),
                    go.Scatter(name=r'$True$', y=CA.true_stress_strain[1],
                               x=CA.true_stress_strain[0], mode='lines'),

                    go.Scatter(name=r'$F_{in}$', y=CA.F_in, x=micro_sec,
                               mode='lines', visible=False),

                    go.Scatter(name=r'$V_{in}$', y=CA.v_in, x=micro_sec,
                               mode='lines', visible=False)

                ]
            )

            fig.update_layout(title_x=0.45, template='none',
                              font=dict(family="Times New Roman", size=25),
                              legend=dict(yanchor='top', xanchor='right', y=1.1, x=1,
                                          font=dict(size=30)),
                              margin=dict(l=150, r=500, t=200, b=250),
                              updatemenus=[go.layout.Updatemenu(
                                  active=3,
                                  buttons=list(
                                      [dict(label='Raw Signal',
                                            method='update',
                                            args=[{'visible': [True] + [False] * 7},
                                                  {'title': 'Raw Signals',
                                                   'xaxis': {'title': r'$Time [μs]$'},
                                                   'yaxis': {'title': r'$Amplitude [V]$'},
                                                   'showlegend': True}]),

                                       dict(label='Corrected Signals',
                                            method='update',
                                            args=[{'visible': [False] + [True] * 2 + [False] * 5},
                                                  {'title': r'$Corrected Signals$',
                                                   'xaxis': {'title': r'$Time [μs]$'},
                                                   'yaxis': {'title': r'$Amplitude [V]$'},
                                                   'showlegend': True}]),

                                       dict(label='Displacement',
                                            method='update',
                                            args=[{'visible': [False] * 3 + [True] + [False] * 4},
                                                  {'title': r'$Displacement$',
                                                   'xaxis': {'title': r'$Time [μs]$'},
                                                   'yaxis': {'title': r'$Displacement [m]$'},
                                                   'showlegend': True}]),

                                       dict(label='Stress - Strain',
                                            method='update',
                                            args=[{'visible': [False] * 4 + [True] * 2 + [False] * 2},
                                                  {'title': r'$Stress - Strain$',
                                                   'xaxis': {'title': r'$\epsilon [strain]$'},
                                                   'yaxis': {'title': r'$Stress [MPa]$'},
                                                   'showlegend': True}]),

                                       dict(label='Force',
                                            method='update',
                                            args=[{'visible': [False] * 6 + [True] + [False]},
                                                  {'title': r'$Forces$',
                                                   'xaxis': {'title': r'$Time [μs]$'},
                                                   'yaxis': {'title': r'$Force [N]$'},
                                                   'showlegend': True}]),

                                       dict(label='Velocity',
                                            method='update',
                                            args=[{'visible': [False] * 7 + [True]},
                                                  {'title': r'$Velocity$',
                                                   'xaxis': {'title': r'$Time [μs]$'},
                                                   'yaxis': {'title': r'$Velocity [m/s]$'},
                                                   'showlegend': True}]

                                            ),
                                       ]),
                                  x=0.9, y=1.1
                              )
                              ])

        if CA.specimen_mode == "shear":
            vectors = [CA.strain.y, CA.time]
            df = transpose(array(vectors))
            filepath = CA.path_folder + "/Exp #" + str(exp_num) + '/Bar Strain.csv'
            savetxt(filepath, df, delimiter=',',
                       header='incident strain, time [s]',
                       fmt='%s')

            vectors = [CA.incid_og.y, CA.incid_og.x]
            df = transpose(array(vectors))
            filepath = CA.path_folder + "/Exp #" + str(exp_num) + '/Raw Signal.csv'
            savetxt(filepath, df, delimiter=',', header='Incident [V], time [s]',
                       fmt='%s')

            vectors = [CA.corr_incid.y,
                       CA.corr_refle.y,
                       CA.time]

            df = transpose(array(vectors))
            filepath = CA.path_folder + "/Exp #" + str(exp_num) + '/Corrected Signals.csv'
            savetxt(filepath, df, delimiter=',',
                       header='Incident [V], Reflected [V], time [s]',
                       fmt='%s')

            vectors = [CA.u_in, CA.time]
            df = transpose(array(vectors))
            filepath = CA.path_folder + "/Exp #" + str(exp_num) + '/Displacement.csv'
            savetxt(filepath, df, delimiter=',', header='u_in [m], time [s]', fmt='%s')

            vectors = [CA.F_in, CA.time]
            df = transpose(array(vectors))
            filepath = CA.path_folder + "/Exp #" + str(exp_num) + '/Forces.csv'
            savetxt(filepath, df, delimiter=',', header='F_in [N], time [s]', fmt='%s')

            vectors = [CA.v_in, CA.time]
            df = transpose(array(vectors))
            filepath = CA.path_folder + "/Exp #" + str(exp_num) + '/Velocity.csv'
            savetxt(filepath, df, delimiter=',', header='v_in [m/s], time [s]', fmt='%s')

            fig = go.FigureWidget(
                [
                    go.Scatter(name=r'$Incident$', y=CA.incid_og.y, x=CA.incid_og.x,
                               mode='lines', visible=False),

                    go.Scatter(name=r'$Incident$', y=CA.corr_incid.y, x=micro_sec,
                               mode='lines', visible=False),
                    go.Scatter(name=r'$Reflected$', y=CA.corr_refle.y, x=micro_sec,
                               mode='lines', visible=False),

                    go.Scatter(name=r'$U_{in}$', y=CA.u_in, x=micro_sec,
                               mode='lines', visible=False),

                    go.Scatter(name=r'$F_{in}$', y=CA.F_in, x=micro_sec,
                               mode='lines', visible=True),

                    go.Scatter(name=r'$V_{in}$', y=CA.v_in, x=micro_sec,
                               mode='lines', visible=False),

                ]
            )

            fig.update_layout(title_x=0.45, template='none',
                              font=dict(family="Times New Roman", size=25),
                              legend=dict(yanchor='top', xanchor='right', y=1.1, x=1,
                                          font=dict(size=30)),
                              margin=dict(l=150, r=500, t=200, b=250),
                              updatemenus=[go.layout.Updatemenu(
                                  active=3,
                                  buttons=list(
                                      [dict(label='Raw Signal',
                                            method='update',
                                            args=[{'visible': [True] + [False] * 5},
                                                  {'title': r'$Raw Signals$',
                                                   'xaxis': {'title': r'$Time [μs]$'},
                                                   'yaxis': {'title': r'$Amplitude [V]$'},
                                                   'showlegend': True}]),

                                       dict(label='Corrected Signals',
                                            method='update',
                                            args=[{'visible': [False] + [True] * 2 + [False] * 3},
                                                  {'title': r'$Corrected Signals$',
                                                   'xaxis': {'title': r'$Time [μs]$'},
                                                   'yaxis': {'title': r'$Amplitude [V]$'},
                                                   'showlegend': True}]),

                                       dict(label='Displacement',
                                            method='update',
                                            args=[{'visible': [False] * 3 + [True] + [False] * 2},
                                                  {'title': r'$Displacement$',
                                                   'xaxis': {'title': r'$Time [μs]$'},
                                                   'yaxis': {'title': r'$Displacement [m]$'},
                                                   'showlegend': True}]),

                                       dict(label='Forces',
                                            method='update',
                                            args=[{'visible': [False] * 4 + [True] + [False]},
                                                  {'title': r'$Force$',
                                                   'xaxis': {'title': r'$Time [μs]$'},
                                                   'yaxis': {'title': r'$Force [N]$'},
                                                   'showlegend': True}]),

                                       dict(label='Velocities',
                                            method='update',
                                            args=[{'visible': [False] * 5 + [True]},
                                                  {'title': r'$Velocity$',
                                                   'xaxis': {'title': r'$Time [μs]$'},
                                                   'yaxis': {'title': r'$Velocity [m/s]$'},
                                                   'showlegend': True}]

                                            ),
                                       ]),
                                  x=0.9, y=1.1
                              )
                              ])
        try:
            fig.add_annotation(dict(font=dict(color='red', size=16),
                                    font_family="Garamound",
                                    x=1,
                                    y=0.1,
                                    showarrow=False,
                                    text="Average Strain Rate: " + str(int(CA.mean_strain_rate)) + " [1/s]",
                                    textangle=0,
                                    xanchor='left',
                                    xref="paper",
                                    yref="paper"))
        except:
            print("Average Strain Rate could not be calcualted")

        fig.add_annotation(dict(font=dict(color='black', size=16),
                                font_family="Garamound",
                                x=1,
                                y=0.37,
                                showarrow=False,
                                font_color='blue',
                                text="<b>Experiment Parameters:<b>                   ",
                                textangle=0,
                                xanchor='left',
                                xref="paper",
                                yref="paper"))

        fig.add_annotation(dict(font=dict(color='black', size=14),
                                font_family="Garamound",
                                x=1,
                                y=0.32,
                                showarrow=False,
                                text="Specimen Diameter: " + str(parameters[0][1]) + " [m]",
                                textangle=0,
                                xanchor='left',
                                xref="paper",
                                yref="paper"))

        fig.add_annotation(dict(font=dict(color='black', size=14),
                                font_family="Garamound",
                                x=1,
                                y=0.29,
                                showarrow=False,
                                text="Specimen Length: " + str(parameters[1][1]) + " [m]",
                                textangle=0,
                                xanchor='left',
                                xref="paper",
                                yref="paper"))

        fig.add_annotation(dict(font=dict(color='black', size=14),
                                font_family="Garamound",
                                x=1,
                                y=0.26,
                                showarrow=False,
                                text="Bar Diameter: " + str(parameters[2][1]) + " [m]",
                                textangle=0,
                                xanchor='left',
                                xref="paper",
                                yref="paper"))

        fig.add_annotation(dict(font=dict(color='black', size=14),
                                font_family="Garamound",
                                x=1,
                                y=0.23,
                                showarrow=False,
                                text="Young's Modulus: " + str(parameters[3][1] / (10 ** 9)) + " [GPa]",
                                textangle=0,
                                xanchor='left',
                                xref="paper",
                                yref="paper"))

        fig.add_annotation(dict(font=dict(color='black', size=14),
                                font_family="Garamound",
                                x=1,
                                y=0.2,
                                showarrow=False,
                                text="Sound Velocity in Bar: " + str(parameters[6][1]) + " [m/s]",
                                textangle=0,
                                xanchor='left',
                                xref="paper",
                                yref="paper"))

        fig.add_annotation(dict(font=dict(color='black', size=14),
                                font_family="Garamound",
                                x=1,
                                y=0.17,
                                showarrow=False,
                                text="Bridge Tension: " + str(parameters[8][1]) + " [V]",
                                textangle=0,
                                xanchor='left',
                                xref="paper",
                                yref="paper"))

        fig.add_annotation(dict(font=dict(color='black', size=14),
                                font_family="Garamound",
                                x=1,
                                y=0.14,
                                showarrow=False,
                                text="Striker Velocity: " + str("%.2f" % CA.mean_striker_velocity) + " [m/s]",
                                textangle=0,
                                xanchor='left',
                                xref="paper",
                                yref="paper"))

        fig.add_annotation(dict(font=dict(color='black', size=18),
                                font_family="Garamound",
                                x=1,
                                y=0.6,
                                showarrow=False,
                                text="<b>Experiment no. " + str(exp_num) + "<b>",
                                textangle=0,
                                xanchor='left',
                                xref="paper",
                                yref="paper"))

        fig.add_annotation(dict(font=dict(color='black', size=14),
                                font_family="Garamound",
                                x=1,
                                y=0.56,
                                showarrow=False,
                                text="Specimen type: " + str(CA.specimen_mode),
                                textangle=0,
                                xanchor='left',
                                xref="paper",
                                yref="paper"))

        fig.add_annotation(dict(font=dict(color='black', size=14),
                                font_family="Garamound",
                                x=1,
                                y=0.54,
                                showarrow=False,
                                text="Experiment mode: " + str(CA.mode),
                                textangle=0,
                                xanchor='left',
                                xref="paper",
                                yref="paper"))

        fig.add_annotation(dict(font=dict(color='black', size=20),
                                font_family="Garamound",
                                x=1,
                                y=0.8,
                                showarrow=False,
                                text="main Analysis Report",
                                textangle=0,
                                xanchor='left',
                                xref="paper",
                                yref="paper"))

        fig.update_layout(margin=dict(r=250))
        fig.write_html(CA.path_folder + "\Exp " + str(exp_num) + '.html',
                       auto_open=CA.auto_open_report,
                       include_mathjax='cdn')

    elif bar_num == 2:
        if CA.specimen_mode == "regular":
            vectors = [CA.incid_og.y, CA.trans_og.y, CA.incid_og.x]
            df = transpose(array(vectors))
            filepath = CA.path_folder + "/Analysis Results" + '/Raw Signals.csv'
            savetxt(filepath, df, delimiter=',', header='Incident [V], Transmitted [V], time [s]',
                       fmt='%s')

            vectors = [CA.corr_incid.y,
                       CA.corr_refle.y,
                       CA.corr_trans.y,
                       CA.time]
            df = transpose(array(vectors))
            filepath = CA.path_folder + "/Analysis Results" + '/Corrected Signals.csv'
            savetxt(filepath, df, delimiter=',',
                       header='Incident [V], Reflected [V], Transmitted [V], time [s]',
                       fmt='%s')

            vectors = [CA.u_in, CA.u_out, CA.time]
            df = transpose(array(vectors))
            filepath = CA.path_folder + "/Analysis Results" + '/Displacements.csv'
            savetxt(filepath, df, delimiter=',', header='u_in [m], u_out [m], time [s]', fmt='%s')

            vectors = [CA.true_stress_strain[0], CA.true_stress_strain[1]]
            df = transpose(array(vectors))
            filepath = CA.path_folder + "/Analysis Results" + '/Stress-Strain True.csv'
            savetxt(filepath, df, delimiter=',', header='Strain, Stress', fmt='%s')

            vectors = [CA.eng_stress_strain[0], CA.eng_stress_strain[1]]
            df = transpose(array(vectors))
            filepath = CA.path_folder + "/Analysis Results" + '/Stress-Strain Engineering.csv'
            savetxt(filepath, df, delimiter=',', header='Strain, Stress', fmt='%s')

            vectors = [CA.F_in, CA.F_out, CA.time]
            df = transpose(array(vectors))
            filepath = CA.path_folder + "/Analysis Results" + '/Forces.csv'
            savetxt(filepath, df, delimiter=',', header='F_in [N], F_out [N], time [s]', fmt='%s')

            vectors = [CA.v_in, CA.v_out, CA.time]
            df = transpose(array(vectors))
            filepath = CA.path_folder + "/Analysis Results" + '/Velocities.csv'
            savetxt(filepath, df, delimiter=',', header='v_in [m/s], v_out [m/s], time [s]', fmt='%s')

            vectors = [CA.plastic_strain, CA.plastic_stress, CA.IR_temperature, CA.plastic_time]
            df = transpose(array(vectors))
            filepath = CA.path_folder + "/Analysis Results" + '/Plastic Strain and Temperature.csv'
            savetxt(filepath, df, delimiter=',', header='strain, stress [GPa], Temperature [K], time[s]',
                       fmt='%s')

            vectors = [CA.plastic_strain, CA.plastic_stress, CA.beta_int]
            df = transpose(array(vectors))
            filepath = CA.path_folder + "/Analysis Results" + '/Plastic Stress - Strain - beta_int.csv'
            savetxt(filepath, df, delimiter=',', header='strain , stress [GPa], beta_int',
                       fmt='%s')

            fig = make_subplots(specs=[[{"secondary_y": True}]])
            fig.add_trace(go.Scatter(name=r'$Incident$', y=CA.incid_og.y, x=CA.incid_og.x,
                                     mode='lines', visible=False), secondary_y=False)
            fig.add_trace(go.Scatter(name=r'$Transmitted$', y=CA.trans_og.y, x=CA.trans_og.x,
                                     mode='lines', visible=False), secondary_y=False)

            fig.add_trace(go.Scatter(name=r'$Incident$', y=CA.corr_incid.y, x=micro_sec,
                                     mode='lines', visible=False), secondary_y=False)
            fig.add_trace(go.Scatter(name=r'$Transmitted$', y=CA.corr_trans.y, x=micro_sec,
                                     mode='lines', visible=False), secondary_y=False)
            fig.add_trace(go.Scatter(name=r'$Reflected$', y=CA.corr_refle.y, x=micro_sec,
                                     mode='lines', visible=False), secondary_y=False)
            fig.add_trace(go.Scatter(name=r'$IR$', y=CA.IR_EXP.y[:len(micro_sec)], x=micro_sec,
                                     mode='lines', visible=False), secondary_y=True)

            fig.add_trace(go.Scatter(name=r'$U_{in}$', y=CA.u_in, x=micro_sec,
                                     mode='lines', visible=False), secondary_y=False)
            fig.add_trace(go.Scatter(name=r'$U_{out}$', y=CA.u_out, x=micro_sec,
                                     mode='lines', visible=False), secondary_y=False)

            fig.add_trace(go.Scatter(name=r'$\sigma$', y=CA.plastic_stress, x=CA.plastic_strain,
                                     mode='lines'), secondary_y=False)
            fig.add_trace(go.Scatter(name=r'$IR$', y=CA.IR_temperature, x=CA.plastic_strain,
                                     mode='lines', visible=False), secondary_y=True)

            fig.add_trace(go.Scatter(name='$F_{in}$', y=CA.F_in, x=micro_sec,
                                     mode='lines', visible=False), secondary_y=False)
            fig.add_trace(go.Scatter(name=r'$F_{out}$', y=CA.F_out, x=micro_sec,
                                     mode='lines', visible=False), secondary_y=False)

            fig.add_trace(go.Scatter(name=r'$V_{in}$', y=CA.v_in, x=micro_sec,
                                     mode='lines', visible=False), secondary_y=False)
            fig.add_trace(go.Scatter(name=r'$V_{out}$', y=CA.v_out, x=micro_sec,
                                     mode='lines', visible=False), secondary_y=False)

            fig.add_trace(go.Scatter(name=r'$\epsilon_{plastic}$', y=CA.plastic_strain, x=micro_sec,
                                     mode='lines', visible=False), secondary_y=False)
            fig.add_trace(go.Scatter(name=r'$IR$', y=CA.IR_temperature, x=micro_sec,
                                     mode='lines', visible=False), secondary_y=True)

            fig.add_trace(go.Scatter(name=r'$\beta_{int}$', y=CA.beta_int, x=CA.plastic_strain,
                                     mode='lines', visible=False), secondary_y=False)

            fig.add_trace(go.Scatter(name=r'$\Delta T = \beta_{int} \cdot W_p \textrm{ (Experiment)}$',
                                     y=CA.IR_temperature, x=CA.Wp,
                                     mode='lines', visible=False), secondary_y=False)

            LR_name = r"$\Delta T = " + str(CA.LR_T_Wp_slope)[:5] + "W_p " + " + " \
                      + str(CA.LR_T_Wp_intercept)[:5] + r"\textrm{ (Linear Regression) ____ }$"
            fig.add_trace(go.Scatter(name=LR_name, y=CA.LR_T_Wp, x=CA.Wp, line=dict(dash='dash'),
                                     mode='lines', visible=False), secondary_y=False)

            fig.update_layout(title_x=0.45, template='none',
                              font=dict(family="Times New Roman", size=25),
                              legend=dict(yanchor='top', xanchor='right', y=1.1, x=1,
                                          font=dict(size=30)),
                              margin=dict(l=150, r=500, t=200, b=250),
                              updatemenus=[go.layout.Updatemenu(
                                  active=3,
                                  buttons=list(
                                      [dict(label='Raw Signals',
                                            method='update',
                                            args=[{'visible': [True] * 2 + [False] * 17},
                                                  {'title': 'Raw Signals',
                                                   'xaxis': {'title': 'Time [μs]'},
                                                   'yaxis': {'title': 'Amplitude [V]'},
                                                   "yaxis2.visible": False,
                                                   'showlegend': True}]),

                                       dict(label='Corrected Signals',
                                            method='update',
                                            args=[{'visible': [False] * 2 + [True] * 4 + [False] * 13},
                                                  {'title': r'Corrected Signals',
                                                   'xaxis': {'title': 'Time [μs]'},
                                                   'yaxis': {'title': 'Amplitude [V]'},
                                                   'yaxis2': {'title': 'Amplitude [V]',
                                                              'color': 'Red',
                                                              'zeroline': False,
                                                              'mirror': True,
                                                              'anchor': 'free',
                                                              'overlaying': 'y',
                                                              'side': 'right',
                                                              'position': 1},
                                                   'showlegend': True}]),

                                       dict(label='Displacements',
                                            method='update',
                                            args=[{'visible': [False] * 6 + [True] * 2 + [False] * 11},
                                                  {'title': 'Displacements',
                                                   'xaxis': {'title': 'Time [μs]'},
                                                   'yaxis': {'title': 'Displacement [m]'},
                                                   "yaxis2.visible": False,
                                                   'showlegend': True}]),

                                       dict(label='Stress - Strain',
                                            method='update',
                                            args=[{'visible': [False] * 8 + [True] * 2 + [False] * 9},
                                                  {
                                                      'title': 'True Stress and Temperature vs. True Plastic Strain',
                                                      'xaxis': {'title': 'Plastic Strain'},
                                                      'yaxis': {'title': 'Stress [MPa]',
                                                                'zeroline': False,
                                                                'mirror': True},

                                                      'yaxis2': {'title': r'${\Delta} T [Celsius]$',
                                                                 'color': 'Orange',
                                                                 'zeroline': False,
                                                                 'mirror': True,
                                                                 'anchor': 'free',
                                                                 'overlaying': 'y',
                                                                 'side': 'right',
                                                                 'position': 1},
                                                      'showlegend': True}]),

                                       dict(label='Forces',
                                            method='update',
                                            args=[{'visible': [False] * 10 + [True] * 2 + [False] * 7},
                                                  {'title': 'Forces',
                                                   'xaxis': {'title': 'Time [μs]'},
                                                   'yaxis': {'title': 'Force [N]'},
                                                   "yaxis2.visible": False,
                                                   'showlegend': True}]),

                                       dict(label='Velocities',
                                            method='update',
                                            args=[{'visible': [False] * 12 + [True] * 2 + [False] * 5},
                                                  {'title': 'Velocities',
                                                   'xaxis': {'title': 'Time [μs]'},
                                                   'yaxis': {'title': 'Velocity [m/s]'},
                                                   "yaxis2.visible": False,
                                                   'showlegend': True}]),

                                       dict(label='Plastic Strain & Temperature',
                                            method='update',
                                            args=[{'visible': [False] * 14 + [True] * 2 + [False] * 3},
                                                  {'title': 'Temperature, Strain vs Time',
                                                   'xaxis': {'title': 'Time [μs]'},
                                                   'yaxis': {'title': 'Plastic Strain'},
                                                   'yaxis2': {'title': r'${\Delta} T [Celsius]$ ',
                                                              'color': 'Orange',
                                                              'zeroline': False,
                                                              'mirror': True,
                                                              'anchor': 'free',
                                                              'overlaying': 'y',
                                                              'side': 'right',
                                                              'position': 1},
                                                   'showlegend': True}]),

                                       dict(label='beta_int',
                                            method='update',
                                            args=[{'visible': [False] * 16 + [True] + [False] * 2},
                                                  {'title': 'Energy Ratio',
                                                   'xaxis': {'title': 'True Plastic Strain'},
                                                   'yaxis': {'title': r'$\beta_{int}$',
                                                             'range': [0, 1]},
                                                   "yaxis2.visible": False,
                                                   'showlegend': False}]),

                                       dict(label='Temperature - Plastic Work',
                                            method='update',
                                            args=[{'visible': [False] * 17 + [True] * 2},
                                                  {'title': 'Energy Ratio',
                                                   'xaxis': {'title': 'Plastic Work [J]'},
                                                   'yaxis': {'title': r'${\Delta} T [Celsius]$'},
                                                   "yaxis2.visible": False,
                                                   'showlegend': True}]),
                                       ]),
                                  x=0.125, y=1.2
                              )
                              ])

        if CA.specimen_mode == "shear":
            vectors = [CA.strain.y, CA.trans.y, CA.time]
            df = transpose(array(vectors))
            filepath = CA.path_folder + "/Analysis Results" + '/Bar Strains.csv'
            savetxt(filepath, df, delimiter=',',
                       header='incident strain, transmitted strain, time [s]',
                       fmt='%s')

            vectors = [CA.incid_og.y, CA.trans_og.y, CA.incid_og.x]
            df = transpose(array(vectors))
            filepath = CA.path_folder + "/Analysis Results" + '/Raw Signals.csv'
            savetxt(filepath, df, delimiter=',', header='Incident [V], Transmitted [V], time [s]',
                       fmt='%s')

            vectors = [CA.corr_incid.y,
                       CA.corr_refle.y,
                       CA.corr_trans.y,
                       CA.time]
            df = transpose(array(vectors))
            filepath = CA.path_folder + "/Analysis Results" + '/Corrected Signals.csv'
            savetxt(filepath, df, delimiter=',',
                       header='Incident [V], Reflected [V], Transmitted [V], time [s]',
                       fmt='%s')

            vectors = [CA.u_in, CA.u_out, CA.time]
            df = transpose(array(vectors))
            filepath = CA.path_folder + "/Analysis Results" + '/Displacements.csv'
            savetxt(filepath, df, delimiter=',', header='u_in [m], u_out [m], time [s]', fmt='%s')

            vectors = [CA.F_in, CA.F_out, CA.time]
            df = transpose(array(vectors))
            filepath = CA.path_folder + "/Analysis Results" + '/Forces.csv'
            savetxt(filepath, df, delimiter=',', header='F_in [N], F_out [N], time [s]', fmt='%s')

            vectors = [CA.v_in, CA.v_out, CA.time]
            df = transpose(array(vectors))
            filepath = CA.path_folder + "/Analysis Results" + '/Velocities.csv'
            savetxt(filepath, df, delimiter=',', header='v_in [m/s], v_out [m/s], time [s]', fmt='%s')

            fig = go.FigureWidget(
                [
                    go.Scatter(name=r'$Incident$', y=CA.incid_og.y, x=CA.incid_og.x,
                               mode='lines', visible=False),
                    go.Scatter(name=r'$Transmitted$', y=CA.trans_og.y, x=CA.trans_og.x,
                               mode='lines', visible=False),

                    go.Scatter(name=r'$Incident$', y=CA.corr_incid.y, x=micro_sec,
                               mode='lines', visible=False),
                    go.Scatter(name=r'$Transmitted$', y=CA.corr_trans.y, x=micro_sec,
                               mode='lines', visible=False),
                    go.Scatter(name=r'$Reflected$', y=CA.corr_refle.y, x=micro_sec,
                               mode='lines', visible=False),
                    go.Scatter(name=r'$IR_{EXP}$', y=CA.IR_EXP.y, x=micro_sec,
                               mode='lines', visible=False),

                    go.Scatter(name=r'$U_{in}$', y=CA.u_in, x=micro_sec,
                               mode='lines', visible=False),
                    go.Scatter(name=r'$U_{out}$', y=CA.u_out, x=micro_sec,
                               mode='lines', visible=False),

                    go.Scatter(name=r'$F_{in}$', y=CA.F_in, x=micro_sec,
                               mode='lines', visible=True),
                    go.Scatter(name=r'$F_{out}$', y=CA.F_out, x=micro_sec,
                               mode='lines', visible=True),

                    go.Scatter(name=r'$V_{in}$', y=CA.v_in, x=micro_sec,
                               mode='lines', visible=False),
                    go.Scatter(name=r'$V_{out}$', y=CA.v_out, x=micro_sec,
                               mode='lines', visible=False),

                ]
            )

            fig.update_layout(title_x=0.5, template='none',
                              font=dict(family="Gravitas One", size=22),
                              legend=dict(yanchor='top', xanchor='right', y=0.99, x=0.99, itemsizing='trace'),
                              updatemenus=[go.layout.Updatemenu(
                                  active=3,
                                  buttons=list(
                                      [dict(label='Raw Signals',
                                            method='update',
                                            args=[{'visible': [True] * 2 + [False] * 10},
                                                  {'title': r'$Raw Signals$',
                                                   'xaxis': {'title': r'$Time [μs]$'},
                                                   'yaxis': {'title': r'$Amplitude [V]$'},
                                                   'showlegend': True}]),

                                       dict(label='Corrected Signals',
                                            method='update',
                                            args=[{'visible': [False] * 2 + [True] * 4 + [False] * 6},
                                                  {'title': r'$Corrected Signals$',
                                                   'xaxis': {'title': r'$Time [μs]$'},
                                                   'yaxis': {'title': r'$Amplitude [V]$'},
                                                   'showlegend': True}]),

                                       dict(label='Displacement',
                                            method='update',
                                            args=[{'visible': [False] * 6 + [True] * 2 + [False] * 4},
                                                  {'title': r'$Displacements$',
                                                   'xaxis': {'title': r'$Time [μs]$'},
                                                   'yaxis': {'title': r'$Displacement [m]$'},
                                                   'showlegend': True}]),

                                       dict(label='Forces',
                                            method='update',
                                            args=[{'visible': [False] * 8 + [True] * 2 + [False] * 2},
                                                  {'title': r'$Forces$',
                                                   'xaxis': {'title': r'$Time [μs]$'},
                                                   'yaxis': {'title': r'$Force [N]$'},
                                                   'showlegend': True}]),

                                       dict(label='Velocities',
                                            method='update',
                                            args=[{'visible': [False] * 10 + [True] * 2},
                                                  {'title': r'$Velocities$',
                                                   'xaxis': {'title': r'$Time [μs]$'},
                                                   'yaxis': {'title': r'$Velocity [m/s]$'},
                                                   'showlegend': True}]

                                            ),
                                       ]),
                                  x=0.9, y=1.1
                              )
                              ])
        beta_str = "β = " + str(CA.LR_T_Wp_slope * CA.density * CA.heat_capacity)
        fig.add_annotation(dict(font=dict(color='black', size=30),
                                font_family="Garamound",
                                x=0,
                                y=1.1,
                                showarrow=False,
                                text=beta_str,
                                textangle=0,
                                xanchor='left',
                                xref="paper",
                                yref="paper",
                                bordercolor="#c7c7c7",
                                borderwidth=2,
                                borderpad=4,
                                bgcolor="#ff7f0e",
                                opacity=0.8
                                ))

        fig.write_html(CA.path_folder + "/Analysis Results" + '.html',
                       auto_open=CA.auto_open_report,
                       include_mathjax='cdn')
        f_path = CA.path_folder + "\Analysis Results" + "\Parameters.txt"

    if os.path.isfile(f_path):
        os.remove(f_path)

    f = open(f_path, 'x')
    f = open(f_path, 'r+')
    f.truncate(0)
    s = ""

    s += str(parameters[0][0]) + ": " + str(parameters[0][1]) + " [m]" + "\n"
    s += str(parameters[1][0]) + ": " + str(parameters[1][1]) + " [m]" + "\n"
    s += str(parameters[2][0]) + ": " + str(parameters[2][1]) + " [m]" + "\n"
    s += str(parameters[3][0]) + ": " + str(parameters[3][1] / (10 ** 9)) + " [GPa]" + "\n"
    s += str(parameters[4][0]) + ": " + str(parameters[4][1]) + " [m]" + "\n"
    s += str(parameters[5][0]) + ": " + str(parameters[5][1]) + " [m]" + "\n"
    s += str(parameters[6][0]) + ": " + str(parameters[6][1]) + " [m/s]" + "\n"
    s += str(parameters[7][0]) + ": " + str(parameters[7][1]) + "\n"
    s += str(parameters[8][0]) + ": " + str(parameters[8][1]) + " [V]" + "\n"
    s += "Spacing: " + str(CA.spacing) + " Points" + "\n"
    s += "Prominence: " + str(CA.prominence_percent * 100) + "%" + "\n"
    s += "Curve Smoothing Parameter: " + str(CA.smooth_value * 100) + "\n"
    s += "Average Strain Rate: " + str(CA.mean_strain_rate) + "[1/s]"
    s += "\n"  # For some reason, there is a problem without a new line at the end of the defaults file.
    f.write(s)
    f.close()

