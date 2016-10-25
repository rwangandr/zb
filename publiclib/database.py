__author__ = 'carl'

import logging
import logging.config
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, MetaData, desc
from sqlalchemy.dialects.mysql import INTEGER, CHAR, VARCHAR, SMALLINT, TEXT, TIME
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import myglobal


class database:
    def __init__(self):
        logging.config.fileConfig(myglobal.LOGGINGINI)
        self.__logger = logging.getLogger('database')
        self.__mysql_engine = None
        self.__session = None

    def initDB(self, host, user, pwd, db, port):
        DB_CONN_STR = 'mysql://%s:%s@%s:%s/%s' % (user, pwd, host, port, db)
        # DB_CONN_STR='mysql://%s:%s@%s:%i/%s?charset=utf8'%(self.__user,self.__passwd,self.__host,self.__port,self.__db)
        self.__logger.debug("Connect database: %s" % DB_CONN_STR)
        try:
            self.__mysql_engine = create_engine(DB_CONN_STR, echo=False)
            return True
        except Exception, e:
            self.__logger.error("Create DB engine failed: %s" % e.message)
            return False

    def __startSession(self):
        try:
            Session = sessionmaker(bind=self.__mysql_engine)
            self.__session = Session()
            self.__logger.debug("New session setup.")
        except Exception, e:
            self.__logger.error("Start Session failed: %s" % e.message)

    def __closeSession(self):
        if self.__session:
            self.__session.close()
            self.__logger.debug("Session is closed.")

    Base = declarative_base()

    class TotalResults(Base):
        __tablename__ = 'TotalResults'
        id = Column(INTEGER, primary_key=True, autoincrement=True)
        component = Column(CHAR(50), nullable=False)
        line = Column(VARCHAR(20))
        build = Column(VARCHAR(50), nullable=False)
        category = Column(VARCHAR(25))
        time = Column(CHAR(18), nullable=False)
        total_num = Column(SMALLINT, nullable=False)
        pass_num = Column(SMALLINT, nullable=False)
        fail_num = Column(SMALLINT, nullable=False)
        na_num = Column(SMALLINT)
        block_num = Column(SMALLINT)
        startTime = Column(CHAR(25), nullable=False)
        endTime = Column(CHAR(25), nullable=False)
        duration = Column(TIME, nullable=False)
        status = Column(VARCHAR(50))

    class RoundMapping(Base):
        __tablename__ = 'RoundMapping'
        roundId = Column(CHAR(30), primary_key=True)
        component = Column(CHAR(50))
        build = Column(VARCHAR(50))
        time = Column(VARCHAR(18))
        type = Column(VARCHAR(40))
        version = Column(VARCHAR(50))
        db = Column(VARCHAR(25))
        errorMessage = Column(TEXT)

    class DetailedResults(Base):
        __tablename__ = 'DetailedResults'
        id = Column(INTEGER, primary_key=True, autoincrement=True)
        component = Column(CHAR(50), nullable=False)
        roundId = Column(CHAR(30), nullable=False)
        layer = Column(SMALLINT, nullable=False)
        casePriority = Column(CHAR(8))
        caseId = Column(VARCHAR(20))
        caseTitle = Column(VARCHAR(250))
        result = Column(CHAR(8))
        startTime = Column(CHAR(25))
        endTime = Column(CHAR(25))
        elapsed = Column(CHAR(10))
        runTime = Column(INTEGER)

    class TestServers(Base):
        __tablename__ = 'TestServers'
        id = Column(INTEGER, primary_key=True, autoincrement=True)
        component = Column(CHAR(15))
        server = Column(VARCHAR(30))
        status = Column(SMALLINT)

    class LPB(Base):
        __tablename__ = 'LPB'
        id = Column(INTEGER, primary_key=True, autoincrement=True)
        component = Column(CHAR(50))
        individual_ltb = Column(VARCHAR(50))
        individual_lpb = Column(VARCHAR(50))
        integrated_ltb = Column(VARCHAR(50))
        integrated_lpb = Column(VARCHAR(50))
        nightly_ltb = Column(VARCHAR(50))

    class BuildTracker(Base):
        __tablename__ = 'BuildTracker'
        id = Column(INTEGER, primary_key=True, autoincrement=True)
        component = Column(CHAR(50), nullable=False)
        build = Column(VARCHAR(50), nullable=False)
        individual_smoke = Column(VARCHAR(50))
        individual_validation = Column(VARCHAR(50))
        integration_combination = Column(VARCHAR(50))
        integrated_smoke = Column(VARCHAR(50))
        integrated_validation = Column(VARCHAR(50))

    def totalResultsInsert(self, item):
        try:
            self.__startSession()
            total_result = self.TotalResults()
            total_result.component = item.component
            total_result.line = item.line
            total_result.build = item.build
            total_result.time = item.time
            total_result.category = item.category
            total_result.total_num = item.total_num
            total_result.pass_num = item.pass_num
            total_result.fail_num = item.fail_num
            total_result.na_num = item.na_num
            total_result.block_num = item.block_num
            total_result.startTime = item.startTime
            total_result.endTime = item.endTime
            total_result.duration = item.duration
            total_result.status = item.status
            self.__session.add(total_result)
            self.__session.flush()
            self.__session.commit()
            self.__logger.info("One entry had been inserted into TotalResults table.")
        except Exception, e:
            # print e.message
            self.__logger.error("Insert TotalResult failed: %s" % e.message)
        finally:
            self.__closeSession()

    def totalResultQuery(self):
        try:
            self.__startSession()
            return self.__session.query(self.TotalResults).order_by(self.TotalResults.id.desc()).first()
        except Exception, e:
            # print e.message
            self.__logger.error("Query TotalResult failed: %s" % e.message)
        finally:
            self.__closeSession()

    def totalResultQueryLPB(self, component):
        try:
            self.__startSession()
            all_pass = "All tests passed"
            category = 'Buildly'
            return self.__session.query(self.TotalResults).filter_by(component=component).filter_by(
                category=category).filter_by(status=all_pass).order_by(self.TotalResults.id.desc()).first().build
        except Exception, e:
            # print e.message
            self.__logger.error("Query EndToEndResults failed: %s" % e.message)
        finally:
            self.__closeSession()

    def totalResultQueryLatestMatchBuild(self, component, category, status):
        try:
            self.__startSession()
            return self.__session.query(self.TotalResults).filter_by(component=component).filter_by(
                category=category).filter_by(status=status).order_by(self.TotalResults.id.desc()).first().build
        except Exception, e:
            # print e.message
            self.__logger.error("Query EndToEndResults failed: %s" % e.message)
        finally:
            self.__closeSession()

    def totalResultQueryStatus(self, component, build, category):
        try:
            self.__startSession()
            return self.__session.query(self.TotalResults).filter_by(component=component).filter_by(
                build=build).filter_by(category=category).order_by(self.TotalResults.id.desc()).first().status
        except Exception, e:
            # print e.message
            self.__logger.error("Query EndToEndResults status failed: %s" % e.message)
        finally:
            self.__closeSession()

    def totalResultQueryItems(self, component, category):
        try:
            self.__startSession()
            return self.__session.query(self.TotalResults).filter_by(component=component).filter_by(
                category=category).all()
        except Exception, e:
            # print e.message
            self.__logger.error("Query EndToEndResults status failed: %s" % e.message)
        finally:
            self.__closeSession()

    def roundMappingInsert(self, item):
        try:
            self.__startSession()
            round_mapping = self.RoundMapping()
            round_mapping.roundId = item.roundId
            round_mapping.component = item.component
            round_mapping.build = item.build
            round_mapping.time = item.time
            round_mapping.type = item.type
            round_mapping.version = item.version
            round_mapping.db = item.db
            round_mapping.errorMessage = item.errorMessage
            self.__session.add(round_mapping)
            self.__session.flush()
            self.__session.commit()
            self.__logger.info("One entry had been inserted into RoundMapping table.")
        except Exception, e:
            # print e.message
            self.__logger.error("Insert RoundMapping failed: %s" % e.message)
        finally:
            self.__closeSession()

    def roundMappingQuery(self, roundId):
        entry = None
        try:
            self.__startSession()
            if self.__session.query(self.RoundMapping).filter_by(roundId=roundId).count() > 0:
                entry = self.__session.query(self.RoundMapping).filter_by(roundId=roundId).one()
        except Exception, e:
            # print e.message
            self.__logger.error("Query RoundMapping failed: %s" % e.message)
        finally:
            self.__closeSession()
            return entry

    def roundMappingUpdate(self, item):
        entry = None
        try:
            self.__startSession()
            entry = self.__session.query(self.RoundMapping).filter_by(roundId=item.roundId)
            entry.update({self.RoundMapping.component: item.component})
            entry.update({self.RoundMapping.build: item.build})
            entry.update({self.RoundMapping.time: item.time})
            entry.update({self.RoundMapping.type: item.type})
            entry.update({self.RoundMapping.version: item.version})
            entry.update({self.RoundMapping.db: item.db})
            entry.update({self.RoundMapping.errorMessage: item.errorMessage})
            self.__session.flush()
            self.__session.commit()
            self.__logger.info("One entry had been updated to RoundMapping table.")
        except Exception, e:
            # print e.message
            self.__logger.error("Update RoundMapping failed: %s" % e.message)
        finally:
            self.__closeSession()

    def roundMappingJobStatusUpdate(self, item):
        entry = None
        try:
            self.__startSession()
            entry = self.__session.query(self.RoundMapping).filter_by(roundId=item.roundId)
            entry.update({self.RoundMapping.errorMessage: item.errorMessage})
            self.__session.flush()
            self.__session.commit()
            self.__logger.info("One entry had been updated to RoundMapping table.")
        except Exception, e:
            # print e.message
            self.__logger.error("Update RoundMapping failed: %s" % e.message)
        finally:
            self.__closeSession()

    def detailedResultsInsert(self, item_list):
        try:
            self.__startSession()
            for item in item_list:
                d_results = self.DetailedResults()
                d_results.component = item.component
                d_results.roundId = item.roundId
                d_results.layer = item.layer
                d_results.casePriority = item.casePriority
                d_results.caseId = item.caseId
                d_results.caseTitle = item.caseTitle
                d_results.result = item.result
                d_results.startTime = item.startTime
                d_results.endTime = item.endTime
                d_results.elapsed = item.elapsed
                d_results.runTime = item.runTime
                self.__session.add(d_results)
            self.__session.flush()
            self.__session.commit()
            self.__logger.info("%i entry had been inserted into Detailed Result table." % (len(item_list)))
        except Exception, e:
            self.__logger.error("Insert Detailed Result failed: %s" % e.message)
        finally:
            self.__closeSession()

    def detailedResultsQuery(self, component, roundId):
        try:
            self.__startSession()
            items = self.__session.query(self.DetailedResults).filter_by(component=component).filter_by(
                roundId=roundId).all()
        except Exception, e:
            # print e.message
            self.__logger.error("Query Detailed Result failed: %s" % e.message)
        finally:
            self.__closeSession()
            return items

    def detailedResultsQueryByComp(self, component):
        try:
            self.__startSession()
            items = self.__session.query(self.DetailedResults).filter_by(component=component).all()
        except Exception, e:
            # print e.message
            self.__logger.error("Query Detailed Result failed: %s" % e.message)
        finally:
            self.__closeSession()
            return items

    def detailedResultsDelete(self, item_list):
        try:
            self.__startSession()
            if len(item_list):
                for item in item_list:
                    self.__session.delete(item)
                self.__session.flush()
                self.__session.commit()
        except Exception, e:
            self.__logger.error("Delete Detailed Result failed: %s" % e.message)
        finally:
            self.__closeSession()

    def testServerInsert(self, item):
        try:
            self.__startSession()

            test_server = self.TestServers()
            test_server.component = item.component
            test_server.server = item.server
            test_server.status = item.status
            self.__session.add(test_server)
            self.__session.flush()
            self.__session.commit()
            self.__logger.info("%s had been inserted into TestServer table." % item.component)
        except Exception, e:
            # print e.message
            self.__logger.error("Insert TestServer failed: %s" % e.message)
        finally:
            self.__closeSession()

    def testServerStatusQuery(self, component):
        status = 2
        try:
            self.__startSession()
            status = self.__session.query(self.TestServers).filter_by(component=component).one().status
        except Exception, e:
            # print e.message
            self.__logger.error("Query TestServer failed: %s" % e.message)
        finally:
            self.__closeSession()
            return status

    def testServerStatusUpdate(self, component, testServer, status):
        rt = 0
        try:
            self.__startSession()
            rt = self.__session.query(self.TestServers).filter_by(server=testServer, component=component).update(
                {"status": status})
            if rt == 1:
                rt = self.__session.query(self.TestServers).filter_by(server=testServer).update({"status": status})
            # print testServer, rt
            self.__session.flush()
            self.__session.commit()
        except Exception, e:
            # print e.message
            self.__logger.error("Update TestServer status failed: %s" % e.message)
        finally:
            self.__closeSession()

        if rt > 0:
            self.__logger.info("Test Server %s is set to %s" % (testServer, status))
            return True
        else:
            self.__logger.error("Failed to set Test Server %s status" % testServer)
            return False

    def totalResultQueryLatest(self, component):
        try:
            self.__startSession()
            return self.__session.query(self.TotalResults).filter_by(component=component).order_by(
                self.TotalResults.id.desc()).first()
        except Exception, e:
            # print e.message
            self.__logger.error("Query TotalResult failed: %s" % e.message)
        finally:
            self.__closeSession()

    def reportTotalResultsAll(self):
        try:
            self.__startSession()
            return self.__session.query(self.TotalResults).order_by(self.TotalResults.id)
        except Exception, e:
            # print e.message
            self.__logger.error("Query TotalResult failed: %s" % e.message)
        finally:
            self.__closeSession()

    def reportTotalResults(self, component):
        try:
            self.__startSession()
            return self.__session.query(self.TotalResults).filter_by(component=component).order_by(self.TotalResults.id)
        except Exception, e:
            # print e.message
            self.__logger.error("Query TotalResult failed: %s" % e.message)
        finally:
            self.__closeSession()

    def LPBInsert(self, component):
        try:
            if not self.__session:
                self.__startSession()
            lpb = self.LPB()
            lpb.component = component
            lpb.individual_lpb = ""
            lpb.individual_ltb = ""
            lpb.integrated_lpb = ""
            lpb.integrated_ltb = ""
            lpb.nightly_ltb = ""

            self.__session.add(lpb)
            self.__session.flush()
            self.__session.commit()
            self.__logger.info("%s had been inserted into LPB table." % component)
        except Exception, e:
            # print e.message
            self.__logger.error("Insert LPB failed: %s" % e.message)
        finally:
            self.__closeSession()

    def lpbIndividualLTBUpdate(self, component, build):
        try:
            self.__startSession()
            result = self.__session.query(self.LPB).filter_by(component=component).count()
            if result == 0:
                self.LPBInsert(component)
            rt = self.__session.query(self.LPB).filter_by(component=component).update({"individual_ltb": build})
            self.__session.flush()
            self.__session.commit()

        except Exception, e:
            # print e.message
            self.__logger.error("Update individual LTBs status failed: %s" % e.message)
            rt = 0
        finally:
            self.__closeSession()

        if rt > 0:
            self.__logger.info("%s individual LTB had been set to %s" % (component.upper(), build))
            return True
        else:
            self.__logger.error("Failed to set %s individual LTB" % component.upper())
            return False

    def lpbIndividualLTBQuery(self, component):
        build = 0
        try:
            self.__startSession()
            build = int(self.__session.query(self.LPB).filter_by(component=component).one().individual_ltb)
            self.__logger.info("Query %s individual LTB is %i" % (component, build))
        except Exception, e:
            # print e.message
            self.__logger.error("Query individual LTB failed: %s" % e.message)
        finally:
            self.__closeSession()
            return build

    def lpbIndividualLPBUpdate(self, component, build):
        try:
            self.__startSession()
            result = self.__session.query(self.LPB).filter_by(component=component).count()
            if result == 0:
                self.LPBInsert(component)
            rt = self.__session.query(self.LPB).filter_by(component=component).update({"individual_lpb": build})
            self.__session.flush()
            self.__session.commit()

        except Exception, e:
            # print e.message
            self.__logger.error("Update individual LPBs status failed: %s" % e.message)
            rt = 0
        finally:
            self.__closeSession()

        if rt > 0:
            self.__logger.info("%s individual LPB had been set to %s" % (component.upper(), build))
            return True
        else:
            self.__logger.error("Failed to set %s individual LPB" % component.upper())
            return False

    def lpbIndividualLPBQuery(self, component):
        build = 0
        try:
            self.__startSession()
            build = int(self.__session.query(self.LPB).filter_by(component=component).one().individual_lpb)
            self.__logger.info("Query %s individual LPB is %i" % (component, build))
        except Exception, e:
            # print e.message
            self.__logger.error("Query individual LPB failed: %s" % e.message)
        finally:
            self.__closeSession()
            return build

    def lpbNightlyLTBUpdate(self, component, build):
        try:
            self.__startSession()
            result = self.__session.query(self.LPB).filter_by(component=component).count()
            if result == 0:
                self.LPBInsert(component)
            rt = self.__session.query(self.LPB).filter_by(component=component).update({"nightly_ltb": build})
            self.__session.flush()
            self.__session.commit()

        except Exception, e:
            # print e.message
            self.__logger.error("Update nightly LTB status failed: %s" % e.message)
            rt = 0
        finally:
            self.__closeSession()

        if rt > 0:
            self.__logger.info("%s nightly LTB had been set to %s" % (component.upper(), build))
            return True
        else:
            self.__logger.error("Failed to set %s nightly LTB" % component.upper())
            return False

    def lpbNightlyLTBQuery(self, component):
        build = 0
        try:
            self.__startSession()
            build = int(self.__session.query(self.LPB).filter_by(component=component).one().nightly_ltb)
            self.__logger.info("Query %s nightly LTB is %i" % (component, build))
        except Exception, e:
            # print e.message
            self.__logger.error("Query nightly LTB failed: %s" % e.message)
        finally:
            self.__closeSession()
            return build

    '''
    def lpbIntegratedLPBQuery(self, component):
        build = 0
        try:
            self.__startSession()
            build = int(self.__session.query(self.LPB).filter_by(component=component).one().integrated_lpb)
            self.__logger.info("Query %s individual LPB is %i" % (component, build))
        except Exception, e:
            # print e.message
            self.__logger.error("Query individual LPB failed: %s" % e.message)
        finally:
            self.__closeSession()
            return build

    def lpbIntegratedLPBQueryAll(self):
        iBuild = aBuild = mBuild = xBuild = nBuild = 0
        try:
            self.__startSession()
            iBuild = int(self.__session.query(self.LPB).filter_by(component="bmci").one().integrated_lpb)
            aBuild = int(self.__session.query(self.LPB).filter_by(component="bmca").one().integrated_lpb)
            mBuild = int(self.__session.query(self.LPB).filter_by(component="bmm").one().integrated_lpb)
            xBuild = int(self.__session.query(self.LPB).filter_by(component="bmx").one().integrated_lpb)
            nBuild = int(self.__session.query(self.LPB).filter_by(component="bmn").one().integrated_lpb)
            self.__logger.debug("Query integrated LPBs are %i-%i-%i-%i-%i" % (iBuild, aBuild, mBuild, xBuild, nBuild))
        except Exception, e:
            # print e.message
            self.__logger.error("Query integrated LPBs failed: %s" % e.message)
        finally:
            self.__closeSession()
            return iBuild, aBuild, mBuild, xBuild, nBuild
    '''

    def lpbIntegratedLPBUpdateAll(self, inte_lpb_com_list, inte_lpb_build_list):
        # component_list = ['bmci', 'bmca', 'bmm', 'bmx', 'bmn']
        rt = 0
        i = 0

        try:
            self.__startSession()
            '''
            for i in range(5):
                self.__session.query(self.LPB).filter_by(component=component_list[i]).update(
                    {"integrated_lpb": str(inte_lpb_list[i])})
                self.__logger.info("%s integrated LPB is %s" % (component_list[i].upper(), str(inte_lpb_list[i])))
            '''
            components = inte_lpb_com_list.split(',')
            builds = inte_lpb_build_list.split(',')

            for component in components:
                result = self.__session.query(self.LPB).filter_by(component=component).count()
                if result == 0:
                    self.LPBInsert(component)
                rt = rt + self.__session.query(self.LPB).filter_by(component=component).update(
                    {"integrated_lpb": str(builds[i])})
                i = i + 1
            self.__session.flush()
            self.__session.commit()
            self.__logger.info("Integrated LPB had been updated")
        except Exception, e:
            # print e.message
            self.__logger.error("Update integrated LPBs status failed: %s" % e.message)
            rt = 0
        finally:
            self.__closeSession()

        if rt == i:
            self.__logger.info("%s integrated LPB is %s" % (inte_lpb_com_list, inte_lpb_build_list))
            return True
        else:
            self.__logger.error("Failed to set %s integrated LPB" % inte_lpb_com_list)
            return False

    def lpbIntegratedLTBQuery(self, component):
        build = 0
        try:
            self.__startSession()
            build = int(self.__session.query(self.LPB).filter_by(component=component).one().integrated_ltb)
            self.__logger.info("Query %s integration LTB is %i" % (component, build))
        except Exception, e:
            # print e.message
            self.__logger.error("Query integration LTB failed: %s" % e.message)
        finally:
            self.__closeSession()
            return build

    '''
    def lpbIntegratedLTBQueryAll(self):
        iBuild = aBuild = mBuild = xBuild = nBuild = 0
        try:
            self.__startSession()
            iBuild = int(self.__session.query(self.LPB).filter_by(component="bmci").one().integrated_ltb)
            aBuild = int(self.__session.query(self.LPB).filter_by(component="bmca").one().integrated_ltb)
            mBuild = int(self.__session.query(self.LPB).filter_by(component="bmm").one().integrated_ltb)
            xBuild = int(self.__session.query(self.LPB).filter_by(component="bmx").one().integrated_ltb)
            nBuild = int(self.__session.query(self.LPB).filter_by(component="bmn").one().integrated_ltb)
            self.__logger.debug("Query integrated LTBs are %i-%i-%i-%i-%i" % (iBuild, aBuild, mBuild, xBuild, nBuild))
        except Exception, e:
            # print e.message
            self.__logger.error("Query integrated LTBs failed: %s" % e.message)
        finally:
            self.__closeSession()
            return iBuild, aBuild, mBuild, xBuild, nBuild
    '''

    def lpbIntegratedLTBUpdateAll(self, inte_lpb_com_list, inte_lpb_build_list):
        # component_list = ['bmci', 'bmca', 'bmm', 'bmx', 'bmn']
        i = 0
        rt = 0
        try:
            self.__startSession()
            '''
            for i in range(5):
                self.__session.query(self.LPB).filter_by(component=component_list[i]).update(
                    {"integrated_ltb": str(inte_ltb_list[i])})
                self.__logger.info("%s integrated LTB is %s" % (component_list[i].upper(), str(inte_ltb_list[i])))
            '''
            components = inte_lpb_com_list.split(',')
            builds = inte_lpb_build_list.split(',')
            # print components, builds
            for component in components:
                result = self.__session.query(self.LPB).filter_by(component=component).count()
                if result == 0:
                    self.LPBInsert(component)
                rt = rt + self.__session.query(self.LPB).filter_by(component=component).update(
                    {"integrated_ltb": str(builds[i])})
                i = i + 1
                # print rt
            self.__session.flush()
            self.__session.commit()
            # self.__logger.info("Integrated LTB had been updated")
        except Exception, e:
            # print e.message
            self.__logger.error("Update integrated LTBs status failed: %s" % e.message)
            rt = 0
        finally:
            self.__closeSession()

        if rt != 0 and rt == i:
            self.__logger.info("%s integrated LTB is %s" % (inte_lpb_com_list, inte_lpb_build_list))
            return True
        else:
            self.__logger.error("Failed to set %s integrated LTB" % inte_lpb_com_list)
            return False

    def buildTrackerInsert(self, component, build):
        try:
            self.__startSession()
            build_tracker = self.BuildTracker()
            build_tracker.component = component
            build_tracker.build = build
            self.__session.add(build_tracker)
            self.__session.flush()
            self.__session.commit()
            self.__logger.info("One %s entry with build %s had been inserted into BuildTracker table." % (
                component.upper(), str(build)))
        except Exception, e:
            # print e.message
            self.__logger.error("Insert BuildTracker failed: %s" % e.message)
        finally:
            self.__closeSession()

    def buildTrackerUpdateIndiSmkSts(self, component, build, status):
        try:
            self.__startSession()
            self.__session.query(self.BuildTracker).filter_by(component=component).filter_by(build=build).update(
                {"individual_smoke": status})
            self.__session.flush()
            self.__session.commit()
            self.__logger.info(
                "%s build %s individual smoke status had been set to \'%s\'" % (component.upper(), str(build), status))
        except Exception, e:
            # print e.message
            self.__logger.error("Update %s individual smoke status failed: %s" % (component.upper, e.message))
        finally:
            self.__closeSession()

    def buildTrackerUpdateIndiValSts(self, component, build, status):
        try:
            self.__startSession()
            self.__session.query(self.BuildTracker).filter_by(component=component).filter_by(build=build).update(
                {"individual_validation": status})
            self.__session.flush()
            self.__session.commit()
            self.__logger.info(
                "%s build %s individual validation status had been set to \'%s\'" % (
                    component.upper(), str(build), status))
        except Exception, e:
            # print e.message
            self.__logger.error("Update %s individual validation status failed: %s" % (component.upper, e.message))
        finally:
            self.__closeSession()

    def buildTrackerUpdateInteSmkSts(self, component, build, status):
        try:
            self.__startSession()
            self.__session.query(self.BuildTracker).filter_by(component=component).filter_by(build=build).update(
                {"integrated_smoke": status})
            self.__session.flush()
            self.__session.commit()
            self.__logger.info(
                "%s build %s integrated smoke status had been set to \'%s\'" % (component.upper(), str(build), status))
        except Exception, e:
            # print e.message
            self.__logger.error("Update %s integrated smoke status failed: %s" % (component.upper, e.message))
        finally:
            self.__closeSession()

    def buildTrackerUpdateInteValSts(self, component, build, status):
        try:
            self.__startSession()
            self.__session.query(self.BuildTracker).filter_by(component=component).filter_by(build=build).update(
                {"integrated_validation": status})
            self.__session.flush()
            self.__session.commit()
            self.__logger.info(
                "%s build %s integrated validation status had been set to \'%s\'" % (
                    component.upper(), str(build), status))
        except Exception, e:
            # print e.message
            self.__logger.error("Update %s integrated validation status failed: %s" % (component.upper, e.message))
        finally:
            self.__closeSession()

    def buildTrackerUpdateInteComb(self, component, build, combination_string):
        try:
            self.__startSession()
            self.__session.query(self.BuildTracker).filter_by(component=component).filter_by(build=build).update(
                {"integration_combination": combination_string})
            self.__session.flush()
            self.__session.commit()
            self.__logger.info(
                "%s build %s integration combination had been set to \'%s\'" % (
                    component.upper(), str(build), combination_string))
        except Exception, e:
            # print e.message
            self.__logger.error("Update %s integration combination failed: %s" % (component.upper, e.message))
        finally:
            self.__closeSession()


            # d = database()

