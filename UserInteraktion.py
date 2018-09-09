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
    say the error and return to main
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
    wb.save(path + filename + '.xlsx')

if __name__ == '__main__':
    #print(BrowseFile())
    writErr('hello world')
