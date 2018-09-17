import DbBridge as DB
import OrderedControl as OC
from UserInteraktion import toXlsFile


dbName = 'Sku_DB'
SkuDB = DB.mainDB(dbName, 'sku_info')
orderDB = DB.OrderDB(dbName, 'ordered')

def FAQ_preview():
    print('-'*50)
    print('\nHere what i can:')
    print('1: import a csv file into main DB!')
    print('2: show positions require to turn MTS on')
    print('3: import "on_the_way > 0" into oreded DB')
    print('4: test')
    print('0: manual input SQL reqest to DB')
    print('\n')

def main():
    print('\n'*8,'Welcome Back!')
    FAQ_preview()

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
            SkuDB.update_db_from() # Open new CSV file from inventoy and add to main DB
            FAQ_preview()
#--------------------------------------------------------------------------------------------------------
        elif chose == '0': # write manual order to DB
            print('Headers:', SkuDB.get_headers())
            print('Enter the empty reqwest to exit!\n')
            fileName = 'TerminalReqwest'
            while True:
                termReqw = input('\t-=> ')
                if termReqw is '':
                    break
                reqw = SkuDB.reqwest_to_db(termReqw)
                if reqw:
                    toXlsFile(reqw, fileName)

            FAQ_preview()
#--------------------------------------------------------------------------------------------------------
        elif chose == '2':
            SkuDB.turn_MTS_on()
            
#--------------------------------------------------------------------------------------------------------
        elif chose == '3':
            orderDB.update_db_from(SkuDB.main_table)

        elif chose == '4':
            #testin
            OC.arrival_check(orderDB, SkuDB)

        else:
            print('Wrong reqest! try again')

#--------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()