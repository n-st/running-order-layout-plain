#!/usr/bin/env python3
# encoding: utf-8 (as per PEP 263)

import sys
from jinja2 import Environment, FileSystemLoader, select_autoescape
import csv

# The running order considers "Friday 1:30" as part of Thursday.
# To simplify calculations, we internally represent it as "Thursday 25:30", and
# only `mod 24` the number when displaying it to the user.
# The rollover hour is the first hour that will not be considered part of the
# next day, e.g. rollover_hour=7 -> "Friday 6:30 = Thursday 30:30; Friday 7:00
# = Friday 7:00"
DAY_ROLLOVER_HOUR = 7

def main():
    env = Environment(
        loader=FileSystemLoader("."),
        autoescape=select_autoescape()
    )
    template = env.get_template("schedule.html.j2")

    content = {'days': {}}
    minhour = 24
    maxhour = 0

    with open('shows.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        for row in reader:
            # Example row:
            # 17.08.;Main;01:00;02:00;DIE APOKALYPTISCHEN REITER;genre;DE;1984
            fields = dict(enumerate(row))
            day = fields.get(0, 'unknown day')
            stage = fields.get(1, 'unknown stage')
            start = fields.get(2, '12:34')
            starth, startm = [int(x) for x in start.split(':')]
            end = fields.get(3, '12:35')
            endh, endm = [int(x) for x in end.split(':')]
            if starth < DAY_ROLLOVER_HOUR:
                starth += 24
            if endh < DAY_ROLLOVER_HOUR:
                endh += 24
            duration = (endh - starth) * 60 + (endm - startm)
            minhour = min(minhour, starth)
            maxhour = max(maxhour, endh)
            name = fields.get(4, '[no band name]')
            genre = fields.get(5, '')
            country = fields.get(6, '')
            year = fields.get(7, '')
            if day not in content['days']:
                content['days'][day] = {
                    'stages': {}
                }
            if stage not in content['days'][day]['stages']:
                content['days'][day]['stages'][stage] = {
                    'bands': []
                }
            band = {
                'name': name,
                'starth': starth,
                'startm': startm,
                'endh': endh,
                'endm': endm,
                'duration': duration,
                'genre': genre,
                'country': country,
                'year': year,
            }
            content['days'][day]['stages'][stage]['bands'].append(band)

    content['minhour'] = minhour
    content['maxhour'] = maxhour

    print(template.render(content))


if __name__ == '__main__':
    main()
