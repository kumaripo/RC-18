from sqlalchemy.orm import sessionmaker
from flask import Flask, render_template
from sqlalchemy import *
from initialize_db import Base, Requirement_Summary, Requirement_Stats, TestSuiteResult, SuiteStatistics, RegressionResult, DefectStats, PBISummary, CodeCoverage, Productivity
app = Flask(__name__,static_url_path='/static')
engine = create_engine('sqlite:///analytics.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


def add_test_suite_result(rows):
    """Method to populate test suite result table having following columns\n
        test_id, test_result, test_suite, requirement, sprint, config\n
        argument to this method should be list of dictionaries with each dictionary having column names as the keys\n"""
    global engine
    try:
        engine.execute(TestSuiteResult.__table__.insert(), rows)
    except:
        return render_template('error.html')


def add_requirements(rows):
    """Method to populate requirement summary table having following columns\n
        requirement_id, sprint, category\n
        argument to this method should be list of dictionaries with each dictionary having column names as the keys\n"""
    global engine
    engine.execute(Requirement_Summary.__table__.delete())
    engine.execute(Requirement_Summary.__table__.insert(), rows)



def add_requirements_stats(rows):
    """Method to populate requirement statistics table having following columns\n
        requirement_id, total_pass, total_fail, sprint, config\n
        argument to this method should be list of dictionaries with each dictionary having column names as the keys\n"""
    global engine
    print (rows)
    id_select = select([Requirement_Summary.__table__.c.requirement_id]).where(Requirement_Summary.__table__.c.requirement_id == bindparam('req_id'))
    insert = Requirement_Stats.__table__.insert({'requirement_id': id_select})
    engine.execute(insert, rows)


def add_defect_stats(rows):
    """Method to populate defect statistics table having following columns\n
        requirement_id, total_pass, total_fail, sprint, config\n
        argument to this method should be list of dictionaries with each dictionary having column names as the keys\n"""
    global engine
    engine.execute(DefectStats.__table__.insert(), rows)

def add_pbi_summary(rows):
    """Method to populate defect statistics table having following columns\n
        pbi_id, total_pass, total_fail, sprint, config\n
        argument to this method should be list of dictionaries with each dictionary having column names as the keys\n"""
    global engine
    engine.execute(PBISummary.__table__.delete())
    engine.execute(PBISummary.__table__.insert(), rows)

def add_productivity(rows):
    """Method to populate defect statistics table having following columns\n
        pbi_id, total_pass, total_fail, sprint, config\n
        argument to this method should be list of dictionaries with each dictionary having column names as the keys\n"""
    global engine
    engine.execute(Productivity.__table__.delete())
    engine.execute(Productivity.__table__.insert(), rows)


def add_suite_stats(rows):
    """Method to populate test suite statistics table having following columns\n
        suite, total_pass, total_fail, sprint, config\n
        argument to this method should be list of dictionaries with each dictionary having column names as the keys\n"""
    global engine
    engine.execute(SuiteStatistics.__table__.insert(), rows)

def add_regression_result(rows):
    """Method to populate Regression results table having following columns\n
        total_pass, total_fail, sprint, config\n
        argument to this method should be list of dictionaries with each dictionary having column names as the keys\n"""
    global engine
    engine.execute(RegressionResult.__table__.insert(), rows)

def add_code_coverage(rows):
    """Method to populate code coverage results having following columns\n
        release, config, line_coverage, func_coverage\n
        argument to this method should be list of dictionaries with each dictionary having column names as the keys\n"""
    global engine
    engine.execute(CodeCoverage.__table__.delete())
    engine.execute(CodeCoverage.__table__.insert(), rows)

def add_sloc(rows):
    """Method to populate code coverage results having following columns\n
        release, sloc\n
        argument to this method should be list of dictionaries with each dictionary having column names as the keys\n"""
    global engine
    engine.execute(Sloc.__table__.insert(), rows)

def delete_entry(rel_id, config_id):
    """Method to delete database entry of specified release and config"""
    global engine
    tables = ['req_stats', 'test_suite_results', 'statistics', 'suite_stats', 'defect_stats']
    for name in tables:
        meta = MetaData(engine, reflect=True)
        table_name = meta.tables[name]
        #delete_st = table_name.delete().where(table_name.c.release == rel_id).where(table_name.c.config == config_id)
        delete_st = table_name.delete().where(table_name.c.release == rel_id)
        engine.execute(delete_st)


def check_duplicate(rel_id, config_id):
    """Method to avoid duplicate entry of results without override option"""
    global engine
    query = text("SELECT release, config FROM statistics WHERE statistics.release == :x AND statistics.config == :y")
    query_result = engine.execute(query, x=rel_id, y=config_id).fetchall()
    if any(query_result):
        return True
    else:
        return False

