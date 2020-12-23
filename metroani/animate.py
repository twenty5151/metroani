'''Animation functions'''
from .ft import make_frames

import moviepy.editor as mpy
import moviepy.video.fx.all as vfx


def animate(n, settings, next_settings, terminal_settings, constants):
    '''Animates a transition between two languages'''
    return (
        mpy.VideoClip(
            make_frames(
                constants=constants, n=n, settings=settings,
                next_settings=next_settings, terminal_settings=terminal_settings,
                old=names[0], new=names[1], old_next=next_[0], new_next=next_[1],
                old_term=terminal[0], new_term=terminal[1]
            ),
            duration=constants.duration
        )

        for names, next_, terminal in zip(
            settings[n].names.pairs(), next_settings.names.pairs(),
            terminal_settings.names.pairs()
        )
        if any([not settings[n].skip for name in names])
    )


def freeze_end(clip, constants):
    return clip.fx(
        vfx.freeze, t=constants.duration,
        freeze_duration=constants.freeze_duration
    )


def freeze_both(clip, constants):
    return freeze_end(clip, constants).fx(
        vfx.freeze, t=0, freeze_duration=constants.freeze_duration
    )


def freeze(idx, clip, constants):
    if idx % 2 != 0:
        return freeze_end(clip, constants)
    return freeze_both(clip, constants)


def concat_or_skip(clips):
    if clips:
        return mpy.concatenate_videoclips(clips)
    return None


def combine_language_transitions(
    n, station_settings, state_setting, terminal_settings, constants
):
    '''Combines multiple language transitions for a given train state'''
    return concat_or_skip([
        freeze(idx, clip, constants)
        for idx, clip in enumerate(animate(
            n, station_settings, state_setting, terminal_settings, constants
        ))
    ])


def combine_train_states(
    n, station_settings, state_settings, terminal_settings, constants
):
    '''Combines multiple train states and multiple language transitions'''
    return (
        combine_language_transitions(
            n, station_settings, state_setting, terminal_settings, constants
        )
        for state_setting in state_settings
    )

