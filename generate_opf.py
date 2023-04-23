import argparse
from string import Template

def parse_command_line():
    description = 'Generates the boilerplate necessary for the .opf file.'
    argparser = argparse.ArgumentParser(description=description)
    argparser.add_argument('dictionary_name', metavar='dictionary_name', type=str,
                           help='The name of your new dictionary (a book name)')

    argparser.add_argument('dictionary_author', metavar='dictionary_author', type=str,
                           help='You!')

    argparser.add_argument('language', metavar='language', type=str,
                           help='The language of the dictionary.')

    argparser.add_argument('language_in', metavar='language_in', type=str,
                           help='The language of the entries in the dictionary')

    argparser.add_argument('language_out', metavar='language_out', type=str,
                           help='To which language are the entries translated in the dictionary')

    return argparser.parse_args()

def gen_opf_boilerplate(args):
    with open('dict_template.opf', 'r') as f:
        src = Template(f.read())
    cover = {'dictionary_name': args.dictionary_name,
             'dictionary_author': args.dictionary_author,
             'language': args.language,
             'language_in': args.language_in,
             'language_out': args.language_out}
    result = src.substitute(cover)
    with open('dict.opf', 'w') as f:
        f.write(result)


if __name__ == '__main__':
    args = parse_command_line()
    gen_opf_boilerplate(args)
