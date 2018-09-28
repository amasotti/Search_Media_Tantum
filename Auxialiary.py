'''

Some functions for the main script

GNU License 20.09.2018 - Antonio Masotti

'''

def trasforma_result(lista_grezza):
    '''
    The regex will output a list of tuples with matched form and endings.
    This functions manipulate the list and
    returns only the greek forms matching the regex

    '''
    # initialize object for form manipulation and statistics
    statistiche = []
    temp = []
    lista_finale = []

    # extract the single results
    for lista in lista_grezza:
        temp.extend(lista)
    # build a single list with the verbal forms
    for pair in temp:
        lista_finale.append(pair[0])

    # delete the duplicates
    lista_finale = list(set(lista_finale))
    return (lista_finale, statistiche)

def again():
    '''
    DOC:
    Simple function to continue the main while loop.
    If the user tips y the script will ask for a new directory
    if not the script closes.

    '''
    # ask if there is another directory to scan
    choice = input('Do you want to analyze another directory? (y/n) ')
    if choice.lower() == 'y':
        new_directory = True
    else:
        print('Good bye!')
        new_directory = False
    return new_directory
