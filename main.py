import DbBridge as DB
from UserInteraktion import toXlsFile

dbName = 'Sku_DB'
SkuDB = DB.mainDB(dbName)
SkuDB.mainTab = 'sku_info'

def headerPrew():
    print('-'*50)
    print('\nHere what i can:')
    print('1: import a csv file into my DB!')
    print('2: show positions require to turn MTS on')
    print('3: on the way monitoring')
    print('0: manual input SQL reqest to DB')
    print('\n')

def main():
    print('\n'*8,'Welcome Back!')
    headerPrew()

    while True:
        try:
            chose = input('Enter reqest: ')
        except KeyboardInterrupt:
            print('KeyboardInterrupt')
            chose = None
            print('\n'*4,'Good Bye')
            break
        if chose == 'exit':
            break

        if chose == '1':
            SkuDB.updateDB() # Open new CSV file from inventoy and add to main DB
            headerPrew()
#--------------------------------------------------------------------------------------------------------
        elif chose == '0': # write manual order to DB
            print('Headers:', SkuDB.getHeaders())
            print('Enter the empty reqwest to exit!\n')
            fileName = 'TerminalReqwest'
            while True:
                termReqw = input('\t-=> ')
                if termReqw is '':
                    break
                reqw = SkuDB.reqwToDB(termReqw)
                if reqw:
                    toXlsFile(reqw, fileName)

            headerPrew()
#--------------------------------------------------------------------------------------------------------
        elif chose == '2':
            SkuDB.turnMtsOn()
            
#--------------------------------------------------------------------------------------------------------
        elif chose == '3':
            ordereDB = DB.OrderDB(dbName)
            ordereDB.mainTab = 'ordered'
            ordereDB.updateDBfrom(SkuDB.mainTab)

        elif chose == '4':
            print(ordereDB.getSkuFrom(7, 10947)) #testing

        else:
            print('Wrong reqest! try again')

#--------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()