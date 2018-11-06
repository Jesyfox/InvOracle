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
        returns full row information as dictionary - header:value 
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

    def delete_rows(self, sku_row):
        self.open_db()
        for warehouse_code, sku in sku_row:
            self.DBCursor.execute('''
                DELETE FROM {0} 
                WHERE warehouse_code = {1} 
                AND sku = {2}'''.format(self.main_table ,warehouse_code, sku))
        self.DBConnect.commit()
        self.DBConnect.close()

    def kill_all(self):
        self.open_db()
        self.DBCursor.execute('DELETE FROM {0}'.format(self.main_table))
        self.DBConnect.commit()
        self.DBConnect.close()

    def sql_format(self, List):
        ''' make readable for sql cursor list '''
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
        #from ConstAndOptions import NOT_ACTIVE, NOT_IN_INVENTORY
        #get dict from json file
        from openpyxl import Workbook
        from JsonBridge import json_Bridge
        NOT_ACTIVE = json_Bridge.get('NOT_ACTIVE')
        NOT_IN_INVENTORY = json_Bridge.get('NOT_IN_INVENTORY')

        path = 'OutputFiles\\'
        filename = 'MTS_controll'
        wb = Workbook()
        ws = wb.active

        self.open_db()
        headers = 'sku, name, warehouse, matrix, nomenclature_1, warehouse_code'

        main_list = list(self.DBCursor.execute(
            "SELECT {} FROM {} WHERE mts=0 ORDER BY nomenclature_1".format(headers ,self.main_table)))

        progres = self.progBar(main_list)

        for row in main_list:
            print(progres.__next__())
            if row[headers.split(', ').index('warehouse')] in NOT_IN_INVENTORY or row[headers.split(', ').index('nomenclature_1')] in NOT_ACTIVE:
                pass
            else:
                ws.append(row)

        wb.save(path + filename + '.xlsx')

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
        '''
        import a csv type file into main data base
        file takes from BrowseFile() func.
        if import done without errors return True
        else returns False
        '''
        print('Starting update main data base from file...')
        self.open_db()
<<<<<<< HEAD
        from UserInteraktion import BrowseFile
        self.FILE = BrowseFile()
        with open(self.FILE,'r', encoding="utf8") as self.file:
            raw_headers = list(self.file.readline().rstrip().split('";"'))
            # delete '\ufeff' in first and last element
            raw_headers[0], raw_headers[-1] = raw_headers[0][2:], raw_headers[-1][:-1]
            #transform headers contains in HEADERS var
            headers = self.sql_format_from_file(raw_headers)
            # if func returns 0 that means new object was added to 
            # ConstAndOptions.json and we need re'init the variable
            if not headers:
                print('o')
                headers = self.sql_format_from_file(raw_headers)
            # determine the type of column like - name is S(string) etc
            self.SqlType = self.typeAsembler(headers)
            # progress bar initial so that we can watch what our status
            Bar = self.progBar(self.FILE)
            self.createmain_table(self.SqlType)
            print('Starting import!')
            while True:
                try:
                    print(Bar.__next__()) #progress bar
                    # rewrite shells to sql readable format
                    Sku = self.toRealType(self.file, headers)
                    if Sku == [0,]:
                        print('Update Success!')
                        self.DBConnect.commit()
=======
        try:
            from UserInteraktion import BrowseFile
            self.FILE = BrowseFile()
            with open(self.FILE,'r', encoding="utf8") as self.file:
                raw_headers = list(self.file.readline().rstrip().split('";"'))
                # delete '\ufeff' in first and last element
                raw_headers[0], raw_headers[-1] = raw_headers[0][2:], raw_headers[-1][:-1]
                #transform headers contains in HEADERS var
                headers = self.sql_format_from_file(raw_headers)
                # if func returns 0 that means new object was added to 
                # ConstAndOptions.json and we need re'init the variable
                if not headers:
                    print('o')
                    headers = self.sql_format_from_file(raw_headers)
                # determine the type of column like - name is S(string) etc
                self.SqlType = self.typeAsembler(headers)
                # progress bar initial so that we can watch what our status
                Bar = self.progBar(self.FILE)
                self.createmain_table(self.SqlType)
                print('Starting import!')
                while True:
                    try:
                        print(Bar.__next__()) #progress bar
                        # rewrite shells to sql readeble format
                        self.Sku = self.toRealType(self.file, headers)
                        if self.Sku == [0,]:
                            print('Update Success!')
                            self.DBConnect.commit()
                            self.DBConnect.close()
                            return True
                            break
                        self.DBCursor.execute('INSERT OR REPLACE INTO {} {} VALUES {}'.format(self.main_table, tuple(self.headers), tuple(self.Sku)))
                    except sqlite3.IntegrityError:
                        print('Unique name error')
                        self.DBConnect.close()
                        break
                    except sqlite3.OperationalError as Err:
                        writErr('updateDB: {}'.format(Err))
