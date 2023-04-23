import csv
import argparse

from string import Template

def parse_command_line():
    description = 'Converts input into the expected dictionary format.'
    argparser = argparse.ArgumentParser(description=description)
    argparser.add_argument('input_file', metavar='input_file', type=str,
                        help='Input file')
    argparser.add_argument('--format', metavar='format', type=str,
                        default='default_tsv',
                        help='The format of the input file (see README for supported formats)')

    return argparser.parse_args()

def read_default_tsv(in_file):
    # The `default_tsv` format is simply:
    # word,translation,pos,extra_content

    ret = {}
    with open(in_file, newline='') as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            row_data = {'translation': row[1],
                        'pos': row[2],
                        'context': row[3]}

            if row[0] in ret:
                ret[row[0]].append(row_data)
            else:
                ret[row[0]] = [row_data]
    return ret


def read_input_file(args):
    input_file = args.input_file
    input_format = args.format

    # Read input file
    input_reading_function = input_reader.get(input_format)
    input_data = input_reading_function(input_file)
    return input_data


entry_template = '''<idx:entry name="default" scriptable="yes" spell="yes">
  <h5><dt><idx:orth>{}</idx:orth></dt></h5>
  <dd>Part of speech: {}</dd>
  <dd>Translation: {}</dd>
  {}
</idx:entry>
<hr/>'''

def generate_other_contents(entry):
    all_entry_keys = list(entry.keys())
    all_entry_keys.remove('translation')
    all_entry_keys.remove('pos')
    return '\n'.join([entry[i] for i in all_entry_keys])


def generate_content(token, entry):
    rest = generate_other_contents(entry)
    return entry_template.format(token,
                                 entry['translation'],
                                 entry['pos'],
                                 rest)

def input2content(in_data):
    # `in_data` is expected to be dictionary, containing lists as elements.
    # Each entry is a word, so `in_data['hello']` will return data related to
    # the word 'hello'.
    #
    # What does this data look like? It is a list, containing the different
    # possible "entries" of each word. So, if 'hello' has two possible meanings,
    # `in_data['hello']` will return a list containing two elements.
    #
    # Each of the list's elements is a dictionary itself (see
    # `read_default_tsv()`)
    #
    # As a simple example, a 3-word German dictionary with 2 repeated entries
    # for the word "Hund" and one entry for "Nacht" would be:
    # {'Hund': [{'translation': 'dog',
    #            'pos': 'noun',
    #            'context': 'biol.'},
    #           {'translation': 'hound',
    #            'pos': 'noun',
    #            'context': 'biol.'}],
    #  'Nacht': [{'translation': 'night',
    #            'pos': 'noun',
    #            'context': ''}]}

    content = []
    for token in in_data.keys():
        for entry in in_data[token]:
            content.append(generate_content(token, entry))
    return "\n".join(content)


input_reader = {
    'default_tsv': read_default_tsv,
}

if __name__ == '__main__':
    args = parse_command_line()
    input_data = read_input_file(args)
    all_entries = input2content(input_data)
    content = {'all_entries': all_entries}

    # Based on https://stackoverflow.com/a/6385940
    with open('content_template.html', 'r') as f:
        src = Template(f.read())

    result = src.substitute(content)
    with open('content.html', 'w') as f:
        f.write(result)

