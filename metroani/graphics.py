'''Functions that draw graphics for every frame, given surface'''
import gizeh as gz

from .utils import rgb
from .s_types import Metro, Yamanote, JR, Tokyu


def draw_metro_frames(surface, constants):
    # Draw separator line
    gz.polyline(
        [(0, constants.sep_height), (constants.width, constants.sep_height)],
        stroke=Metro.stroke_color, stroke_width=Metro.stroke_width
    ).draw(surface)

    # Draw background for 'next' station text
    gz.rectangle(
        lx=constants.width*2, ly=Metro.rectangle_height,
        xy=[0,0], fill=Metro.rectangle_fill
    ).draw(surface)


def draw_yamanote_frames(surface, constants):
    # Change background color
    gz.rectangle(
        lx=constants.width * 2, ly=constants.height * 2,
        fill=Yamanote.bg_color
    ).draw(surface)

    # Fill station info in the top with background
    gz.rectangle(
        lx=constants.width, ly=constants.sep_height,
        xy=[constants.width/2,constants.sep_height/2],
        fill=Yamanote.rectangle_fill
    ).draw(surface)

    # Add line color indicator
    gz.rectangle(
        lx=Yamanote.indicator_width, ly=constants.sep_height,
        xy=[Yamanote.indicator_pos, constants.sep_height/2],
        fill=constants.line_color
    ).draw(surface)


def draw_jr_frames(surface, constants):
    # Change background color
    gz.rectangle(
        lx=constants.width * 2, ly=constants.height * 2,
        fill=JR.bottom_bg_color
    ).draw(surface)

    # Fill station info in the top with background
    gz.rectangle(
        lx=constants.width, ly=constants.sep_height,
        xy=[constants.width/2,constants.sep_height/2],
        fill=JR.top_bg_color
    ).draw(surface)

    # Fill station text with background
    gz.rectangle(
        lx=constants.width * JR.box_width_mul,
        ly=constants.sep_height * JR.box_height_mul,
        xy=[constants.width/2, constants.sep_height/2 + 50],
        fill=JR.station_bg_color
    ).draw(surface)


def draw_tokyu_frames(surface, constants):
    # Change background color
    gz.rectangle(
        lx=constants.width * 2, ly=constants.height * 2,
        fill=Tokyu.bg_color
    ).draw(surface)

    # Fill station info in the top with background
    gz.rectangle(
        lx=constants.width, ly=constants.sep_height,
        xy=[constants.width/2,constants.sep_height/2],
        fill=Tokyu.rectangle_fill
    ).draw(surface)


def make_vertical_text(text, surface, first_xy, spacing, **kwargs):
    for idx, letter in enumerate(text):
        gz.text(
            letter, xy=[first_xy[0], first_xy[1] + spacing*idx], **kwargs
        ).draw(surface)


def make_bar(surface, constants, bar_width, bar_height, bar_x, bar_y):
    # Light bar
    gz.rectangle(
        lx=bar_width, ly=bar_height,
        xy=[bar_x, bar_y],
        fill=constants.line_color
    ).draw(surface)

    # Dark bar
    gz.rectangle(
        lx=bar_width, ly=bar_height,
        xy=[bar_x, bar_y + bar_height],
        fill=constants.line_color_dark
    ).draw(surface)


def make_triangles(surface, constants, triangle_x, triangle_width, bar_y,
                   bar_height):
    # Light triangle
    gz.polyline(
        [
            (triangle_x                 , bar_y - bar_height/2),
            (triangle_x + triangle_width, bar_y + bar_height/2),
            (triangle_x                 , bar_y + bar_height/2),
        ],
        close_path=True, fill=constants.line_color
    ).draw(surface)

    # Dark triangle
    gz.polyline(
        [
            (triangle_x                 , bar_y + bar_height/2),
            (triangle_x + triangle_width, bar_y + bar_height/2),
            (triangle_x                 , bar_y + bar_height*3/2),
        ],
        close_path=True, fill=constants.line_color_dark
    ).draw(surface)


def make_station_info(surface, settings_to_show, rect_width, bar_height,
                      rect_x, spacing, bar_y, section_center, constants):
    if constants.theme.lower() == 'tokyu':
        func = gz.circle
        args = {'r': bar_height*0.9}
    else:
        func = gz.rectangle
        args = {'lx': rect_width, 'ly': bar_height*2*0.8}

    for n, setting in zip(range(8), settings_to_show):
        x_pos = rect_x + spacing * n
        color = (.5, .5, .5) if setting.skip else (0, 0, 0)
        arrow_x_pos = x_pos - 15
        arrow_width = 5

        # Station rectangles/circles
        if setting.skip:
            gz.polyline(
                [
                    (arrow_x_pos - arrow_width, bar_y - 5),
                    (arrow_x_pos + arrow_width, bar_y - 5),
                    (arrow_x_pos + 7*arrow_width, bar_y + 30),
                    (arrow_x_pos + arrow_width, bar_y + 65),
                    (arrow_x_pos - arrow_width, bar_y + 65),
                    (arrow_x_pos + 5*arrow_width, bar_y + 30),
                ],
                stroke=[1,1,1], stroke_width=5,
                fill=[1,1,1], close_path=True
            ).draw(surface)
        else:
            func(
                fill=[1,1,1,0.9],
                xy=[x_pos, bar_y + bar_height/2],
                **args
            ).draw(surface)

        # Station numbers
        gz.text(
            setting.station_number, 'Roboto', 50,
            xy=[x_pos, section_center - 40],
            fill=color
        ).draw(surface)

        # Station names
        # TODO: font, fontsize, change language, option to rotate instead
        make_vertical_text(
            setting.names.curr().name, surface,
            first_xy=[x_pos, section_center + 40],
            spacing=70, fontfamily='Hiragino Sans GB W3', fontsize=70,
            fill=color
        )

        # Display every transfer line for every station in its first language
        for idx, transfer in enumerate(setting.transfers):
            y_pos = (bar_y - bar_height) + 10 - idx*40
            # TODO: Transition between different translations
            current_translation = transfer[0]

            gz.text(
                current_translation.name,
                fontfamily=current_translation.font,
                fontsize=current_translation.fontsize,
                xy=[x_pos, y_pos],
                fill=color
            ).scale(
                rx=current_translation.scale_x,
                ry=1,
                center=[x_pos, y_pos]
            ).draw(surface)