>>>>>>> 93be35d50c321158febbd943a23e4aadff3a2c98
                        self.DBConnect.close()
                        return True
                        break
                    self.DBCursor.execute('INSERT OR REPLACE INTO {} {} VALUES {}'.format(self.main_table, tuple(headers), tuple(Sku)))
                except sqlite3.IntegrityError:
                    print('Unique name error')
                    self.DBConnect.close()
                    break
        return False

    def sql_format_from_file(self, headers):
        '''
        rename headers to sql-like format given from constants
        '''
        from UserInteraktion import BrowseFile
        #from ConstAndOptions import HEADERS
        #get dict from json file
        from JsonBridge import json_Bridge
        HEADERS = json_Bridge.get('HEADERS')

        #headers = list(file.readline().rstrip().split('";"'))
        # delete '\ufeff' in first and last element
        #headers[0], headers[-1] = headers[0][2:], headers[-1][:-1]
        self.res = []
        self.headTemplate = HEADERS
        for header in headers:
            try:
                #rename 
                self.res.append(self.headTemplate[header])
            except KeyError as Err:
                writErr('header {} not found in "HEADERS"'.format(Err))
                json_Bridge.new_header(Err)
                return 0
        #print(self.res)
        return self.res

    def typeAsembler(self, headers):
        '''
        detects type of header (first row in csv file), 
        combine them with constant and return to create a table 
        '''
        #from ConstAndOptions import HEADERS_TYPE
        #get dict from json file
        from JsonBridge import json_Bridge
        HEADERS_TYPE = json_Bridge.get('HEADERS_TYPE')

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
            toStr = toStr + str(i) + ', ' #CAN WE MAKE IT WITH sql_format()???
        toStr = toStr[0:-2] + ')'
        return toStr

    def toRealType(self, file, headers):
        '''
        convert string of csv file, using as sample headers
        '''
        #from ConstAndOptions import HEADERS_TYPE
        #get dict from json file
        from JsonBridge import json_Bridge
        HEADERS_TYPE = json_Bridge.get('HEADERS_TYPE')

        sku = list(file.readline().rstrip().split('";"'))
        sku[0],sku[-1] = sku[0][1:2], sku[-1][:-1] # delete '"' symb at first and last
        res = []

        for SKU, header in zip(sku, headers):
            try:
                if HEADERS_TYPE[header] is 'S':
                    res.append(str(SKU))
                elif HEADERS_TYPE[header] is 'I':
                    #print(header)
                    if SKU is '': res.append(0)
                    elif SKU[-1] is '%': res.append(int(SKU[0:-1])) #'opb' col correcting
                    else: res.append(int(SKU))
                elif HEADERS_TYPE[header] is 'F':
                    #print(header)
                    if SKU is '': res.append(0.0)
                    else: res.append(float(SKU))
                else:
                    print('ERROR!: you cant be here!')
            except KeyError as Err:
                writErr('"toRealType": missing {} in HEADERS_TYPE'.format(Err))
        return res

    def getLenFile(self, file):
        with open(file,'r', encoding="utf8") as file:
            lines = len(file.readlines())
            return lines

class OrderDB(mainDB):
    def __init__(self, DBname, tabName):
        super(OrderDB, self).__init__(DBname, tabName)
        self.headers = 'sku, name, warehouse, suplayer, warehouse_code, moq, adu, bufer, bb_1, leftover, matrix, on_the_way, ob_index, opb_index'
        self.condition = 'WHERE on_the_way<>0'

    def createmain_table(self,headersType):
        '''create new db table even if its not exists'''
        self.DBCursor.execute('CREATE TABLE IF NOT EXISTS {} {}'.format(self.main_table ,headersType))
        self.DBCursor.execute('CREATE UNIQUE INDEX IF NOT EXISTS OrderedKey ON {} (sku, warehouse_code)'.format(self.main_table))


    def update_db_from(self, DBtable):
        '''
        takes all rows with "on_the_way > 0" from mother-table to main_table in class
        '''
        self.open_db()
        print(self.__class__.__name__, 'Starting update sku...', end='')
        headersList = self.headers.split(', ')
        headersType = self.typeAsembler(headersList)

        self.createmain_table(headersType) #create if not exists...
        self.DBCursor.execute('''
            INSERT OR REPLACE INTO {0}
            SELECT {1} FROM {2} {3} ORDER BY suplayer
            '''.format(self.main_table, self.headers, DBtable, self.condition))

        self.DBConnect.commit()
        self.DBConnect.close()
        print('Update success!')

    def get_all_items(self, headers='warehouse_code, sku'):
        ''' return all items as list of headers '''
        return self.reqwest_to_db('SELECT {} FROM {}'.format(headers, self.main_table))

class OverflowDB(OrderDB):
    """takes all rows with "on_the_way > 0" from mother-table to main_table in class"""
    def __init__(self, DBname, tabName):
        super(OverflowDB, self).__init__(DBname, tabName)
        self.condition = 'WHERE ob_index>100'

        
if __name__ == '__main__':
    pass
