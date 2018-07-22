import xlrd
from DB_Writer import add_requirements
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('--file', required=True, metavar='', help='Sprint Number or release version')
#action = parser.add_mutually_exclusive_group(required=True)
#action.add_argument('--requirement', dest='requirement', action='store_true')
#action.set_defaults(code_coverage=False)
args = parser.parse_args()

def parse_requirement_file():
    """
    Open and read an Excel file
    """
    book = xlrd.open_workbook(args.file)
    # get the first worksheet
    first_sheet = book.sheet_by_index(0)

    data = []
    for r in range(1, first_sheet.nrows):
        tempdict = {}
        li = first_sheet.row_values(r)
        if (li[0]!= '' and li[1]!= '' and li[2]!= '' and li[3]!= ''):
            tempdict['requirement_id']=li[0]
            tempdict['category'] = li[1]
            tempdict['release'] = int(li[2])
            tempdict['feature'] = li[3]
            data.append(tempdict)
    return data

def main():
    rows = parse_requirement_file()
    print rows
    #if args.requirement is True:
    add_requirements(rows)

if __name__ == '__main__':
    main()
