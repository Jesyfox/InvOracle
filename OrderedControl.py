from UserInteraktion import toXlsFile, progress_bar

def ob_opb_check(leftover_ord, on_the_way_ord, leftover_arr):
    '''
    leftover_ord - last leftover
    (leftover_ord + on_the_way_ord) - last leftover with order
    leftover_arr - fresh leftover 
    '''
    if leftover_ord < leftover_arr <= (leftover_ord + on_the_way_ord): #if order arrived 
        return leftover_arr/(leftover_ord + on_the_way_ord)*100 #return how many
    elif leftover_arr <= leftover_ord: # if order didnt arrive
        try:
            return (leftover_arr/leftover_ord*100)-100 #return leftover change
        except ZeroDivisionError: # leftover was 0 and order not arrived
            return 'DEAD!'
    elif leftover_arr > (leftover_ord + on_the_way_ord): #if order more than expected
        return (leftover_arr/(leftover_ord + on_the_way_ord))*100 #return home many

    else: #if somthing wrong
        print('you cant be here!', 'leftover_ord:', leftover_ord, '(leftover_ord + on_the_way_ord):',(leftover_ord + on_the_way_ord), 'leftover_arr:', leftover_arr, sep='\n')
        return '???'

def adu_check(ordered_adu, arrived_adu):
    '''
    returns change percent of adu
    ADU - average daily usage
    '''
    try:
        if not ordered_adu or not arrived_adu:
            if arrived_adu > ordered_adu:
                return '+' + str(arrived_adu)
            elif arrived_adu == ordered_adu:
                return '0.0'
            else: return '-' + str(ordered_adu)
        else:
            return str(round(100 - (ordered_adu/arrived_adu)*100, 1)) + '%' # return rounded change percent
    except ZeroDivisionError:
        print(ordered_adu, arrived_adu)
        raise Exception

def arrival_check(ordered_db, main_db):
    '''
    Compares two states, oredered and arrival.
        ordered state hold - ordered_db(updated yesterday or later)
        arrival(or  not) hold - main_db(updated today)
    Adds additional colums with more information/
    After processing row will deleted from - ordered_db 
    result write to xls file
    THIS IS NEED MAKE A CLASS!
    '''
    from openpyxl import Workbook #XLS
    wb = Workbook() #XLS
    ws = wb.active #XLS
    path = 'OutputFiles\\'
    filename = 'arrival_check'

    ordered_list = ordered_db.get_all_items()
    headers = list(ordered_db.get_headers())[:-3] # delete 'on_the_way', 'ob_index', 'opb_index'
    for col in ['status','adu_change']: # add my cols
        headers.append(col)

    ws.append(headers) 
    sku_row = []
    bar = progress_bar(ordered_list)
    arrived = []

    for row in ordered_list:
        progress = bar.__next__()
        ordered = ordered_db.get_row(row)
        arrival = main_db.get_row(row)

        try:
            if arrival['on_the_way'] == 0: # If the waiting time for the order is over
                print(progress)
                arrived.append(row)

                #'status' column #1:
                status_col = ob_opb_check(ordered['leftover'], ordered['on_the_way'], arrival['leftover'])
                if isinstance(status_col, float): status_col = round(status_col) 
                #______ column #n

                #-------------mother_columns-------------------
                for header in headers[:-3]: # delete 'on_the_way', 'ob_index', 'opb_index'
                    sku_row.append(arrival[header])

                #-------------my_columns---------------------
                sku_row.append(status_col) # add 'status' column
                sku_row.append(adu_check(ordered['adu'], arrival['adu']))

                ws.append(sku_row) #xls

        except TypeError:
            print('ERROR!', row, 'closed in matirix?')
            sku_row.append(row[0])
            sku_row.append(row[1])
            sku_row.append('closed in matrix')
            ws.append(sku_row)
        sku_row = [] # clear when done

    try:
        wb.save(path + filename + '.xlsx')
    except PermissionError:
        wb.save(path +  'CLOSE_ORIGINAL!_' + filename + '.xlsx')

    ordered_db.delete_rows(arrived) # when imported - delete from db

class Output_statistic(object):
    '''
    Compares two states, past and present.
        past_db(updated yesterday or later)
        present_db(updated today)
    returns changes...
    to the xls file, right now...
    '''
    def __init__(file_name, past_db, present_db):
        from openpyxl import Workbook
        self.file_name = 'OutputFiles\\' + file_name
        self.work_book = Workbook()
        self.work_sheet = wb.active
        self.past_db = past_db
        self.present_db = present_db
        self.workflow_list = past_db.get_all_items()
        self._bar = progress_bar(self.workflow_list)
        self.progress = _bar.__next__()

    def headers_assembler(self):
        '''assemble headers for file, can add additional columns'''
        headers = list(past_db.get_headers())[:-3] # delete 'on_the_way', 'ob_index', 'opb_index'
        if self.has_additional_cols:
            for col in self.has_additional_cols: # add my cols
                headers.append(col)
        return headers



if __name__ == "__main__":
    print(adu_check(0.1,0.11))



