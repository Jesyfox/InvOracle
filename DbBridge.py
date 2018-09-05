import sqlite3
from UserInteraktion import writErr, toXlsFile

#miss white

class DbSql(object):

    def __init__(self,DBname):
        self.DBname = DBname
        self.mainTab = '' #need manualy name it!!!
        self.DBpath = "DataBase\\" + DBname + '.db'
        self.openDB()

    def openDB(self):
        '''
        Connect DB file to class
        '''
        self.DBConnect = sqlite3.connect(self.DBpath)
        self.DBConnect.text_factory = lambda x: str(x, "utf-8", "ignore")
        self.DBCursor = self.DBConnect.cursor()

    def reqwToDB(self, Input):
        '''
        manual reqwest to sql terminal, result return as list
        '''
        self.openDB()
        list_ = []
        try:
            for row in self.DBCursor.execute(Input):
                list_.append(row) 
        except sqlite3.OperationalError as Error:
            print('Error: ', Error)
        self.DBConnect.close()
        return list_


    def getHeaders(self):
        res = []
        for row in self.DBCursor.execute('PRAGMA table_info({})'.format(self.mainTab)):
            res.append(row[1])
        return tuple(res)

class mainDB(DbSql):

    def turnMtsOn(self):
        '''
        find items who need to be turn ON
        '''
        from ConstAndOptions import NOT_ACTIVE, NOT_IN_INVENTORY
        self.openDB()
        headers = 'sku, name, warehouse, matrix, nomenclature_1'
        nomencl = []
        endFile = []
        for row in self.DBCursor.execute("SELECT {} FROM {} WHERE mts=0 ORDER BY nomenclature_1".format(headers ,self.mainTab)):
            if row[2] in NOT_IN_INVENTORY or row[3] in NOT_ACTIVE:
                pass
            else:
                endFile.append(row)
        toXlsFile(endFile, 'turnMtsOn')

    def createMainTab(self,headersType):
        #create new db table even if its exists
        self.DBCursor.execute('DROP TABLE IF EXISTS {}'.format(self.mainTab))
        self.DBCursor.execute('CREATE TABLE {} {}'.format(self.mainTab ,headersType))
        self.DBCursor.execute('CREATE UNIQUE INDEX IF NOT EXISTS CombineKey ON {} (sku,warehouse)'.format(self.mainTab))

    def progBar(self,countList):
        """
        return progress bar of exchange
        """
        from copy import copy
        self.LineCount = self.getLenFile(countList)
        self.progres = copy(self.LineCount)
        while self.progres >= 0:
            self.progres = self.progres-1
            self.ProgBar = float(100-(self.progres/self.LineCount)*100)
            yield '{0:0.2f}%'.format(self.ProgBar)


    def updateDB(self):
        print('Starting update main data base from file...')
        self.openDB()
        try:
            from UserInteraktion import BrowseFile
            self.FILE = BrowseFile()
            with open(self.FILE,'r', encoding="utf8") as self.file:
                self.headers = self.sqlFormat(self.file) #transform headers contains in HEADERS var
                self.SqlType = self.typeAsembler(self.headers) #determine the type of column
                self.Bar = self.progBar(self.FILE)
                self.createMainTab(self.SqlType)
                print('Starting import!')
                while True:
                    try:
                        print(self.Bar.__next__()) #progress bar

                        self.Sku = self.toRealType(self.file,self.headers)
                        if self.Sku == [0,]:
                            print('Update Success!')
                            break
                        self.DBCursor.execute('INSERT OR REPLACE INTO {} {} VALUES {}'.format(self.mainTab, tuple(self.headers), tuple(self.Sku)))
                    except sqlite3.IntegrityError:
                        print('Unique name error')
                        break
                    except sqlite3.OperationalError as Err:
                        writErr('updateDB: {}'.format(Err))

            self.DBConnect.commit()
            self.DBConnect.close()
        except FileNotFoundError as Err:
            writErr('updateDB: {}'.format(Err))

    def sqlFormat(self, file):
        '''
        rename headers to sqlike format given from constants
        '''
        from UserInteraktion import BrowseFile
        from ConstAndOptions import HEADERS
        self.headers = list(file.readline().rstrip().split('";"'))
        self.headers[0], self.headers[-1] = self.headers[0][2:], self.headers[-1][:-1] # delete '\ufeff' in first and last element
        self.res = []
        self.headTemplate = HEADERS
        for self.header in self.headers:
            try:
                self.res.append(self.headTemplate[self.header])
            except KeyError as Err:
                writErr('header {} not found in "headTemplate"'.format(Err))
                return 0
        #print(self.res)
        return self.res

    def typeAsembler(self, headers):
        '''
        detects type of header (first row in csv file), 
        combine them with constant and return  for create a table 
        '''
        from ConstAndOptions import HEADERS_TYPE

        res = []
        toStr = '('
        try:
            for header in headers:
                if HEADERS_TYPE[header] is 'S':
                    res.append(header + ' ' + 'TEXT')
                elif HEADERS_TYPE[header] is 'I':
                    res.append(header + ' ' + 'INTEGER')
                elif HEADERS_TYPE[header] is 'F':
                    res.append(header + ' ' + 'REAL')
                else:
                    print('ERROR!: you cant be here!')
        except KeyError as Err:
            writErr('missing {} in HEADERS_TYPE'.format(Err))
            return 0

        for i in res: #transform to string like
            toStr = toStr + str(i) + ', '
        toStr = toStr[0:-2] + ')'
        return toStr

    def toRealType(self, file, headers):
        '''
        convert string of csv file, using as sample headers
        '''
        from ConstAndOptions import HEADERS_TYPE

        self.sku = list(file.readline().rstrip().split('";"'))
        self.sku[0],self.sku[-1] = self.sku[0][1:2], self.sku[-1][:-1] # delete '"' symb at first and last
        self.res = []

        for self.SKU, self.header in zip(self.sku,self.headers):
            try:
                if HEADERS_TYPE[self.header] is 'S':
                    self.res.append(str(self.SKU))
                elif HEADERS_TYPE[self.header] is 'I':
                    #print(header)
                    if self.SKU is '': self.res.append(0)
                    elif self.SKU[-1] is '%': self.res.append(int(self.SKU[0:-1])) #'opb' col correcting
                    else: self.res.append(int(self.SKU))
                elif HEADERS_TYPE[self.header] is 'F':
                    #print(header)
                    if self.SKU is '': self.res.append(0.0)
                    else: self.res.append(float(self.SKU))
                else:
                    print('ERROR!: you cant be here!')
            except KeyError as Err:
                writErr('"toRealType": missing {} in HEADERS_TYPE'.format(Err))
        return self.res

    def getLenFile(self, file):
        with open(file,'r', encoding="utf8") as file:
            self.lines = len(file.readlines())
            return self.lines

class OrderDB(mainDB):
    def updateDBfrom(self, DBtable):
        self.openDB()
        print('Starting update ordered sku...')
        headers = 'sku, name, warehouse, suplayer, moq, bufer, bb_1, leftover, matrix, on_the_way, ob_index, opb_index'
        headersType = self.typeAsembler(headers.split(', '))
        data = [headers.split(', '),] # first row is headers
        self.createMainTab(headersType) #create if not exists...
        #output:
        for row in self.DBCursor.execute("SELECT {} FROM {} WHERE on_the_way<>0 ORDER BY suplayer".format(headers ,DBtable)):
            data.append(row)
        #input:
        for row in data[1:]:
            self.DBCursor.execute('INSERT OR REPLACE INTO {} {} VALUES {}'.format(self.mainTab, tuple(data[0]), tuple(row)))
        #end
        self.DBConnect.commit()
        self.DBConnect.close()


if __name__ == '__main__':
    pass