# host = "172.16.50.201"
# username = "root"
# password = "111111"
# db = "AutoResults"
# port = 3306
# d.initDB(host, username, password, db, port)
# component = 'bmn'
# build = 60
# d.buildTrackerInsert(component,str(build))
# d.buildTrackerUpdateInteSmkSts(component, build, 'fail')

# component = "bmci"
# category = "Buildly"
# status = "1 critical test failed"
# d.lpbIndividualLPBQueryAll()
# d.lpbIntegratedLPBQueryAll()
# d.lpbIntegratedLTBQueryAll()
# lpb_list = [109, 119, 68, 20, 62]
# d.lpbIntegratedLPBUpdateAll(lpb_list)
# d.lpbIntegratedLTBUpdateAll(lpb_list)

# item=d.EndToEndResults()
# item.category="buildly"
# item.bmci_build=3
# item.bmca_build=4
# item.bmm_build=5
# item.bmx_build=6
# item.bmn_build=8
# item.time="20160127001640234"
# item.startTime="20160127 00:18:40.588"
# item.endTime="20160127 04:06:43.104"
# item.duration="04:50:03"
# item.total_num=33
# item.pass_num=33
# item.fail_num=3
# item.status="3 critical test failed"
# # d.endToEndResultsInsert(item)
# result= d.endToEndResultsQueryLatestPass()
# print result.bmci_build
# print d.totalResultQueryLPB(component)
# print d.totalResultQueryLatestMatchBuild(component,category,status)
