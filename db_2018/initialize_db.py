from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
 
Base = declarative_base()


class Requirement_Summary(Base):
    """Class representation to map requirements and category"""
    __tablename__ = 'req_summary'
    requirement_id = Column(String(20), primary_key=True)
    category = Column(String(10), nullable=False)
    release = Column(String(20), nullable=False)
    feature = Column(String(20), nullable=False)


class Requirement_Stats(Base):
    """Class representation for requirement IDs"""
    __tablename__ = 'req_stats'
    id = Column(Integer, primary_key=True)
    requirement_id = Column(String(100), ForeignKey('req_summary.requirement_id'))
    req_summary = relationship(Requirement_Summary)
    total_pass = Column(Integer, nullable=False)
    total_fail = Column(Integer, nullable=False)
    release = Column(String(20), nullable=False)



class TestSuiteResult(Base):
    """Table created to hold individual test case results"""
    __tablename__ = 'test_suite_results'
    # Here we define columns for individual test suite level result
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    test_id = Column(String(100))
    test_result = Column(String(10), nullable=False)
    test_suite = Column(String(50), nullable=False)
    requirement = Column(String(50), nullable=False)
    release = Column(String(20), nullable=False)
    config = Column(String(20), nullable=False)


class RegressionResult(Base):
    '''Table created to hold cummulative results'''
    __tablename__ = 'statistics'
    id = Column(Integer, primary_key=True)
    release = Column(String(20))
    total_pass = Column(Integer, nullable=False)
    total_fail = Column(Integer, nullable=False)
    config = Column(String(20), nullable=False)


class SuiteStatistics(Base):
    '''Table created to hold suite level statistics'''
    __tablename__ = 'suite_stats'
    id = Column(Integer, primary_key=True)
    release = Column(String(20))
    suite = Column(String(50), nullable=False)
    total_pass = Column(Integer)
    total_fail = Column(Integer)


class PBISummary(Base):
    """Table created to hold defect summary from JIRA"""
    __tablename__ = 'pbi_summary'
    id = Column(Integer, primary_key=True)
    release = Column(String(20))
    pbi_id = Column(String(20))
    pbi_status = Column(String(20))
    severity = Column(String(10))
    priority = Column(String(10))
    original_estimate = Column(Integer)
    logged_estimate = Column(Integer)
    issue_type = Column(String(20))

class DefectStats(Base):
    """Table created to hold defect statistics from test result"""
    __tablename__ = 'defect_stats'
    release = Column(String(20))
    id = Column(Integer, primary_key=True)
    defect_id = Column(String(20))
    total_fail = Column(Integer, nullable=False)



class CodeCoverage(Base):
    """Table created to hold code coverage statistics"""
    __tablename__ = 'code_coverage'
    release = Column(Integer,primary_key=True)
    line_coverage = Column(Float, nullable=False)
    func_coverage = Column(Float, nullable=False)



class Productivity(Base):
    """Table craeted to find the sprint productivity"""
    __tablename__ = 'productivity'
    id = Column(Integer, primary_key=True)
    release = Column(Integer)
    pbi_id = Column(String(20))
    label = Column(String(20))
    logged_hours = Column(Integer)
    count = Column(Integer)
    epic = Column(String(20))
# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
engine = create_engine('sqlite:///analytics.db')
 
# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)

