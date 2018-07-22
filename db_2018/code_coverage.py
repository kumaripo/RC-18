import csv
from DB_Writer import add_code_coverage
from argparse import ArgumentParser
parser = ArgumentParser()
parser.add_argument('--file', required=True, metavar='', help='Sprint Number or release version')

# action = parser.add_mutually_exclusive_group()
# # action.add_argument('--code_coverage', default=False, metavar='', type=bool, help='Input file is code coverage file. Valid values: enable')
# action.add_argument('--sloc', default=False, metavar='', type=bool, help='Input file is sloc file. Valid values: enable')
# action.add_argument('--code-coverage', dest='code_coverage', action='store_true')
# #action.add_argument('--sloc', dest='sloc', action='store_true')
# action.set_defaults(code_coverage=True)
# #action.set_defaults(code_coverage=False)
args = parser.parse_args()


def get_code_coverage_attr():
    return ['release', 'line_coverage', 'func_coverage']


def get_sloc_attr():
    return ['release', 'sloc']


def parse_csv_file():
    with open(args.file, 'rb') as fp:
        data_rows = []
        # parse file into csv module
        reader = csv.reader(fp)

        for row in reader:
            # if args.code_coverage is True and len(row) == 4:
            try:
                keys = get_code_coverage_attr()
            except:
                raise AssertionError('Might be data already present')

            # elif args.sloc is True and len(row) == 2:
            #     keys = get_sloc_attr()

            # else:
            #     raise AssertionError("%s CSV file has invalid number of elements" % args.file)

            data = dict(zip(keys, row))
            data_rows.append(data)

    return data_rows


def main():
    rows = parse_csv_file()
    print rows
    # if args.code_coverage is True:
    try:
       add_code_coverage(rows)
    except :
        print("Error : Data already present!")




if __name__ == '__main__':
    main()
