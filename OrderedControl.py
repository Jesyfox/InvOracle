from UserInteraktion import toXlsFile

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


def arrival_check(ordered_db, main_db):
    '''
    Compares two states, oredered and arrival.
        ordered state hold - ordered_db(updated yesterday or later)
        arrival(or  not) hold - main_db(updated today)
    after processing row will deleted from - ordered_db 
    result write to xls file
    '''
    ordered_list = ordered_db.get_all_items()
    headers = list(ordered_db.get_headers())
    res = [headers, ]
    sku_row = []
    for row in ordered_list:
        ordered = ordered_db.get_row(row)
        arrival = main_db.get_row(row)

        try:
            if arrival['on_the_way'] == 0: # If the waiting time for the order is over
                print('row:', row)
                for header in headers:
                    sku_row.append(arrival[header])

                #status col #1:
                status_col = ob_opb_check(ordered['leftover'], ordered['on_the_way'], arrival['leftover'])
                if isinstance(status_col, float): status_col = round(status_col) 
                sku_row.append(status_col)
                #______ col #n
                res.append(sku_row)
                print('len:',len(res))
        except TypeError:
            print('ERROR!', row, 'closed in matirix?')
            pass

            res.append(sku_row)
            print('len:',len(res))
        sku_row = []
        #ordered_db.delete_row(row)
    #add additional column
    res[0].append('status') #1

    toXlsFile(res, 'arrival_check')


if __name__ == "__main__":
    print(ob_opb_check(5, 5, 1))



