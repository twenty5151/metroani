import json

import moviepy.editor as mpy

from .animate import combine_train_states
from .s_types import Constants, Transition, StationTransition, TerminusTransition


def make_video(
    constants, station_settings, terminal_settings, state_settings, service_settings
):
    start = 0 if constants.show_direction else 1
    final = (
        combine_train_states(
            n, station_settings, state_settings, terminal_settings, constants,
            service_settings
        )
        for n in range(start, len(station_settings))
    )

    return mpy.concatenate_videoclips([
        clip
        for station_clips in final
        for clip in station_clips
        if clip is not None
    ])


def settings_from_json(file_):
    with open(file_, 'r') as f:
        settings = json.load(f)

    return (
        Constants(**settings['constants']),
        StationTransition.from_json_list(settings, 'stations'),
        TerminusTransition.from_json(settings, 'terminal'),
        [Transition.from_json(settings['states'], key)
         for key in settings['states'].keys()],
        Transition.from_json(settings, 'service_type')
    )
