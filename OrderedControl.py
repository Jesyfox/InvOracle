from UserInteraktion import toXlsFile

def ob_opb_check(ob_ord, opb_ord, ob_arr):
    '''
    ob - state of buffer fullness on right moment
    opb - state of buffer fullness with ordered count
    ob_ord - last leftover
    opb_ord - last leftover with order
    ob_arr - fresh leftover 
    '''
    if ob_ord < ob_arr <= opb_ord: #if order arrived 
        return ob_arr/opb_ord*100
    elif ob_arr <= ob_ord: # if order didnt arrive
        return (ob_arr/ob_ord*100)-100
    elif ob_arr > opb_ord: #if order more than expected
        return (ob_arr/opb_ord)*100
    else: #if somthing wrong
        print('you cant be here!', 'ob_ord:', ob_ord, 'opb_ord:',opb_ord, 'ob_arr:', ob_arr, sep='\n')
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
        print('row:', row)
        ordered = ordered_db.get_row(row)
        arrival = main_db.get_row(row)
        if arrival['on_the_way'] == 0:
            for header in headers:
                sku_row.append(arrival[header])
            sku_row.append(ob_opb_check(ordered['ob_index'], ordered['opb_index'], arrival['ob_index']))
            res.append(sku_row)
        sku_row = []
        ordered_db.delete_row(row)

    res[0].append('status')
    toXlsFile(res, 'arrival_check')


if __name__ == "__main__":
    print(ob_opb_check(24, 97, 56))



