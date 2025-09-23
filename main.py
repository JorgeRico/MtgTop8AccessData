from classes.menu import Menu 


if __name__ == "__main__":
    menu = Menu()
    # can be commented if exists excel and json data files
    # menu.accessToExcel()
    # # can be commented if exists excel and json data files
    # menu.excelToJson()
    # insert data on mysql DB
    menu.jsonToDatabase()

