#!/usr/bin/env python3
# encoding: utf-8 (as per PEP 263)

import sys
from jinja2 import Environment, FileSystemLoader, select_autoescape

def main():
    env = Environment(
        loader=FileSystemLoader("."),
        autoescape=select_autoescape()
    )
    template = env.get_template("schedule.html.j2")
    content = {
            'days': [
                {
                    'name': 'Wed, 28.08.',
                    'stages': [
                        {
                            'name': 'Main',
                            'bands': [

                                ]
                        },
                        {
                            'name': 'Wera',
                            'bands': [

                                ]
                            }
                    ]
                    }
                ]
            }
    print(template.render(content))


if __name__ == '__main__':
    main()
