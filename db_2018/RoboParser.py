import xml.etree.cElementTree as ET
import os
from DB_Writer import *
from argparse import ArgumentParser

in_stat = False
in_suite = False
parser = ArgumentParser()
parser.add_argument('--release', required=True, metavar='\b', help='Sprint Number or release version')
parser.add_argument('--configuration', required=True, metavar='\b', help='Platform or test execution configuration')
parser.add_argument('--overwrite', default=False, type=bool, metavar='\b', help='Overwrite existing results with new one. valid options: 0/1')
parser.add_argument('--file', required=True, metavar='\b', help='Robot output.xml filename')
args = parser.parse_args()


def parse_suite_stats(node):
    """Method to extract suite level results from statistics element of robot output.xml file"""
    suite_rows = []
    for stat in iter(node):
        if stat.get('name') == args.configuration:
            next
        else:
            suite_dict = {'release': args.release,'config': args.configuration}
            suite_dict['suite'] = stat.get('name')
            suite_dict['total_pass'], suite_dict['total_fail'] = (stat.get('pass'), stat.get('fail'))
            suite_rows.append(suite_dict)

    return suite_rows

def parse_req_stats(node):
    """Method to extract test results based on requirements from statistics element of robot output.xml file"""
    req_rows = []
    for stat in iter(node):
        req_dict = {'release': args.release,'config': args.configuration}
        if 'req_' in stat.text:
            req_dict['req_id'], req_dict['total_pass'], req_dict['total_fail'] = (stat.text, stat.get('pass'), stat.get('fail'))
            req_rows.append(req_dict)

    return req_rows


def parse_defect_stats(node):
    defect_rows = []
    for stat in iter(node):
        defect_dict = {'release': args.release,'config': args.configuration}
        if 'RC18' in stat.text:
            defect_dict['defect_id'],  defect_dict['total_fail'] = (stat.text,  stat.get('fail'))
            defect_rows.append(defect_dict)

    return defect_rows


def parse_total_stats(node):
    """Method to extract cumulative results from statistics element of robot output.xml file"""
    totalstats_rows = []
    for stat in iter(node):
        totalstats_dict = {'release': args.release ,'config': args.configuration}
        totalstats_dict['total_pass'], totalstats_dict['total_fail'] = (stat.get('pass'), stat.get('fail'))
        totalstats_rows.append(totalstats_dict)
        break
    return totalstats_rows


def parse_requirement(tag):
    """Method to extract requirement from each test case"""
    for element in iter(tag):
        #if element.text == 'Sanity' or element.text == 'Regression':
        return element.text
    return "Sanity"


def parse_test(test):
    """Method to extract test id and status from each test case element in robot output.xml file"""
    status = test.find('.status')
    test_req = parse_requirement(test.find('.tags'))
    # print suite_name + ": " + test.get('name') + ":" + status.get('status') + ":" + test_req
    return test.get('name'), status.get('status'), test_req


def parse_suite(node):
    """Method to extract all test cases and parse suite wise test results from robot output.xml file"""
    test_rows = []
    suite_name = node.get('name')
    tests = node.iterfind('test')
    for test in tests:
        test_dict = {'release': args.release ,'config': args.configuration}
        test_stats = parse_test(test)
        test_dict['test_id'], test_dict['test_result'], test_dict['requirement'] = [element for element in test_stats]
        test_dict['test_suite'] = suite_name
        test_rows.append(test_dict)

    return test_rows


def parse_robot_results():
    """Main method invoked to parse robot output.xml file element by element incrementally and extract \n
       the required statistics and upload it to sqlite database"""
    global in_suite, in_stat
    for event, element in ET.iterparse(args.file, events=('start', 'end')):
        if event == 'end' and element.tag == 'suite' and element.get('name') != args.configuration and in_stat is not True:
            suite_elements = parse_suite(element)
            if suite_elements is not None and any(suite_elements):
                add_test_suite_result(suite_elements)
            # for suite in suite_elements:
            #     print suite
            element.clear()

        elif event == 'start' and element.tag == 'statistics':
            in_stat = True

        elif event == 'end' and element.tag == 'statistics':
            suite_stat_rows = parse_suite_stats(element.find('.suite'))
            if suite_stat_rows is not None and any(suite_stat_rows):
                add_suite_stats(suite_stat_rows)
            req_stat_rows = parse_req_stats(element.find('.tag'))
            add_requirements_stats(req_stat_rows)
            defect_stat_rows = parse_defect_stats(element.find('.tag'))
            add_defect_stats(defect_stat_rows)
            total_stats_rows = parse_total_stats(element.find('.total'))
            add_regression_result(total_stats_rows)
            element.clear()
            in_stat = False

        # elif event == 'end' and element.tag != 'statistics' and in_suite is False:
        #     element.clear()


def main():
    presence = check_duplicate(args.release, args.configuration)
    if presence is True and args.overwrite is True:
        print("In overwriting mode")
        delete_entry(args.release, args.configuration)
        parse_robot_results()
    elif presence is True and args.overwrite is False:
        print("ERROR: Database already present. Resume after enabling overwrite option")
        os.system("'1' > error.txt")
    else:
        parse_robot_results()
        print("Completed populating Database for %s with %s Configuration" % (args.release, args.configuration))

main()
