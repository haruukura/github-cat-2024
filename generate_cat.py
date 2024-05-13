#!/usr/bin/env python3
"""
Generates backdated git commits to draw a pixel art cat on the GitHub contribution graph for 2024.
Spans across May to August 2024.
"""
import os
import sys
import datetime
import subprocess

# Cat sprite: 15 columns x 7 rows
# Row 0: Sun, 1: Mon, 2: Tue, 3: Wed, 4: Thu, 5: Fri, 6: Sat
CAT_SPRITE = [
    ' #   #      ## ',  # 0: Sun (ears & tail top)
    '### ###    #  #',  # 1: Mon (ear bases & tail loop)
    '#######       #',  # 2: Tue (forehead & tail upright)
    '# ### #       #',  # 3: Wed (face with eyes & tail)
    '############## ',  # 4: Thu (body connecting to tail)
    ' ############# ',  # 5: Fri (belly)
    '  ##     ##    ',  # 6: Sat (paws)
]

def generate():
    repo_dir = os.path.dirname(os.path.abspath(__file__))
    start_sun = datetime.date(2023, 12, 31)
    offset = 19  # Starts week 19 (May 12, 2024) and ends week 33 (August 24, 2024)

    active_days = []
    for r in range(7):
        for c in range(len(CAT_SPRITE[r])):
            if CAT_SPRITE[r][c] == '#':
                col_idx = offset + c
                d = start_sun + datetime.timedelta(days=col_idx * 7 + r)
                active_days.append((d, r, c, col_idx))

    active_days.sort(key=lambda x: x[0])

    env = os.environ.copy()
    env['GIT_AUTHOR_NAME'] = 'haruukura'
    env['GIT_AUTHOR_EMAIL'] = 'daniellin6656@gmail.com'
    env['GIT_COMMITTER_NAME'] = 'haruukura'
    env['GIT_COMMITTER_EMAIL'] = 'daniellin6656@gmail.com'

    commits_file = os.path.join(repo_dir, 'cat.txt')
    total = 0
    for d, r, c, col_idx in active_days:
        date_str = d.strftime('%Y-%m-%d')
        day_name = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'][r]
        for i in range(5):
            time_str = f'12:{i:02d}:00 -0400'
            commit_dt = f'{date_str} {time_str}'
            env['GIT_AUTHOR_DATE'] = commit_dt
            env['GIT_COMMITTER_DATE'] = commit_dt

            with open(commits_file, 'a') as f:
                f.write(f'{commit_dt} | {day_name} | Col {col_idx} | ({r},{c}) | #{i+1}\n')

            subprocess.run(['git', 'add', 'cat.txt', 'README.md', 'generate_cat.py'], cwd=repo_dir, check=True)
            msg = f'cat {date_str} [{i+1}/5]'
            subprocess.run(['git', 'commit', '-m', msg], cwd=repo_dir, env=env, check=True, capture_output=True)
            total += 1

    print(f'Done! Created {total} commits across {len(active_days)} days.')

if __name__ == '__main__':
    generate()
