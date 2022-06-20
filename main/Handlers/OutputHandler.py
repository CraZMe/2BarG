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


def make_report(CA, exp_num, parameters, bar_num):
    micro_sec = [t * 1e6 for t in CA.time]

    if bar_num == 1:

        plots = [
            go.Scatter(name=r'$Incident$', y=CA.incid_og.y, x=CA.incid_og.x,
                       mode='lines', visible=False),

            go.Scatter(name=r'$Incident$', y=CA.corr_incid.y, x=micro_sec,
                       mode='lines', visible=False),
            go.Scatter(name=r'$Reflected$', y=CA.corr_refle.y, x=micro_sec,
                       mode='lines', visible=False),

            go.Scatter(name=r'$U_{in}$', y=CA.u_in, x=micro_sec,
                       mode='lines', visible=False),

            go.Scatter(name=r'$V_{in}$', y=CA.v_in, x=micro_sec,
                       mode='lines', visible=False),

            go.Scatter(name=r'$F_{in}$', y=CA.F_in, x=micro_sec,
                       mode='lines', visible=True),

            go.Scatter(name=r'$\sigma_{Engineering}$', y=CA.eng_stress_strain[1],
                       x=CA.eng_stress_strain[0], mode='lines'),

            go.Scatter(name=r'$True$', y=CA.true_stress_strain[1],
                       x=CA.true_stress_strain[0], mode='lines')
        ]
        buttons = [
            dict(label='Raw Signal',
                 method='update',
                 args=[{'visible': [True] + [False] * 7},
                       {'xaxis': {'title': 'Time [μs]'},
                        'yaxis': {'title': 'Amplitude [V]'},
                        'showlegend': True}]),

            dict(label='Corrected Signals',
                 method='update',
                 args=[{'visible': [False] + [True] * 2 + [False] * 5},
                       {'xaxis': {'title': 'Time [μs]'},
                        'yaxis': {'title': 'Amplitude [V]'},
                        'showlegend': True}]),

            dict(label='Displacement',
                 method='update',
                 args=[{'visible': [False] * 3 + [True] + [False] * 4},
                       {'xaxis': {'title': 'Time [μs]'},
                        'yaxis': {'title': 'Displacement [m]'},
                        'showlegend': True}]),

            dict(label='Forces',
                 method='update',
                 args=[{'visible': [False] * 4 + [True] + [False] * 3},
                       {'xaxis': {'title': 'Time [μs]'},
                        'yaxis': {'title': 'Force [N]'},
                        'showlegend': True}]),

            dict(label='Velocities',
                 method='update',
                 args=[{'visible': [False] * 5 + [True] + [False] * 2},
                       {'xaxis': {'title': 'Time [μs]'},
                        'yaxis': {'title': 'Velocity [m/s]'},
                        'showlegend': True}]),

            dict(label='Stress - Strain',
                 method='update',
                 args=[{'visible': [False] * 6 + [True] * 2},
                       {'xaxis': {'title': 'Strain'},
                        'yaxis': {'title': 'Stress [MPa]'},
                        'showlegend': True}]),
        ]

        fig = go.FigureWidget(plots)

        fig.write_html(CA.path_folder + r"\Exp " + str(exp_num) + '.html',
                       auto_open=CA.auto_open_report,
                       include_mathjax='cdn')

    elif bar_num == 2:
        fig = make_subplots()
        fig.add_trace(go.Scatter(name=r'$\large{Incident}$', y=CA.incid_og.y, x=CA.incid_og.x,
                                 mode='lines', visible=False))
        fig.add_trace(go.Scatter(name=r'$\large{Transmitted}..$', y=CA.trans_og.y, x=CA.trans_og.x,
                                 mode='lines', visible=False))

        fig.add_trace(go.Scatter(name=r'$\large{Incident}$', y=CA.corr_incid.y, x=micro_sec,
                                 mode='lines', visible=False))
        fig.add_trace(go.Scatter(name=r'$\large{Transmitted}..$', y=CA.corr_trans.y, x=micro_sec,
                                 mode='lines', visible=False))
        fig.add_trace(go.Scatter(name=r'$\large{Reflected}$', y=CA.corr_refle.y, x=micro_sec,
                                 mode='lines', visible=False))

        fig.add_trace(go.Scatter(name=r'$\large{U_{in}}$', y=CA.u_in, x=micro_sec,
                                 mode='lines', visible=False))
        fig.add_trace(go.Scatter(name=r'$\large{U_{out}}$', y=CA.u_out, x=micro_sec,
                                 mode='lines', visible=False))

        fig.add_trace(go.Scatter(name=r'$\large{\sigma_{Engineering}}$', y=CA.eng_stress_strain[1],
                                 x=CA.eng_stress_strain[0], mode='lines'))
        fig.add_trace(go.Scatter(name=r'$\large{\sigma_{True}}$', y=CA.true_stress_strain[1],
                                 x=CA.true_stress_strain[0], mode='lines'))

        fig.add_trace(go.Scatter(name=r'$\large{F_{in}}$', y=CA.F_in, x=micro_sec,
                                 mode='lines', visible=False))
        fig.add_trace(go.Scatter(name=r'$\large{F_{out}}$', y=CA.F_out, x=micro_sec,
                                 mode='lines', visible=False))

        fig.add_trace(go.Scatter(name=r'$\large{V_{in}}$', y=CA.v_in, x=micro_sec,
                                 mode='lines', visible=False))
        fig.add_trace(go.Scatter(name=r'$\large{V_{out}}$', y=CA.v_out, x=micro_sec,
                                 mode='lines', visible=False))

        buttons = list([dict(label='Raw Signals',
                  method='update',
                  args=[{'visible': [True, True] + [False] * 11},
                        {'xaxis': {'title': r'Time [μs]'},
                         'yaxis': {'title': r'Amplitude [V]'},
                         'showlegend': True}]),

             dict(label='Corrected Signals',
                  method='update',
                  args=[{'visible': [False] * 2 + [True] * 3 + [False] * 8},
                        {'xaxis': {'title': r'Time [μs]'},
                         'yaxis': {'title': r'Amplitude [V]'},
                         'showlegend': True}]),

             dict(label='Displacements',
                  method='update',
                  args=[{'visible': [False] * 5 + [True] * 2 + [False] * 6},
                        {'xaxis': {'title': r'Time [μs]'},
                         'yaxis': {'title': r'Displacement [m]'},
                         'showlegend': True}]),

             dict(label='Stress - Strain',
                  method='update',
                  args=[{'visible': [False] * 7 + [True] * 2 + [False] * 4},
                        {'xaxis': {'title': r'Strain$'},
                         'yaxis': {'title': 'Stress [MPa]'},
                         'showlegend': True}]),

             dict(label='Forces',
                  method='update',
                  args=[{'visible': [False] * 9 + [True] * 2 + [False] * 2},
                        {'xaxis': {'title': r'Time [μs]'},
                         'yaxis': {'title': r'Force [N]'},
                         'showlegend': True}]),

             dict(label='Velocities',
                  method='update',
                  args=[{'visible': [False] * 11 + [True] * 2},
                        {'xaxis': {'title': r'Time [μs]'},
                         'yaxis': {'title': r'Velocity [m/s]'},
                         'showlegend': True}]

                  ),
             ])

    fig.update_layout(title_x=0.5, template='none',
                      font=dict(family="Overpass", size=20),
                      legend=dict(yanchor='top', xanchor='right', y=1.2, x=1, font=dict(size=30)),
                      margin=dict(l=300, r=500, t=200, b=200),
                      updatemenus=[dict(active=3, buttons=buttons, xanchor='left', x=0, y=1.2)]
                      )

    try:
        fig.add_annotation(dict(font=dict(color='red', size=20),
                                font_family="Overpass",
                                x=1.02,
                                y=0.8,
                                showarrow=False,
                                text=r"$\large{\dot{\bar{\varepsilon}} = " + str(int(CA.mean_strain_rate)) + " [1/s]}$",
                                textangle=0,
                                xanchor='left',
                                xref="paper",
                                yref="paper"))
    except:
        print("Mean Strain Rate could not be calcualted")

    fig.add_annotation(dict(font=dict(color='black', size=22),
                            font_family="Overpass",
                            x=1.02,
                            y=0.7,
                            showarrow=False,
                            text="<b>Experiment Parameters:<b>",
                            textangle=0,
                            xanchor='left',
                            xref="paper",
                            yref="paper"))

    fig.add_annotation(dict(font=dict(color='black', size=18),
                            font_family="Overpass",
                            x=1.02,
                            y=0.6,
                            showarrow=False,
                            text=r"$\large{d_{specimen} = " + str(round(parameters[0][1]*1e6) * 1000 / 1e6) + " [mm]}$",
                            textangle=0,
                            xanchor='left',
                            xref="paper",
                            yref="paper"))

    fig.add_annotation(dict(font=dict(color='black', size=18),
                            font_family="Overpass",
                            x=1.02,
                            y=0.5,
                            showarrow=False,
                            text=r"$\large{\ell_{specimen} = " + str(round(parameters[1][1]*1e6) * 1000 / 1e6) + " [mm]}$",
                            textangle=0,
                            xanchor='left',
                            xref="paper",
                            yref="paper"))

    fig.add_annotation(dict(font=dict(color='black', size=18),
                            font_family="Overpass",
                            x=1.02,
                            y=0.4,
                            showarrow=False,
                            text=r"$\large{d_{bar} = " + str(round(parameters[2][1]*1e6) * 1000 / 1e6) + " [mm]}$",
                            textangle=0,
                            xanchor='left',
                            xref="paper",
                            yref="paper"))

    fig.add_annotation(dict(font=dict(color='black', size=18),
                            font_family="Overpass",
                            x=1.02,
                            y=0.3,
                            showarrow=False,
                            text=r"$\large{E = " + str(parameters[3][1] / (10 ** 9)) + " [GPa]}$",
                            textangle=0,
                            xanchor='left',
                            xref="paper",
                            yref="paper"))

    fig.add_annotation(dict(font=dict(color='black', size=18),
                            font_family="Overpass",
                            x=1.02,
                            y=0.2,
                            showarrow=False,
                            text=r"$\large{c_0 = " + str(parameters[6][1]) + " [m/s]}$",
                            textangle=0,
                            xanchor='left',
                            xref="paper",
                            yref="paper"))

    fig.add_annotation(dict(font=dict(color='black', size=18),
                            font_family="Overpass",
                            x=1.02,
                            y=0.1,
                            showarrow=False,
                            text=r"$\large{V_{bridge} = " + str(parameters[8][1]) + " [V]}$",
                            textangle=0,
                            xanchor='left',
                            xref="paper",
                            yref="paper"))

    fig.add_annotation(dict(font=dict(color='black', size=18),
                            font_family="Overpass",
                            x=1.02,
                            y=0,
                            showarrow=False,
                            text=r"$\large{\bar{V}_{striker} = " + str("%.2f" % CA.mean_striker_velocity) + " [m/s]}$",
                            textangle=0,
                            xanchor='left',
                            xref="paper",
                            yref="paper"))

    fig.add_annotation(dict(font=dict(color='black', size=20),
                            font_family="Overpass",
                            x=1.02,
                            y=0.85,
                            showarrow=False,
                            text=r"$\large{" + str(CA.specimen_mode) + "}$",
                            textangle=0,
                            xanchor='left',
                            xref="paper",
                            yref="paper"))

    fig.add_annotation(dict(font=dict(color='black', size=20),
                            font_family="Overpass",
                            x=1.02,
                            y=0.9,
                            showarrow=False,
                            text=r"$\large{" + str(CA.mode) + "}$",
                            textangle=0,
                            xanchor='left',
                            xref="paper",
                            yref="paper"))

    fig.add_annotation(dict(font=dict(color='black', size=30),
                            font_family="Overpass",
                            x=1.02,
                            y=1,
                            showarrow=False,
                            text="<b>2BarG Analysis Report<b>",
                            textangle=0,
                            xanchor='left',
                            xref="paper",
                            yref="paper"))

    fig.write_html(CA.path_folder + "/Exp " + str(exp_num) + '.html',
                   auto_open=CA.auto_open_report,
                   include_mathjax='cdn')


