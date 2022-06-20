Tabs = '''
#:import MDDropdownMenu kivymd.uix.menu.MDDropdownMenu
#:import MDExpansionPanelLabel kivymd.uix.expansionpanel.MDExpansionPanelLabel 
#:import MDExpansionPanelThreeLine kivymd.uix.expansionpanel.MDExpansionPanelThreeLine
#:import RoundedRectangularElevationBehavior kivymd.uix.behaviors 
<TooltipMDIconButton@MDIconButton+MDTooltip+HoverBehavior>
<MDFloatingActionButtonTooltip@MDFloatingActionButton+MDTooltip>
<HoverButton@HoverBehavior+MDRectangleFlatButton>
<HoverTextButton@HoverBehavior+MDTextButton>
<M3Card@MDCard+RoundedRectangularElevationBehavior>

MDBoxLayout:
    orientation: "vertical"

    MDTabs:
        id: tabs
        tab_indicator_type: "round"
        tab_indicator_anim: True
        default_tab: 1
        tab_hint_x: True
        on_tab_switch:  app.on_tab_switch(*args)
        allow_strech:   True
        tab_indicator_height: "0dp"
        indicator_color: 0.95, 0.88, 0.82, 0.7
        background_color: app.main_color
        font_name: app.text_font
        lock_swiping: True

<Check@MDCheckbox>:
    group: 'group'
    size_hint:  None, None
    size: dp(48), dp(48)

<InfoTab>
    md_bg_color: app.light_or_dark       
    MDLabel:
        pos_hint:  {'center_x': .5, 'center_y': .7}
        text:   "developed by Tzvi Gershanik, Itay Levin & Daniel Rittel."
        font_size:  14
        halign: "center"
        font_name: app.text_font


    Image:
        source: "images/2BarG.png"
        pos_hint: {"center_x": 0.5, "center_y":0.8}

    M3Card:
        orientation: "vertical"
        padding: "15dp"
        size_hint: None, None
        size: "450", "400dp"
        pos_hint: {"center_x": .5, "center_y": .4}
        radius: dp(10)
        md_bg_color: 0.898, 0.725, 0.69, 0.1

        MDLabel:
            text: "About DFL"
            theme_text_color: "Secondary"
            size_hint_y: None
            height: self.texture_size[1]

        MDSeparator:
            height: "2dp"

        MDLabel:
            halign: "justify"
            text: app.about_dfl
            font_name: "GARA"
            font_size: 18

<ParametersTab>
    md_bg_color: app.light_or_dark   

    MDTextField:
        id: spec_diam
        font_name_hint_text: app.text_font
        hint_text:  "Specimen Diameter [m]"
        multiline:  False
        on_text_validate:   app.ButtonAction_update_parameter("specimen", 0, self)
        helper_text: "Default value: {} [m]".format(app.parameters[0][1])
        helper_text_mode: "on_focus"
        helper_text_color: app.pink
        icon_right: "diameter"
        icon_right_color: app.pink
        pos_hint: {'center_x': 0.25, 'center_y': 0.9}
        size_hint_x: None
        width: 240

    MDTextField:
        id: spec_length
        font_name_hint_text: app.text_font
        hint_text:  "Specimen Length [m]"
        multiline:  False
        on_text_validate:   app.ButtonAction_update_parameter("specimen", 1, self)
        helper_text: "Default value: {} [m]".format(app.parameters[1][1])
        helper_text_mode: "on_focus"
        helper_text_color: app.pink
        icon_right: "consolidate"
        icon_right_color: app.pink
        pos_hint: {'center_x': 0.25, 'center_y': 0.8}
        size_hint_x: None
        width: 240
        
    MDTextField:
        id: bar_diameter 
        font_name_hint_text: app.text_font
        hint_text:  "Bar Diameter [m]"
        multiline:  False
        on_text_validate:   app.ButtonAction_update_parameter("experiment", 2, self)
        helper_text: "Default value: {} [m]".format(app.parameters[2][1])
        helper_text_mode: "on_focus"
        helper_text_color: app.pink
        icon_right: "diameter"
        icon_right_color: app.pink
        pos_hint: {'center_x': 0.25, 'center_y': 0.7}
        size_hint_x: None
        width: 240

    MDTextField:
        id: young_modulus
        font_name_hint_text: app.text_font
        hint_text:  "Young's Modulus [GPa]"
        multiline:  False
        on_text_validate:   app.ButtonAction_update_parameter("experiment", 3, self)
        helper_text: "Default value: {} [GPa]".format(app.parameters[3][1]/1e9)
        helper_text_mode: "on_focus"
        helper_text_color: app.pink
        icon_right: "alpha-e-circle"
        icon_right_color: app.pink
        pos_hint: {'center_x': 0.25, 'center_y': 0.6}
        size_hint_x: None
        width: 240

    MDTextField:
        id: first_gage
        font_name_hint_text: app.text_font
        hint_text:  "First Gauge [m]"
        multiline:  False
        on_text_validate:   app.ButtonAction_update_parameter("experiment", 4, self)
        helper_text: "Default value: {} [m]".format(app.parameters[4][1])
        helper_text_mode: "on_focus"
        helper_text_color: app.pink
        icon_right: "chevron-triple-right"
        icon_right_color: app.pink
        pos_hint: {'center_x': 0.25, 'center_y': 0.5}
        size_hint_x: None
        width: 240

    MDTextField:
        id: second_gage
        font_name_hint_text: app.text_font
        hint_text:  "Second Gauge [m]"
        multiline:  False
        on_text_validate:   app.ButtonAction_update_parameter("experiment", 5, self)
        helper_text: "Default value: {} [m]".format(app.parameters[5][1])
        helper_text_mode: "on_focus"
        helper_text_color: app.pink
        icon_right: "transfer-right"
        icon_right_color: app.pink
        pos_hint: {'center_x': 0.25, 'center_y': 0.4}
        size_hint_x: None
        width: 240

    MDTextField:
        id: sound_velocity
        font_name_hint_text: app.text_font
        hint_text:  "Sound Velocity [m/s]"
        multiline:  False
        on_text_validate:   app.ButtonAction_update_parameter("experiment", 6, self)
        helper_text: "Default value: {} [m/s]".format(app.parameters[6][1])
        helper_text_mode: "on_focus"
        helper_text_color: app.pink
        icon_right: "speedometer"
        icon_right_color: app.pink
        pos_hint: {'center_x': 0.25, 'center_y': 0.3}
        size_hint_x: None
        width: 240

    MDTextField:
        id: gage_factor
        font_name_hint_text: app.text_font
        hint_text:  "Gauge Factor [-]"
        multiline:  False
        on_text_validate:   app.ButtonAction_update_parameter("experiment", 7, self)
        helper_text: "Default value: {}".format(app.parameters[7][1])
        helper_text_mode: "on_focus"
        helper_text_color: app.pink
        icon_right: "gauge"
        icon_right_color: app.pink
        pos_hint: {'center_x': 0.25, 'center_y': 0.2}
        size_hint_x: None
        width: 240

    MDTextField:
        id: bridge_tension
        font_name_hint_text: app.text_font
        hint_text:  "Bridge Tension [V]"
        multiline:  False
        on_text_validate:   app.ButtonAction_update_parameter("experiment", 8, self)
        helper_text: "Default value: {} [V]".format(app.parameters[8][1])
        helper_text_mode: "on_focus"
        helper_text_color: app.pink
        icon_right: "bridge"
        icon_right_color: app.pink
        pos_hint: {'center_x': 0.25, 'center_y': 0.1}
        size_hint_x: None
        width: 240

    HoverButton:
        id: experiment_chooser
        text: "Analyze."
        pos_hint: {"center_x": .7, "center_y": .87}
        font_size: 70
        text_color: "#808080"
        line_color: "#808080"
        font_name: "GOTHIC"
        on_release: app.experiments_menu.open()
        on_enter:   self.text_color = app.pink; self.line_color = app.pink
        on_leave:   self.text_color = "#808080"; self.line_color = "#808080"

    MDBoxLayout:
        adaptive_size: True
        pos_hint: {"center_x": .7, "center_y": .475}

        MyToggleButton:
            text: "Auto"
            state: "down"
            group: "cropping"
            font_name: app.text_font
            on_release: app.sp_mode = "Automatic" 

        MyToggleButton:
            text: "Manual"
            font_name: app.text_font
            group: "cropping"
            state: "normal"
            on_release: app.sp_mode = "Manual"

    MDLabel:
        pos_hint:  {'center_x': .7, 'center_y': .525}
        text:   "CROPPING"
        font_name: 'GOTHIC'
        font_size: 30
        halign: "center"
        theme_text_color: "Custom"
        text_color: "#808080"

    MDBoxLayout:
        adaptive_size: True
        pos_hint: {"center_x": .7, "center_y": .65}

        MyToggleButton:
            text: "Comp"
            group: "mode"
            state: "down"
            font_name: app.text_font
            on_release: app.mode = "compression" 

        MyToggleButton:
            text: "Tens"
            font_name: app.text_font
            group: "mode"
            state: "normal"
            on_release: app.mode = "tension" 

    MDLabel:
        pos_hint:  {'center_x': .7, 'center_y': .7}
        text:   "MODE"
        font_name: 'GOTHIC'
        font_size: 30
        halign: "center"
        theme_text_color: "Custom"
        text_color: "#808080"

    MDBoxLayout:
        adaptive_size: True
        pos_hint: {"center_x": .7, "center_y": .3}

        MyToggleButton:
            text: "Regular"
            group: "specimen"
            state: "down"
            font_name: app.text_font
            on_release: app.specimen_mode = "regular"; 

        MyToggleButton:
            text: "Shear"
            font_name: app.text_font
            group: "specimen"
            state: "normal"
            on_release: app.specimen_mode = "shear"; 

    MDLabel:
        pos_hint:  {'center_x': .7, 'center_y': .35}
        text:   "SPECIMEN"
        font_name: 'GOTHIC'
        font_size: 30
        halign: "center"
        theme_text_color: "Custom"
        text_color: "#808080"

    HoverTextButton:
        id: INCID
        disabled:   True
        opacity:    0
        pos_hint:  {'center_x': .5, 'center_y': 0.2}
        text: "INCID"
        font_name: app.text_font
        theme_text_color: "Custom"
        font_size: 16
        text_color: "#808080"
        on_enter:   self.text_color = app.main_color
        on_leave:   self.text_color = "#808080"
        on_release: app.ButtonAction_select_data_file("incid")

    HoverTextButton:
        id: TRANS
        disabled:   True
        opacity:    0
        pos_hint:  {'center_x': .6, 'center_y': 0.2}
        text: "TRANS"
        font_name: app.text_font
        theme_text_color: "Custom"
        font_size: 16
        text_color: "#808080"
        on_enter:   self.text_color = app.main_color
        on_leave:   self.text_color = "#808080"
        on_release: app.ButtonAction_select_data_file("trans")

    HoverTextButton:
        id: IR_EXP
        disabled:   True
        opacity:    0
        pos_hint:  {'center_x': .7, 'center_y': 0.2}
        text: "IR EXP"
        font_name: app.text_font
        theme_text_color: "Custom"
        font_size: 16
        text_color: "#808080"
        on_enter:   self.text_color = app.main_color
        on_leave:   self.text_color = "#808080"
        on_release: app.ButtonAction_select_data_file("IR_EXP")

    HoverTextButton:
        id: IR_CAL
        disabled:   True
        opacity:    0
        pos_hint:  {'center_x': .8, 'center_y': 0.2}
        text: "IR CAL"
        font_name: app.text_font
        theme_text_color: "Custom"
        font_size: 16
        text_color: "#808080"
        on_enter:   self.text_color = app.main_color
        on_leave:   self.text_color = "#808080"
        on_release: app.ButtonAction_select_data_file("IR_CAL")

    HoverTextButton:
        id: TC_CAL
        disabled:   True
        opacity:    0
        pos_hint:  {'center_x': .9, 'center_y': 0.2}
        text: "TC CAL"
        font_name: app.text_font
        theme_text_color: "Custom"
        font_size: 16
        text_color: "#808080"
        on_enter:   self.text_color = app.main_color
        on_leave:   self.text_color = "#808080"
        on_release: app.ButtonAction_select_data_file("TC_CAL")

    M3Card:
        padding: 16
        size_hint: None, None
        size: "460dp", "80dp"
        pos_hint:  {'center_x': .7, 'center_y': 0.13}
        md_bg_color: 0.898, 0.725, 0.69, 0.1
        radius: dp(12)
        elevation: 0
        MDRelativeLayout:
            size_hint: None, None
            size: root.size

            TooltipMDIconButton:
                icon: "folder-open"
                tooltip_text: "Set Path Folder"
                on_release: app.ButtonAction_set_path_folder()
                theme_text_color: "Custom"
                text_color: "#808080"
                user_font_size: "30sp"
                tooltip_bg_color:  app.main_color
                on_enter:   self.text_color = app.main_color
                on_leave:   self.text_color = "#808080"

            TooltipMDIconButton:
                icon: "arch"
                tooltip_text: "Set as Default"
                on_release: app.ButtonAction_set_parameters_as_default()
                pos:   dp(75), 0
                theme_text_color: "Custom"
                text_color: "#808080"
                user_font_size: "30sp"
                tooltip_bg_color:  app.main_color
                on_enter:   self.text_color = app.main_color
                on_leave:   self.text_color = "#808080"

            TooltipMDIconButton:
                icon: "check-all"
                tooltip_text: "Analyze All Experiments"
                on_release: app.analyse_all_experiments()
                pos:   dp(225), 0
                theme_text_color: "Custom"
                text_color: "#808080"
                user_font_size: "30sp"
                tooltip_bg_color:  app.main_color
                on_enter:   self.text_color = app.main_color
                on_leave:   self.text_color = "#808080"

            TooltipMDIconButton:
                icon: "download"
                tooltip_text: "Save Parameters"
                on_release: app.ButtonAction_save_parameters_file()
                pos:   dp(300), 0
                theme_text_color: "Custom"
                text_color: "#808080"
                user_font_size: "30sp"
                tooltip_bg_color:  app.main_color
                on_enter:   self.text_color = app.main_color
                on_leave:   self.text_color = "#808080"

            TooltipMDIconButton:
                icon: "upload"
                tooltip_text: "Load Parameters"
                on_release: app.ButtonAction_load_parameters_file()
                pos:   dp(375), 0
                theme_text_color: "Custom"
                text_color: "#808080"
                user_font_size: "30sp"
                tooltip_bg_color:  app.main_color
                on_enter:   self.text_color = app.main_color
                on_leave:   self.text_color = "#808080"

            TooltipMDIconButton:
                id: show_parameters
                icon: "equal-box"
                tooltip_text: "Show Parameters"
                on_release: app.ButtonAction_show_data()
                pos:   dp(150), 0
                theme_text_color: "Custom"
                text_color: "#808080"
                user_font_size: "30sp"
                tooltip_bg_color:  app.main_color
                on_enter:   self.text_color = app.main_color
                on_leave:   self.text_color = "#808080"


<SettingsTab>
    md_bg_color: app.light_or_dark   

    Image:
        source: "images/logo-dfl.png"
        pos_hint: {"center_x": 0.49, "center_y":0.075}
        size_hint: .15, .15

    MDSwitch:
        id: thermal_analysis
        pos_hint:  {'center_x': .585, 'center_y': .2}
        on_active:  app.ButtonAction_change_thermal_analysis()
        on_state:   app.ButtonAction_change_thermal_analysis()

    MDLabel:
        pos_hint:  {'center_x': .895, 'center_y': .2}
        text:   "Thermal Analysis"
        halign: "left"
        font_style: "Button"
    
    MDTextField:
        id: density
        opacity: 0
        font_name_hint_text: app.text_font
        hint_text:  "Density [kg/m^3]"
        multiline:  False
        mode: "rectangle"
        on_text_validate:   app.ButtonAction_update_parameter("specimen", 12, self)
        helper_text: "Default value: {} [kg/m^3]".format(app.parameters[12][1])
        helper_text_mode: "on_focus"
        helper_text_color: app.pink
        icon_right: "chemical-weapon"
        icon_right_color: app.pink
        pos_hint: {'center_x': .2, 'center_y': .2}
        size_hint_x: None
        width: 220
    
    MDTextField:
        id: heat_capacity
        opacity: 0
        font_name_hint_text: app.text_font
        hint_text:  "Heat Capacity [J/kgC]"
        multiline:  False
        mode: "rectangle"
        on_text_validate:   app.ButtonAction_update_parameter("specimen", 13, self)
        helper_text: "Default value: {} [kJ/kgK]".format(app.parameters[13][1])
        helper_text_mode: "on_focus"
        helper_text_color: app.pink
        icon_right: "fire"
        icon_right_color: app.pink
        pos_hint: {'center_x': .8, 'center_y': .2}
        size_hint_x: None
        width: 220

    MDSwitch:
        pos_hint:  {'center_x': .585, 'center_y': .3}
        on_active:  app.ButtonAction_change_auto_open_report()
        on_state:   app.ButtonAction_change_auto_open_report()

    MDLabel:
        pos_hint:  {'center_x': .895, 'center_y': .3}
        text:   "Disable Report"
        halign: "left"
        font_style: "Button"

    MDSwitch:
        id: dark_mode
        pos_hint:  {'center_x': .585, 'center_y': .4}
        on_active:  app.ButtonAction_change_theme()
        on_state:   app.ButtonAction_change_theme()

    MDLabel:
        pos_hint:  {'center_x': .895, 'center_y': .4}
        text:   "Dark Mode"
        halign: "left"
        font_style: "Button"

    MDSwitch:
        pos_hint:  {'center_x': .585, 'center_y': .5}
        on_active:  app.ButtonAction_change_bar_num()
        on_state:   app.ButtonAction_change_bar_num()

    MDLabel:
        pos_hint:  {'center_x': .895, 'center_y': .5}
        text:   "One Bar"
        halign: "left"
        font_style: "Button"

    MDTextField:
        id: prominence_percent
        font_name_hint_text: app.text_font
        hint_text:  "Prominence [%]"
        multiline:  False
        on_text_validate:   app.ButtonAction_update_parameter("spacing", 0, self)
        helper_text: "Default value: {}%".format(app.prominence_percent*100)
        helper_text_mode: "on_focus"
        helper_text_color: app.pink
        pos_hint: {'center_x': .5, 'center_y': .6}
        icon_right: "chart-areaspline"
        icon_right_color: app.pink
        size_hint_x: 0.21
        width: 300

    MDTextField:
        id: spacing
        font_name_hint_text: app.text_font
        hint_text:  "Spacing"
        multiline:  False
        on_text_validate:   app.ButtonAction_update_parameter("spacing", 0, self)
        helper_text: "Default value: {} points".format(app.spacing)
        helper_text_mode: "on_focus"
        helper_text_color: app.pink
        icon_right: "arrow-expand-horizontal"
        icon_right_color: app.pink
        pos_hint: {'center_x': .5, 'center_y': .7}
        size_hint_x: 0.21
        width: 300

    M3Card:
        padding: 16
        size_hint: None, None
        size: "250dp", "50dp"
        pos_hint:  {'center_x': .5, 'center_y': 0.775}
        md_bg_color: 0, 0, 0, 0
        radius: dp(12)
        elevation: 0

        MDSlider:
            id: smooth_slider
            min: 55
            max: 151
            step: 2
            value: 71
            hint: True
            show_off: False

    MDLabel:
        pos_hint:  {'center_x': .895, 'center_y': .825}
        text:   "Curve Smoothing"
        halign: "left"
        font_size: "30sp"
        font_style: "Button"

    TooltipMDIconButton:
        id: curve_smooth_info
        icon: "help-circle"
        tooltip_text: "info"
        on_release: app.ButtonAction_open_curve_smoothing_dialog()
        pos_hint:  {'center_x': .6, 'center_y': .825}
        theme_text_color: "Custom"
        text_color: "#808080"
        user_font_size: "20sp"
        tooltip_bg_color:  app.main_color
        on_enter:   self.text_color = app.main_color
        on_leave:   self.text_color = "#808080"
        
    HoverButton:
        id: show_logger
        text: "VIEW LOGGER"
        pos_hint: {"center_x": .5, "center_y": .9}
        font_size: 25
        text_color: "#808080"
        line_color: "#808080"
        font_name: "GOTHIC"
        on_enter:   self.text_color = app.pink; self.line_color = app.pink
        on_leave:   self.text_color = "#808080"; self.line_color = "#808080"
        on_release: app.toggle_view_logger()
    
    M3Card:
        id: logger_card
        opacity: 0
        orientation: "vertical"
        padding: "15dp"
        size_hint: None, None
        size: "300dp", "550dp"
        pos_hint: {"center_x": .2, "center_y": .6}
        radius: dp(10)
        md_bg_color: 0.898, 0.725, 0.69, 0.1

        MDSeparator:
            height: "0.2dp"
        
        ScrollView:
            MDList:
                id: logger_list
                
                OneLineListItem:
                    text:   "2BarG Initialized."
'''