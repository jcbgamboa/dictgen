import argparse
from string import Template

def parse_command_line():
    description = 'Generates the boilerplate necessary for the .opf file.'
    argparser = argparse.ArgumentParser(description=description)
    argparser.add_argument('dictionary_name', metavar='dictionary_name', type=str,
                           help='The name of your new dictionary (a book name)')

    argparser.add_argument('dictionary_author', metavar='dictionary_author', type=str,
                           help='You!')

    argparser.add_argument('copyright_remark', metavar='copyright_remark', type=str,
                           help="Probably you want to say the book's licence name here.")

    return argparser.parse_args()


def gen_usage_boilerplate(args):
    with open('usage_template.html', 'r') as f:
        src = Template(f.read())

    # In the future, if needed, add code to change the usage template
    usage = {}

    result = src.substitute(usage)
    with open('usage.html', 'w') as f:
        f.write(result)


def gen_copyright_boilerplate(args):
    with open('copyright_template.html', 'r') as f:
        src = Template(f.read())
    copyright = {'copyright': args.copyright_remark}
    result = src.substitute(copyright)
    with open('copyright.html', 'w') as f:
        f.write(result)

def gen_cover_boilerplate(args):
    with open('cover_template.html', 'r') as f:
        src = Template(f.read())
    cover = {'dictionary_name': args.dictionary_name,
             'dictionary_author': args.dictionary_author}
    result = src.substitute(cover)
    with open('cover.html', 'w') as f:
        f.write(result)

if __name__ == '__main__':
    args = parse_command_line()
    gen_usage_boilerplate(args)
    gen_copyright_boilerplate(args)
    gen_cover_boilerplate(args)

