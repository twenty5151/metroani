import os
import sys

sys.path.append(os.path.abspath('.'))

import metroani


video = metroani.make_video(*metroani.settings_from_json('settings/gif.json'))

gif_duration = (1 + 0.7 + 1 + 0.7 + 1) * 2

(video
    .subclip(0, gif_duration)
    .resize(0.5)
    .write_gif('examples/example.gif', fps=24))

os.system('gifsicle -O3 examples/example.gif -o examples/out.gif')
os.system('rm examples/example.gif')
os.system('mv examples/out.gif examples/example.gif')
