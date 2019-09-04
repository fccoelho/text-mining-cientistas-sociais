#!/usr/bin/env python3
import jinja2
import glob
import os
import re

latex_jinja_env = jinja2.Environment(
    block_start_string='\BLOCK{',
    block_end_string='}',
    variable_start_string='\VAR{',
    variable_end_string='}',
    comment_start_string='\#{',
    comment_end_string='}',
    line_statement_prefix='%%',
    line_comment_prefix='%#',
    trim_blocks=True,
    autoescape=False,
    loader=jinja2.FileSystemLoader(os.path.abspath('.'))
)

## Add in the list below, the Notebook latex files to become chapters, in the desired order.

chapters = [
    'Capitulo_1.tex',
]


def render(files):
    """
    Render book template
    """
    template = latex_jinja_env.get_template('Book/Book_master.tex')
    with open('Book/book.tex', 'w') as f:
        f.write(template.render(chapters=files))


def move_directories():
    """
    Move directories to the Book directory
    :return:
    """
    for f in glob.glob('*'):
        if f == 'Book':
            continue
        if os.path.isdir(f):
            print(f)
            os.system(r"rm -rf 'Book/{}' && mv -f '{}'/ 'Book/{}'".format(f, f, f))


def chop_files(files):
    """
    Chop the files keeping only the document block
    """
    pattern = r'\\title{([\w\s]+)}'
    for n, fn in enumerate(files):
        with open(fn, 'r') as inp:
            text = inp.read()
            try:
                chapter_title = re.findall(pattern, text)[0]
            except IndexError as exc:
                print(exc, re.findall(pattern, text))
                chapter_title = 'Chapter'
            body = text.split(r'\maketitle')[1].split(r'\end{document}')[0]
            with open('Book/chapter_{}.tex'.format(n), 'w') as out:
                out.write(r'\chapter{' + chapter_title + '}\n' + body)


if __name__ == "__main__":
    move_directories()
    chop_files(chapters)
    chapter_files = [f.split('/')[1].split('.tex')[0] for f in glob.glob('Book/chapter*.tex')]
    render(chapter_files)


