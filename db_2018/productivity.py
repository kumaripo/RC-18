import xlrd
from DB_Writer import add_productivity
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('--file', required=True, metavar='', help='Sprint Number or release version')
#action = parser.add_mutually_exclusive_group(required=True)
parser.add_argument('--release', required=True, metavar='\b', help='Sprint Number or release version')
#action.add_argument('--defect', dest='defect', action='store_true')
#action.set_defaults(code_coverage=False)
args = parser.parse_args()

def parse_requirement_file():
    book = xlrd.open_workbook(args.file)
    first_sheet = book.sheet_by_index(0)
    # read a row
    data = []
    for r in range(1, first_sheet.nrows):
        tempdict = {}
        li = first_sheet.row_values(r)
        if (li[0] != '' and li[1] != '' and li[2] != '' and li[3] != ''):
            tempdict['release'] = li[0]
            tempdict['pbi_id'] = li[1]
            tempdict['label'] = li[2]
            tempdict['logged_hours'] = li[3]
            tempdict['count'] = li[4]
            tempdict['epic'] = li[5]
            data.append(tempdict)
    return data

def main():
    rows = parse_requirement_file()
    print rows
    #if args.defect is True:
    add_productivity(rows)

if __name__ == '__main__':
    main()