def make_seperator(surface, constants, section_center):
    gz.polyline(
        [(0, section_center),(constants.width, section_center)],
        stroke=constants.line_color, stroke_width=8
    ).draw(surface)


def make_arrow(surface, spacing, rect_width, arrow_x_offset, rect_x, bar_y,
               bar_height):
    arrow_width = spacing / 2 - rect_width/2
    points = [
        (
            arrow_x_offset + rect_x + rect_width/2,
            bar_y - bar_height/2
        ),
        (
            arrow_x_offset + rect_x + rect_width/2 + arrow_width,
            bar_y - bar_height/2
        ),
        (
            arrow_x_offset + rect_x + spacing - rect_width/2,
            bar_y + bar_height/2
        ),
        (
            arrow_x_offset + rect_x + rect_width/2 + arrow_width,
            bar_y + bar_height*3/2
        ),
        (
            arrow_x_offset + rect_x + rect_width/2,
            bar_y + bar_height*3/2
        ),
        (
            arrow_x_offset + rect_x + spacing - rect_width/2 - arrow_width,
            bar_y + bar_height/2
        ),
    ]
    gz.polyline(
        points,close_path=True, stroke=[1,1,1], stroke_width=5,
        fill=rgb([251, 3, 1])
    ).draw(surface)
    # TODO flash arrow color


def make_line_info(surface, constants, settings, station_idx):
    # Set values
    # Fundamental constants
    max_stations = 8
    number_of_stations = len(settings)
    remaining_stations = number_of_stations - station_idx
    section_center = (
        (constants.height - constants.sep_height) / 2
        + constants.sep_height
    )

    # Bar settings
    bar_height = constants.height * 0.05
    bar_width = constants.width * 0.955
    bar_x = bar_width/2
    # The bottom of the bars is slightly above the center of the section
    bar_y = (
        section_center - bar_height * 2
        - 40  # Approx fontheight/2
    )

    # Triangle settings
    triangle_width = constants.width * 0.03
    # bar_x is the center of the bar, but triangle_x is the start of the bar
    triangle_x = bar_x + bar_width/2 - 1

    # Rectangle settings
    rect_width = bar_width * 0.06
    edge_padding = constants.width * 0.05
    rect_x = (
        (constants.width - bar_width - triangle_width)/2
        + rect_width/2
        + edge_padding
    )
    max_rect_x = triangle_x - edge_padding - rect_width/2
    spacing = (max_rect_x - rect_x) / (max_stations - 1)

    # Arrow and station slice settings
    arrow_x_offset = 0

    if remaining_stations <= max_stations - 2:
        # End of the line: show all 8 stations from the last
        settings_to_show = settings[-max_stations:]
        # Move arrow to between next rectangle
        arrow_x_offset = spacing * (max_stations - 1 - remaining_stations)
    elif station_idx == 0:
        # 1st -> 2nd station: show 1st station as 'previous'
        settings_to_show = settings[station_idx:station_idx + max_stations]
        # Move arrow to center of first rectangle
        arrow_x_offset = - spacing/2
    else:
        # Anywhere else in the line: show previous station
        settings_to_show = settings[station_idx-1:station_idx + max_stations - 1]

    # Actually draw the frame
    make_bar(surface, constants, bar_width, bar_height, bar_x, bar_y)

    if remaining_stations > max_stations - 1:
        make_triangles(
            surface, constants, triangle_x, triangle_width, bar_y,
            bar_height
        )

    make_station_info(
        surface, settings_to_show, rect_width, bar_height, rect_x,
        spacing, bar_y, section_center, constants
    )

    make_seperator(surface, constants, section_center)

    make_arrow(
        surface, spacing, rect_width, arrow_x_offset, rect_x, bar_y, bar_height
    )


def make_station_icon(surface, settings, n, constants):
    x_pos, y_pos = constants.icon_xy

    if constants.icon_shape.lower() == 'square':
        mod = 40
        gz.square(
            constants.icon_size,
            xy=[x_pos, y_pos],
            stroke=constants.line_color,
            stroke_width=15,
            fill=[1,1,1]
        ).draw(surface)
    else:
        mod = 45
        gz.circle(
            constants.icon_size,
            xy=[x_pos, y_pos],
            stroke=constants.line_color,
            stroke_width=30,
            fill=[1,1,1]
        ).draw(surface)

    line, num = settings[n].station_number.split('-')
    gz.text(
        line, constants.icon_text_font,
        constants.icon_line_fontsize, xy=[x_pos, y_pos-mod]
    ).draw(surface)
    gz.text(
        num, constants.icon_text_font,
        constants.icon_station_fontsize, xy=[x_pos, y_pos+30]
    ).draw(surface)
