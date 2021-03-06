#!/usr/bin/python3

__author__ = 'Antonio Masotti'
__date__ = '20.09.2018'

'''

Some auxiliary functions for the main script

'''

def trasforma_result(raw_list):

    '''
    The regex will output a list of tuples with matched form and endings.

    This functions manipulate the list and 
    returns only the greek forms matching the regex

    '''
    stats = []
    temp = []
    final_list = []

    # extract the single results
    for listObj in raw_list:
        temp.extend(listObj)
    # build a single list with the verbal forms
    for pair in temp:
        final_list.append(pair[0])

    # delete the duplicates
    final_list = list(set(final_list))
    return (final_list, stats)


# prepare the text deleting the verse number
def delete_number(text_to_analyze):
    '''

     DOC: Deletes the verse number from the raw text

    '''
    number = r"(\d{1,}\.?\d{1,}?)"
    number_subst = ""
    find_number = re.sub(number, number_subst, text_to_analyze, 0, re.MULTILINE | re.DOTALL)

    if find_number:
        raw_text = find_number

    return raw_text

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
