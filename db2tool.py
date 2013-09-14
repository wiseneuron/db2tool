#!/usr/bin/python
#  db2 tool
# author Chunhui Li wiseneuron@gmail.com

import sys
import DB2
import os
from path import *
class DB2Tool:
    def __init__(self, dbname, schema, userid, password, root):
              self.connection = DB2.connect(dsn=dbname,uid=userid,pwd=password)
              self.dbname = dbname
              self.schema = schema.upper()
              self.userid = userid
              self.password = password
              self.tables = []
              self.__getTableNames()
              self.views = []
              self.__getViewNames()
              self.root = root
          # get table names
    def __getTableNames(self):
             cs = self.connection.cursor()
             cs.execute('select tabname from syscat.keycoluse where tabschema=' + "'" + self.schema + "'")
             for row in cs.fetchall():
                 self.tables.append(row[0])
    #get views' name
    def __getViewNames(self):             
             cs = self.connection.cursor()
             cs.execute('select viewname from syscat.views where viewschema=' + "'" + self.schema + "'")
             for row in cs.fetchall():
                 self.views.append(row[0])
    # generate sql for exporting given table data as ixf format.
    def gen_export_table_sql(self, tablename):
        pathData = self.root + "/data/"
        pathLog = self.root + "/log/"
        expcmd = "export to " + "'" + pathData + tablename + ".ixf'" + " of ixf messages '" + pathLog + tablename + ".log'" + " select * from " + self.schema + "." + tablename + ";"
        return expcmd
    # generate sql for exporting given tables data as ixf format.
    def gen_export_tables_sql(self, tablenames,sqlfileName):
        outputFile = self.root + "/sql/" + sqlfileName + ".sql"
        f = open(outputFile,'w')
        idx = 1
        comment = ''
        connectStatement = "CONNECT TO " + self.dbname + " user " + self.userid + " using " + self.password + ";\n"
        f.writelines(connectStatement)
        for tbl in tablenames:
            comment = '--' + str(idx) + ' export datas in ' + tbl + ' as ixf format.\n'
            expcmd = self.gen_export_table_sql(tbl) + "\n"
            unisql = comment + expcmd
            f.writelines(unisql)
            idx = idx + 1
        f.close()
    #generate sql for exporting all tables in given schema as ixf format.
    def gen_export_all_tables_sql(self,sqlfileName):
        self.gen_export_tables_sql(self.tables, sqlfileName)
    #generate sql for importing given ixf formated data where file name is the same to table name into given table.
    def gen_import_table_sql(self, tablename):
        pathData = self.root + "/data/"
        pathLog = self.root + "/log/"
        impcmd = "import from " + "'" + pathData + tablename + ".ixf'" + " of ixf messages '" + pathLog + tablename + ".log'" + " insert into " + self.schema + "." + tablename + ";"
        return impcmd
    #generate sql for importing given ixf formated data where file name is the same to table name into given tables.
    def gen_import_tables_sql(self, tablenames,sqlfileName):
        outputFile = self.root + "/sql/" + sqlfileName + ".sql"
        f = open(outputFile,'w')
        idx = 1
        comment = ''
        connectStatement = "CONNECT TO " + self.dbname + " user " + self.userid + " using " + self.password + ";\n"
        f.writelines(connectStatement)
        for tbl in tablenames:
            comment = '--' + str(idx) + ' import datas into ' + tbl + '.\n'
            expcmd = self.gen_import_table_sql(tbl) + "\n"
            unisql = comment + expcmd
            f.writelines(unisql)
            idx = idx + 1
        f.close()
    #generate sql for exporting all tables in given schema as ixf format.
    def gen_import_all_tables_sql(self,fileName):
        self.gen_import_tables_sql(self.tables, fileName)
    # get ddl of the database
    def get_ddl(self):
        ddlfile = self.root + "/ddl/" + self.dbname + "_" + self.schema + ".ddl"
        db2look = "db2look -d " + self.dbname + " -e -a -x -i " + self.userid + " -w " + self.password + " -o " + ddlfile
        os.system(db2look)
if __name__ == "__main__":
     if sys.argv[1:]:
               root = path(sys)
               db = sys.argv[1]
               schema = sys.argv[2]
               userid = sys.argv[3]
               password = sys.argv[4]
               #create a DB2Tool object.
               db2tool = DB2Tool(db, schema, userid,password,root)

               #generate sql used to export table data. sql file:
               #print db2tool.gen_export_table_sql('table_to_export_data')
               
               #generate sql to export all tables. file is  ./sql/exportAllSql.sql
               #db2tool.gen_export_all_tables_sql('exportAllSql')
               
               #generate sql to import data to table.
               #print db2tool.gen_import_table_sql('table_to_import_data')
               
               #generate sql to import datal to table. file is ./sql/importAllSql.sql
               #db2tool.gen_import_all_tables_sql('importAllSql')
               
               #generate ddl of the db's schema. file is ./ddl/<schema>.ddl
               #db2tool.get_ddl()
               
