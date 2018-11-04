"""
contains classes and functions, worging with JSON's data bases.
"""
import json

DB_PATH_FOLDER = 'DataBase\\ConstAndOptions.json'

class JsonDB(object):
    '''
    class will be return reqwested dictionaries from json db
    and add new one's elements if missing
    '''
    def __init__(self, path=DB_PATH_FOLDER):
        self.path_folder = path
        with open(self.path_folder, encoding='utf-8') as json_file:
            #get all main keys from json file
            #self.keys = list(json.load(json_file).keys())
            pass

    def get(self, name=''):
        '''
        return reqwested key dict
        '''
        with open(self.path_folder, encoding='utf-8') as json_file:
            if name is '':
                #get all
                return json.load(json_file)
            else:
                return json.load(json_file)[name]

    def addTo(self, key, name:dict):
        #get all obj
        main_dict = self.get()
        
        #add new obj
        main_dict[key].update(name)

        #write to json file
        with open(self.path_folder, 'w', encoding='utf-8') as json_file:
            json.dump(main_dict, json_file, ensure_ascii=False, indent=4)



    def new_header(self, key):
        '''
        open an input constructor for creating new key header
        after catching an KeyError
        '''
        # S - TEXT, F - REAL, I - INTEGER
        sql_types = ['S','I','F']
        key = str(key).strip('\'')
        #User Dialog

        print('new key - {}, will be added. Enter the name of it'.format(key))
        print('Types: ', end='')
        for i in sql_types: 
            print(i, end=' ')
        print('\n')
        print('write "redo" to restart')
        while True:
            NAME = input('NAME: ')
            TYPE = input('TYPE: ')

            if TYPE in sql_types:
                break
            else:
                print('wrong type, try again...')

        self.addTo('HEADERS', {key:NAME})
        self.addTo('HEADERS_TYPE', {NAME:TYPE})

def dump_From_Py_File_To_Json(DB_PATH_FOLDER):
    '''
    take all info from py file
    and write all to the json file
    use it while i rewrite stable reqwest bridge class - 'JSON to Python'
    '''
    with open(DB_PATH_FOLDER, 'w', encoding='utf-8') as json_file:
        import ConstAndOptions
        #get all non standart variables(keys) in py file
        keys = [key for key in dir(ConstAndOptions) if not key.startswith('__')]
        
        #create common dicrionary from py file with keys
        main_dict = {}
        for key in keys:
            main_dict['{}'.format(str(key))] = eval('ConstAndOptions.{}'.format(key))
        
        #write to json file
        data = json.dump(main_dict, json_file, ensure_ascii=False, indent=4)

#main object to import
json_Bridge = JsonDB()

def main():
    '''for testing'''
    dump_From_Py_File_To_Json(DB_PATH_FOLDER)
    #json_Bridge.addTo('HEADERS', {'foo':'bar'})
    #json_Bridge.addTo('HEADERS_TYPE', {'bar':'F'})
    pass

if __name__ == '__main__':
    main()