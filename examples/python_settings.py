import os
import sys

sys.path.append(os.path.abspath('.'))

import metroani

# Constants
constants = metroani.Constants(
    height=1080,
    width=1920,
    duration=0.7,
    freeze_duration=1,
    sep_height=350,
    line_color=[0.19, 0.71, 0.85],
    line_color_dark=[0.12, 0.6, 0.81],
    theme='metro',
    icon_xy=[650, 240],
    icon_text_font='Roboto',
    icon_line_fontsize=60,
    icon_station_fontsize=70
)

# Station settings
saginomiya_names = metroani.CircularList([
    metroani.Translation(
        name='鷺ノ宮',
        font='Hiragino Sans GB W3',
        fontsize=200,
        enter_xy=[960,110],
        exit_xy=[960,320],
        scale_x=1
    ),
    metroani.Translation(
        name='Saginomiya',
        font='Robot',
        fontsize=170,
        enter_xy=[1400,120],
        exit_xy=[1400,320],
        scale_x=0.8
    )
])
saginomiya = metroani.StationTransition(
    names=saginomiya_names,
    xy=[1300, 220],
    station_number='SS-09',
    transfers=[]
)

toritsu_kasei_names = metroani.CircularList([
    metroani.Translation(
        name='都立家政',
        font='Hiragino Sans GB W3',
        fontsize=200,
        enter_xy=[960,110],
        exit_xy=[960,320],
        scale_x=1
    ),
    metroani.Translation(
        name='Toritsu-Kasei',
        font='Robot',
        fontsize=170,
        enter_xy=[1400,120],
        exit_xy=[1400,320],
        scale_x=0.8
    )
])
toritsu_kasei = metroani.StationTransition(
    names=toritsu_kasei_names,
    xy=[1300, 220],
    station_number='SS-08',
    transfers=[]
)
station_settings = [saginomiya, toritsu_kasei]

# Terminus station setting
terminal = metroani.CircularList([
    metroani.Translation(
        name='西武新宿 ゆき',
        font='Hiragino Sans GB W3',
        fontsize=70,
        enter_xy=[960,35],
        exit_xy=[960,100],
        scale_x=1
    ),
    metroani.Translation(
        name='For Seibu Shinjuku',
        font='Roboto',
        fontsize=60,
        enter_xy=[960,35],
        exit_xy=[960,110],
        scale_x=0.8
    )
])
terminal_settings = metroani.Transition(terminal, [650, 70])

# Train state settings
next_ = metroani.CircularList([
    metroani.Translation(
        name='つぎは',
        font='Hiragino Sans GB W3',
        fontsize=70,
        enter_xy=[960,250],
        exit_xy=[960,330],
        scale_x=1
    ),
    metroani.Translation(
        name='Next',
        font='Roboto',
        fontsize=60,
        enter_xy=[960,250],
        exit_xy=[960,330],
        scale_x=1
    )
])
next_settings = metroani.Transition(next_, [300, 280])

# Other possible states:
# まもなく -> Arriving at
# ただいま -> Now stopping at

clip = metroani.make_video(
    station_settings,
    [next_settings],
    terminal_settings,
    constants
)

# We can write the clip into a video file, but this file is just a demostration
# of the python settings API