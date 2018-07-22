import xlrd
from DB_Writer import add_pbi_summary
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
            tempdict['release'] = li [7]
            tempdict['pbi_id'] = li[0]
            tempdict['pbi_status'] = li[1]
            tempdict['severity'] = li[2]
            tempdict['priority'] = li[3]
            tempdict['original_estimate'] = li[4]
            tempdict['logged_estimate'] = li[5]
            tempdict['issue_type'] = li[6]
            data.append(tempdict)
    return data

def main():
    rows = parse_requirement_file()
    print rows
    #if args.defect is True:
    add_pbi_summary(rows)

if __name__ == '__main__':
    main()