import csv
import os

if not os.path.exists('OutputFiles'):
    os.makedirs('OutputFiles')


def BrowseFile():
    '''
    start a file dialog (open folder) with starting point: __file__
    '''

    from tkinter import Tk
    from tkinter.filedialog import askopenfilename
    from os import path
    root = Tk()
    ftypes = [('Comma Separated Values',"*.CSV")]
    dir1 = path.dirname(path.abspath(__file__)) # start at dir file
    #root.fileName = askopenfilename(filetypes = ftypes, initialdir = dir1)
    fileWay = askopenfilename(filetypes = ftypes, initialdir = dir1)
    root.destroy()
    return fileWay

def writErr(text):
    '''
    print Error masage
    and write to Errorlog file
    '''
    print('-'*50)
    print('Error!: ',text)
    #console cant read Utf-8 symbols so i write cope of the error to the file:
    with open('OutputFiles\\ErrorLog.txt','w',encoding='utf8') as file:
        file.write(text)

def toXlsFile(file, filename):
    from openpyxl import Workbook
    wb = Workbook()
    ws = wb.active
    path = 'OutputFiles\\'
    for row in file:
        ws.append(row)
        try:
            wb.save(path + filename + '.xlsx')
        except PermissionError:
            wb.save(path +  'CLOSE_ORIGINAL!_' + filename + '.xlsx')


def progress_bar(countList):
    """
    return progress bar of list enumeration
    howto:
        1.name the variable with this func
        2.print(var.__next__())
    """
    from copy import copy
    LineCount = len(countList)
    progres = copy(LineCount)
    while progres >= 0:
        progres = progres-1
        ProgBar = float(100-(progres/LineCount)*100)
        yield '{0:0.2f}%'.format(ProgBar)

if __name__ == '__main__':
    #print(BrowseFile())
    LIST = [x**x for x in range(50)]
    bar = progress_bar(LIST)
    for i in LIST:
        print(i, bar.__next__())

