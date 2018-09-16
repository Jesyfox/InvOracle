import sqlite3
from UserInteraktion import writErr, toXlsFile

#miss white

class DbSql(object):

    def __init__(self, DBname, tabName):
        import os
        self.DBname = DBname
        self.main_table = tabName
        directory = 'DataBase'
        splt = '\\'
        if not os.path.exists(directory):
            os.makedirs(directory)
        self.DBpath =  os.getcwd() + splt + directory + splt + self.DBname + '.db'
        self.open_db()

    def open_db(self):
        '''
        Connect DB file to class
        '''
        self.DBConnect = sqlite3.connect(self.DBpath)
        #self.DBConnect.text_factory = lambda x: str(x, 'utf-8', 'ignore')
        self.DBCursor = self.DBConnect.cursor()

    def reqwest_to_db(self, Input):
        '''
        manual reqwest to sql terminal, result return a list
        '''
        self.open_db()
        list_ = []
        try:
            for row in self.DBCursor.execute(Input):
                list_.append(row) 
        except sqlite3.OperationalError as Error:
            writErr(str(Error))
        self.DBConnect.close()
        return list_

    def get_headers(self):
        self.open_db()
        res = []
        for row in self.DBCursor.execute('PRAGMA table_info({})'.format(self.main_table)):
            res.append(row[1])
        self.headers = tuple(res)
        self.DBConnect.close()
        return self.headers

    def get_row(self, sku_row:tuple):
        ''' 
        Takes tuple (warehouse_code, sku) and
        returns one sku from warehouse, as dictionary - header:value 
        '''
        warehouse_code, sku = sku_row
        headers = self.sql_format(self.get_headers())
        reqwest = 'SELECT {0} FROM {1} WHERE warehouse_code = {2} AND sku = {3}'.format(headers, self.main_table, warehouse_code, sku)

        try:
            item = self.reqwest_to_db(reqwest)[0]
            return dict(zip(headers.split(', '), item))
        except IndexError as Err:
            print('get_row: error: {}'.format(Err))
            return None

    def delete_row(self, sku_row:tuple):
        self.open_db()
        warehouse_code, sku = sku_row
        self.DBCursor.execute('DELETE FROM {0} WHERE warehouse_code = {1} AND sku = {2}'.format(self.main_table ,warehouse_code, sku))
        self.DBConnect.commit()
        self.DBConnect.close()


    def sql_format(self, List):
        ''' make readable list for sql cursor '''
        res = str()
        for i in List:
            res += str(i) + ', '
        return res.rstrip(', ') #remove last ', ' from string

class mainDB(DbSql):
    def __init__(self, DBname, tabName):
        super(mainDB, self).__init__(DBname, tabName)
        self.get_headers()

    def turn_MTS_on(self):
        '''
        find items who need to be turn ON
        '''
        from ConstAndOptions import NOT_ACTIVE, NOT_IN_INVENTORY
        self.open_db()
        headers = 'sku, name, warehouse, matrix, nomenclature_1, warehouse_code'
        nomencl = []
        endFile = []
        for row in self.DBCursor.execute("SELECT {} FROM {} WHERE mts=0 ORDER BY nomenclature_1".format(headers ,self.main_table)):
            if row[2] in NOT_IN_INVENTORY or row[3] in NOT_ACTIVE:
                pass
            else:
                endFile.append(row)
        toXlsFile(endFile, 'turn_MTS_on')

    def createmain_table(self,headersType):
        #create new db table even if its exists
        self.DBCursor.execute('DROP TABLE IF EXISTS {}'.format(self.main_table))
        self.DBCursor.execute('CREATE TABLE {} {}'.format(self.main_table ,headersType))
        self.DBCursor.execute('CREATE UNIQUE INDEX IF NOT EXISTS CombineKey ON {} (sku,warehouse_code)'.format(self.main_table))

    def progBar(self,countList):
        """
        return progress bar of exchange
        howto:
            1.name the variable with this func
            2.print(var.__next__())
        """
        from copy import copy
        try:
            self.LineCount = self.getLenFile(countList)
        except TypeError: # if its not a file:
            self.LineCount = len(countList)
        self.progres = copy(self.LineCount)
        while self.progres >= 0:
            self.progres = self.progres-1
            self.ProgBar = float(100-(self.progres/self.LineCount)*100)
            yield '{0:0.2f}%'.format(self.ProgBar)


    def update_db_from(self):
        print('Starting update main data base from file...')
        self.open_db()
        try:
            from UserInteraktion import BrowseFile
            self.FILE = BrowseFile()
            with open(self.FILE,'r', encoding="utf8") as self.file:
                self.headers = self.sql_format_from_file(self.file) #transform headers contains in HEADERS var
                self.SqlType = self.typeAsembler(self.headers) #determine the type of column
                Bar = self.progBar(self.FILE)
                self.createmain_table(self.SqlType)
                print('Starting import!')
                while True:
                    try:
                        print(Bar.__next__()) #progress bar

                        self.Sku = self.toRealType(self.file,self.headers)
                        if self.Sku == [0,]:
                            print('Update Success!')
                            break
                        self.DBCursor.execute('INSERT OR REPLACE INTO {} {} VALUES {}'.format(self.main_table, tuple(self.headers), tuple(self.Sku)))
                    except sqlite3.IntegrityError:
                        print('Unique name error')
                        break
                    except sqlite3.OperationalError as Err:
                        writErr('updateDB: {}'.format(Err))

            self.DBConnect.commit()
            self.DBConnect.close()
        except FileNotFoundError as Err:
            writErr('updateDB: {}'.format(Err))

    def sql_format_from_file(self, file):
        '''
        rename headers to sql-like format given from constants
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
            lines = len(file.readlines())
            return lines

class OrderDB(mainDB):
    def __init__(self, DBname, tabName):
        super(OrderDB, self).__init__(DBname, tabName)
        self.headers = 'sku, name, warehouse, suplayer, warehouse_code, moq, bufer, bb_1, leftover, matrix, on_the_way, ob_index, opb_index'

    def update_db_from(self, DBtable):
        '''
        takes all rows with "on_the_way > 0" to main_table
        '''
        self.open_db()
        print('Starting update ordered sku...')
        headersList = self.headers.split(', ')
        headersType = self.typeAsembler(headersList)
        data = [] # first row is headers

        self.createmain_table(headersType) #create if not exists...

        #output from mainDB:
        for row in self.DBCursor.execute("SELECT {} FROM {} WHERE on_the_way<>0 ORDER BY suplayer".format(self.headers ,DBtable)):
            data.append(row)

        #input:
        bar = self.progBar(data)
        rowsCounted = 0
        for row in data:
            print(bar.__next__())
            self.DBCursor.execute('INSERT OR REPLACE INTO {} {} VALUES {}'.format(self.main_table, tuple(headersList), tuple(row)))
            rowsCounted += 1
        #end
        self.DBConnect.commit()
        self.DBConnect.close()
        print('update success \n{0} rows was exported'.format(rowsCounted))

    def get_all_items(self):
        ''' return list of all unique items (warehouse_code, sku) '''
        headers = 'warehouse_code, sku'
        return self.reqwest_to_db('SELECT {} FROM {}'.format(headers, self.main_table))


if __name__ == '__main__':
    pass