def make_report_thermal(CA, exp_num, parameters, bar_num):
    micro_sec = [t * 1e6 for t in CA.time]

    if bar_num == 1:

        plots = [
                    go.Scatter(name=r'$Incident$', y=CA.incid_og.y, x=CA.incid_og.x,
                               mode='lines', visible=False),

                    go.Scatter(name=r'$Incident$', y=CA.corr_incid.y, x=micro_sec,
                               mode='lines', visible=False),
                    go.Scatter(name=r'$Reflected$', y=CA.corr_refle.y, x=micro_sec,
                               mode='lines', visible=False),

                    go.Scatter(name=r'$U_{in}$', y=CA.u_in, x=micro_sec,
                               mode='lines', visible=False),

                    go.Scatter(name=r'$V_{in}$', y=CA.v_in, x=micro_sec,
                               mode='lines', visible=False),

                    go.Scatter(name=r'$F_{in}$', y=CA.F_in, x=micro_sec,
                               mode='lines', visible=True),

                    go.Scatter(name=r'$\sigma_{Engineering}$', y=CA.eng_stress_strain[1],
                               x=CA.eng_stress_strain[0], mode='lines'),

                    go.Scatter(name=r'$True$', y=CA.true_stress_strain[1],
                               x=CA.true_stress_strain[0], mode='lines')
                ]
        buttons = [
            dict(label='Raw Signal',
                 method='update',
                 args=[{'visible': [True] + [False] * 7},
                       {'xaxis': {'title': 'Time [μs]'},
                        'yaxis': {'title': 'Amplitude [V]'},
                        'showlegend': True}]),

            dict(label='Corrected Signals',
                 method='update',
                 args=[{'visible': [False] + [True] * 2 + [False] * 5},
                       {'xaxis': {'title': 'Time [μs]'},
                        'yaxis': {'title': 'Amplitude [V]'},
                        'showlegend': True}]),

            dict(label='Displacement',
                 method='update',
                 args=[{'visible': [False] * 3 + [True] + [False] * 4},
                       {'xaxis': {'title': 'Time [μs]'},
                        'yaxis': {'title': 'Displacement [m]'},
                        'showlegend': True}]),

            dict(label='Forces',
                 method='update',
                 args=[{'visible': [False] * 4 + [True] + [False] * 3},
                       {'xaxis': {'title': 'Time [μs]'},
                        'yaxis': {'title': 'Force [N]'},
                        'showlegend': True}]),

            dict(label='Velocities',
                 method='update',
                 args=[{'visible': [False] * 5 + [True] + [False] * 2},
                       {'xaxis': {'title': 'Time [μs]'},
                        'yaxis': {'title': 'Velocity [m/s]'},
                        'showlegend': True}]),

            dict(label='Stress - Strain',
                 method='update',
                 args=[{'visible': [False] * 6 + [True] * 2},
                       {'xaxis': {'title': 'Strain'},
                        'yaxis': {'title': 'Stress [MPa]'},
                        'showlegend': True}]),
        ]

        fig = go.FigureWidget(plots)

        fig.update_layout(title_x=0.5, template='none',
                          font=dict(family="Overpass", size=20),
                          legend=dict(yanchor='top', xanchor='right', y=1.2, x=1, font=dict(size=30)),
                          margin=dict(l=300, r=300, t=200, b=200),
                          updatemenus=[dict(active=3, buttons=buttons, xanchor='left', x=0, y=1.2)]
                          )

        fig.write_html(CA.path_folder + r"\Exp " + str(exp_num) + '.html',
                       auto_open=CA.auto_open_report,
                       include_mathjax='cdn')

    elif bar_num == 2:

        fig = make_subplots(specs=[[{"secondary_y": True}]])

        fig.add_trace(go.Scatter(name=r'$\Large{Incident}$', y=CA.incid_og.y, x=CA.incid_og.x,
                                 mode='lines', visible=False), secondary_y=False)
        fig.add_trace(go.Scatter(name=r'$\Large{Transmitted}..$', y=CA.trans_og.y, x=CA.trans_og.x,
                                 mode='lines', visible=False), secondary_y=False)

        fig.add_trace(go.Scatter(name=r'$\Large{Incident}$', y=CA.corr_incid.y, x=micro_sec,
                                 mode='lines', visible=False), secondary_y=False)
        fig.add_trace(go.Scatter(name=r'$\Large{Transmitted}..$', y=CA.corr_trans.y, x=micro_sec,
                                 mode='lines', visible=False), secondary_y=False)
        fig.add_trace(go.Scatter(name=r'$\Large{Reflected}$', y=CA.corr_refle.y, x=micro_sec,
                                 mode='lines', visible=False), secondary_y=False)
        fig.add_trace(go.Scatter(name=r'$\Large{IR}$', y=CA.IR_EXP.y[:len(micro_sec)], x=micro_sec,
                                 mode='lines', visible=False), secondary_y=True)

        fig.add_trace(go.Scatter(name=r'$\Large{U_{in}}$', y=CA.u_in, x=micro_sec,
                                 mode='lines', visible=False), secondary_y=False)
        fig.add_trace(go.Scatter(name=r'$\Large{U_{out}}$', y=CA.u_out, x=micro_sec,
                                 mode='lines', visible=False), secondary_y=False)

        fig.add_trace(go.Scatter(name=r'$\Large{\sigma}$', y=CA.plastic_stress, x=CA.plastic_strain,
                                 mode='lines'), secondary_y=False)
        fig.add_trace(go.Scatter(name=r'$\Large{IR}$', y=CA.IR_temperature, x=CA.plastic_strain,
                                 mode='lines', visible=False), secondary_y=True)

        fig.add_trace(go.Scatter(name=r'$\Large{F_{in}}$', y=CA.F_in, x=micro_sec,
                                 mode='lines', visible=False), secondary_y=False)
        fig.add_trace(go.Scatter(name=r'$\Large{F_{out}}$', y=CA.F_out, x=micro_sec,
                                 mode='lines', visible=False), secondary_y=False)

        fig.add_trace(go.Scatter(name=r'$\Large{V_{in}}$', y=CA.v_in, x=micro_sec,
                                 mode='lines', visible=False), secondary_y=False)
        fig.add_trace(go.Scatter(name=r'$\Large{V_{out}}$', y=CA.v_out, x=micro_sec,
                                 mode='lines', visible=False), secondary_y=False)

        fig.add_trace(go.Scatter(name=r'$\Large{\epsilon_{plastic}}..$', y=CA.plastic_strain, x=micro_sec,
                                 mode='lines', visible=False), secondary_y=False)
        fig.add_trace(go.Scatter(name=r'$\Large{IR}$', y=CA.IR_temperature, x=micro_sec,
                                 mode='lines', visible=False), secondary_y=True)

        fig.add_trace(go.Scatter(name=r'$\Large{\beta_{int}}$', y=CA.beta_int, x=CA.plastic_strain,
                                 mode='lines', visible=False), secondary_y=False)

        fig.add_trace(go.Scatter(name=r'$\Large{\Delta T = \beta_{int} \cdot W_p \textrm{(Experiment)}}$',
                                 y=CA.IR_temperature, x=CA.Wp,
                                 mode='lines', visible=False), secondary_y=False)

        LR_name = r"$\Large{\Delta T = " + str(CA.LR_T_Wp_slope * (10 ** 6))[:5] \
                  + r"\cdot 10^{-6} \cdot W_p " + " + " \
                  + str(CA.LR_T_Wp_intercept)[:5] \
                  + r"\textrm{ (Linear Regression) ____.}}$"

        fig.add_trace(go.Scatter(name=LR_name, y=CA.LR_T_Wp, x=CA.Wp, line=dict(dash='dash'),
                                 mode='lines', visible=False), secondary_y=False)

        buttons = list([dict(label='Raw Signals',
                            method='update',
                            args=[{'visible': [True] * 2 + [False] * 17},
                                  {'xaxis': {'title': 'Time [μs]'},
                                   'yaxis': {'title': 'Amplitude [V]'},
                                   "yaxis2.visible": False,
                                   'showlegend': True}]),

                       dict(label='Corrected Signals',
                            method='update',
                            args=[{'visible': [False] * 2 + [True] * 4 + [False] * 13},
                                  {'xaxis': {'title': 'Time [μs]'},
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
                                  {'xaxis': {'title': 'Time [μs]'},
                                   'yaxis': {'title': 'Displacement [m]'},
                                   "yaxis2.visible": False,
                                   'showlegend': True}]),

                       dict(label='Stress - Strain',
                            method='update',
                            args=[{'visible': [False] * 8 + [True] * 2 + [False] * 9},
                                  {'xaxis': {'title': 'Plastic Strain'},
                                  'yaxis': {'title': 'Stress [MPa]',
                                            'zeroline': False,
                                            'mirror': True},

                                  'yaxis2': {'title': r'$\Large{{\Delta} T [Celsius]}$',
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
                                  {'xaxis': {'title': 'Time [μs]'},
                                   'yaxis': {'title': 'Force [N]'},
                                   "yaxis2.visible": False,
                                   'showlegend': True}]),

                       dict(label='Velocities',
                            method='update',
                            args=[{'visible': [False] * 12 + [True] * 2 + [False] * 5},
                                  {'xaxis': {'title': 'Time [μs]'},
                                   'yaxis': {'title': 'Velocity [m/s]'},
                                   "yaxis2.visible": False,
                                   'showlegend': True}]),

                       dict(label='Plastic Strain & Temperature',
                            method='update',
                            args=[{'visible': [False] * 14 + [True] * 2 + [False] * 3},
                                  {'xaxis': {'title': 'Time [μs]'},
                                   'yaxis': {'title': 'Plastic Strain'},
                                   'yaxis2': {'title': r'$\Large{{\Delta} T [Celsius]}$',
                                              'color': 'Orange',
                                              'zeroline': False,
                                              'mirror': True,
                                              'anchor': 'free',
                                              'overlaying': 'y',
                                              'side': 'right',
                                              'position': 1},
                                   'showlegend': True}]),

                       dict(label='Energy Ratio',
                            method='update',
                            args=[{'visible': [False] * 16 + [True] + [False] * 2},
                                  {'xaxis': {'title': 'True Plastic Strain'},
                                   'yaxis': {'title': r'$\Large{\beta_{int}}$',
                                             'range': [0, 1]},
                                   "yaxis2.visible": False,
                                   'showlegend': False}]),

                       dict(label='Temperature - Plastic Work',
                            method='update',
                            args=[{'visible': [False] * 17 + [True] * 2},
                                  {'xaxis': {'title': 'Plastic Work [J]'},
                                   'yaxis': {'title': r'$\Large{{\Delta} T [Celsius]}$'},
                                   "yaxis2.visible": False,
                                   'showlegend': True}]),

                       ])

        fig.update_layout(title_x=0.5, template='none',
                          font=dict(family="Overpass", size=20),
                          legend=dict(yanchor='top', xanchor='right', y=1.2, x=1, font=dict(size=30)),
                          margin=dict(l=300, r=600, t=200, b=200),
                          updatemenus=[dict(active=3, buttons=buttons, xanchor='left', x=0, y=1.2)]
                          )

        beta_str = r"$\Large{\bar\beta_{int} = " + str(CA.LR_T_Wp_slope * CA.density * CA.heat_capacity)[:6] + r"}$"
        fig.add_annotation(dict(font=dict(color="#ff7f0e", size=30),
                                font_family="Overpass",
                                x=0,
                                y=1.1,
                                showarrow=False,
                                text=beta_str,
                                textangle=0,
                                xanchor='left',
                                xref="paper",
                                yref="paper",
                                opacity=0.8
                                ))
        try:
            fig.add_annotation(dict(font=dict(color='red', size=20),
                                    font_family="Overpass",
                                    x=1.15,
                                    y=0.8,
                                    showarrow=False,
                                    text=r"$\large{\dot{\bar{\varepsilon}} = " + str(
                                        int(CA.mean_strain_rate)) + " [1/s]}$",
                                    textangle=0,
                                    xanchor='left',
                                    xref="paper",
                                    yref="paper"))
        except:
            print("Mean Strain Rate could not be calcualted")

        fig.add_annotation(dict(font=dict(color='black', size=22),
                                font_family="Overpass",
                                x=1.15,
                                y=0.7,
                                showarrow=False,
                                text="<b>Experiment Parameters:<b>",
                                textangle=0,
                                xanchor='left',
                                xref="paper",
                                yref="paper"))

        fig.add_annotation(dict(font=dict(color='black', size=18),
                                font_family="Overpass",
                                x=1.15,
                                y=0.6,
                                showarrow=False,
                                text=r"$\large{d_{specimen} = " + str(round(parameters[0][1] * 1e6) * 1000 / 1e6) + " [mm]}$",
                                textangle=0,
                                xanchor='left',
                                xref="paper",
                                yref="paper"))
        specimen_len_text = r"$\large{\ell_{specimen} = " + str(round(parameters[1][1] * 1e6) * 1000 / 1e6) + " [mm]}$"
        fig.add_annotation(dict(font=dict(color='black', size=18),
                                font_family="Overpass",
                                x=1.15,
                                y=0.5,
                                showarrow=False,
                                text=specimen_len_text,
                                textangle=0,
                                xanchor='left',
                                xref="paper",
                                yref="paper"))

        fig.add_annotation(dict(font=dict(color='black', size=18),
                                font_family="Overpass",
                                x=1.15,
                                y=0.4,
                                showarrow=False,
                                text=r"$\large{d_{bar} = " + str(round(parameters[2][1] * 1e6) * 1000 / 1e6) + " [mm]}$",
                                textangle=0,
                                xanchor='left',
                                xref="paper",
                                yref="paper"))

        fig.add_annotation(dict(font=dict(color='black', size=18),
                                font_family="Overpass",
                                x=1.15,
                                y=0.3,
                                showarrow=False,
                                text=r"$\large{E = " + str(parameters[3][1] / (10 ** 9)) + " [GPa]}$",
                                textangle=0,
                                xanchor='left',
                                xref="paper",
                                yref="paper"))

        fig.add_annotation(dict(font=dict(color='black', size=18),
                                font_family="Overpass",
                                x=1.15,
                                y=0.2,
                                showarrow=False,
                                text=r"$\large{c_0 = " + str(parameters[6][1]) + " [m/s]}$",
                                textangle=0,
                                xanchor='left',
                                xref="paper",
                                yref="paper"))

        fig.add_annotation(dict(font=dict(color='black', size=18),
                                font_family="Overpass",
                                x=1.15,
                                y=0.1,
                                showarrow=False,
                                text=r"$\large{V_{bridge} = " + str(parameters[8][1]) + " [V]}$",
                                textangle=0,
                                xanchor='left',
                                xref="paper",
                                yref="paper"))

        fig.add_annotation(dict(font=dict(color='black', size=18),
                                font_family="Overpass",
                                x=1.15,
                                y=0,
                                showarrow=False,
                                text=r"$\large{\bar{V}_{striker} = " + str(
                                    "%.2f" % CA.mean_striker_velocity) + " [m/s]}$",
                                textangle=0,
                                xanchor='left',
                                xref="paper",
                                yref="paper"))

        fig.add_annotation(dict(font=dict(color='black', size=20),
                                font_family="Overpass",
                                x=1.15,
                                y=0.85,
                                showarrow=False,
                                text=r"$\large{" + str(CA.specimen_mode) + "}$",
                                textangle=0,
                                xanchor='left',
                                xref="paper",
                                yref="paper"))

        fig.add_annotation(dict(font=dict(color='black', size=20),
                                font_family="Overpass",
                                x=1.15,
                                y=0.9,
                                showarrow=False,
                                text=r"$\large{" + str(CA.mode) + "}$",
                                textangle=0,
                                xanchor='left',
                                xref="paper",
                                yref="paper"))

        fig.add_annotation(dict(font=dict(color='black', size=30),
                                font_family="Overpass",
                                x=1.15,
                                y=1,
                                showarrow=False,
                                text="<b>2BarG Analysis Report<b>",
                                textangle=0,
                                xanchor='left',
                                xref="paper",
                                yref="paper"))
        fig.write_html(CA.path_folder + "/Analysis Results.html",
                       auto_open=CA.auto_open_report,
                       include_mathjax='cdn')


def save_data(CA, exp_num, parameters, bar_num):
    if CA.thermal_analysis:
        desired_path = CA.path_folder + "/Analysis Results"
        if not os.path.isdir(desired_path):
            os.makedirs(CA.path_folder + "/Analysis Results")
    else:
        desired_path = CA.path_folder + "/Exp #" + str(exp_num)

    if bar_num == 1:
        vectors = [CA.incid_og.y, CA.incid_og.x]
        df = transpose(array(vectors))
        filepath = desired_path + '/Raw Signal.csv'
        savetxt(filepath, df, delimiter=',', header='Incident [V], time [s]', fmt='%s')

        vectors = [CA.corr_incid.y, CA.corr_refle.y, CA.time]
        df = transpose(array(vectors))
        filepath = desired_path + '/Corrected Signals.csv'
        savetxt(filepath, df, delimiter=',', header='Incident [V], Reflected [V], time [s]', fmt='%s')

        vectors = [CA.u_in, CA.time]
        df = transpose(array(vectors))
        filepath = desired_path + '/Displacement.csv'
        savetxt(filepath, df, delimiter=',', header='u_in [m], time [s]', fmt='%s')

        vectors = [CA.true_stress_strain[0], CA.true_stress_strain[1]]
        df = transpose(array(vectors))
        filepath = desired_path + '/Stress-Strain True.csv'
        savetxt(filepath, df, delimiter=',', header='Strain, Stress', fmt='%s')

        vectors = [CA.eng_stress_strain[0], CA.eng_stress_strain[1]]
        df = transpose(array(vectors))
        filepath = desired_path + '/Stress-Strain Engineering.csv'
        savetxt(filepath, df, delimiter=',', header='Strain, Stress', fmt='%s')

        vectors = [CA.F_in, CA.time]
        df = transpose(array(vectors))
        filepath = desired_path + '/Force.csv'
        savetxt(filepath, df, delimiter=',', header='F_in [N], time [s]', fmt='%s')

        vectors = [CA.v_in, CA.time]
        df = transpose(array(vectors))
        filepath = desired_path + '/Velocity.csv'
        savetxt(filepath, df, delimiter=',', header='v_in [m/s], time [s]', fmt='%s')

        if CA.specimen_mode == "shear":
            vectors = [CA.strain.y, CA.time]
            df = transpose(array(vectors))
            filepath = desired_path + '/Bar Strain.csv'
            savetxt(filepath, df, delimiter=',', header='incident strain, time [s]', fmt='%s')

    if bar_num == 2:
        vectors = [CA.incid_og.y, CA.trans_og.y, CA.incid_og.x]
        df = transpose(array(vectors))
        filepath = desired_path + '/Raw Signals.csv'
        savetxt(filepath, df, delimiter=',', header='Incident [V], Transmitted [V], time [s]', fmt='%s')

        vectors = [CA.corr_incid.y, CA.corr_refle.y, CA.corr_trans.y, CA.time]
        df = transpose(array(vectors))
        filepath = desired_path + '/Corrected Signals.csv'
        savetxt(filepath, df, delimiter=',', header='Incident [V], Reflected [V], Transmitted [V], time [s]', fmt='%s')

        vectors = [CA.u_in, CA.u_out, CA.time]
        df = transpose(array(vectors))
        filepath = desired_path + '/Displacements.csv'
        savetxt(filepath, df, delimiter=',', header='u_in [m], u_out [m], time [s]', fmt='%s')

        vectors = [CA.true_stress_strain[0], CA.true_stress_strain[1]]
        df = transpose(array(vectors))
        filepath = desired_path + '/Stress-Strain True.csv'
        savetxt(filepath, df, delimiter=',', header='Strain, Stress', fmt='%s')

        vectors = [CA.eng_stress_strain[0], CA.eng_stress_strain[1]]
        df = transpose(array(vectors))
        filepath = desired_path + '/Stress-Strain Engineering.csv'
        savetxt(filepath, df, delimiter=',', header='Strain, Stress', fmt='%s')

        vectors = [CA.F_in, CA.F_out, CA.time]
        df = transpose(array(vectors))
        filepath = desired_path + '/Forces.csv'
        savetxt(filepath, df, delimiter=',', header='F_in [N], F_out [N], time [s]', fmt='%s')

        vectors = [CA.v_in, CA.v_out, CA.time]
        df = transpose(array(vectors))
        filepath = desired_path + '/Velocities.csv'
        savetxt(filepath, df, delimiter=',', header='v_in [m/s], v_out [m/s], time [s]', fmt='%s')

        if CA.thermal_analysis:
            vectors = [CA.plastic_strain, CA.plastic_stress, CA.IR_temperature, CA.plastic_time]
            df = transpose(array(vectors))
            filepath = desired_path + '/Plastic Strain and Temperature.csv'
            savetxt(filepath, df, delimiter=',', header='strain, stress [GPa], Temperature [K], time[s]', fmt='%s')

            vectors = [CA.plastic_strain, CA.plastic_stress, CA.beta_int]
            df = transpose(array(vectors))
            filepath = desired_path + '/Plastic Stress - Strain - beta_int.csv'
            savetxt(filepath, df, delimiter=',', header='strain , stress [GPa], beta_int', fmt='%s')

        if CA.specimen_mode == "shear":
            vectors = [CA.incid.y, CA.trans.y, CA.time]
            df = transpose(array(vectors))
            filepath = desired_path + '/Bar Strains.csv'
            savetxt(filepath, df, delimiter=',', header='incident strain, transmitted strain, time [s]', fmt='%s')

    f_path = desired_path + "/Parameters.txt"

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


