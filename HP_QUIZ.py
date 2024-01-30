# ----- importing libraries

import random as rd
import requests as rq
import datetime
import csv

# ----- basic helper functions

def ask_TF():
    # asks for true or false input until a clear answer is provided, returns choice as boolean
    while True:
        ans = input("Enter 'T' for True or 'F' for false: ").upper()
        if ('T' in ans) and not ('F' in ans):
            print("YOUR ANSWER: True")
            return True
        elif ('F' in ans) and not ('T' in ans):
            print("YOUR ANSWER: False")
            return False
        else:
            print("Your response is not clear, try again. ")

def check_ans(given, actual):
    # compares the given response to the actual answer,
    # returns bool stating if response is correct
    if given == actual:
        print("\t>>> Correct! :D")
        return True
    else:
        print("\t>>> Sorry, wrong answer. :(")
        return False

def ask_YN(msg = ""):
    # asks for yes/no input until a clear answer is provided, returns choice as boolean
    # 'msg' is optional string input to be printed before the 'Y/N:' input request
    while True:
        print(msg, end=" ")
        ans = input("Y/N: ").upper()
        if ('Y' in ans) and not ('N' in ans):
            return True
        elif ('N' in ans) and not ('Y' in ans):
            return False
        else:
            print("Your response is not clear, try again. ")




# ----- score functions

def limit(string, max):
    # if user chooses to save their score they must enter a username
    # ensures that user only enters a username within the limit (to maintain formatting in leaderboard output)
    if len(string) > max:
        string = input(f"Please enter a username that does not exceed {max} characters: ")
    return string

def open_read(file):
    # file handling helper function
    # opens a csv file and reads in the data as a dictionary
    with open(file, 'r') as csv_file:
        spreadsheet = csv.DictReader(csv_file)
        data = []
        for row in spreadsheet:
            data.append(row)
    return data


def open_write(file, data):
    # file handling helper function
    # opens a csv file and saves the score data in dictionary format
    with open(file, 'w') as csv_file:
        spreadsheet = csv.DictWriter(csv_file, fieldnames=field_names, lineterminator='\n')
        spreadsheet.writeheader()
        spreadsheet.writerows(data)


def log_score(file, add_data):
    # adds the new score data to a csv file if it exists,
    # otherwise it creates a new file to store the data

    # If file exists......
    try:
        data = open_read(file)
        data.append(add_data)
        open_write(f_name, data)

    # if the file doesn't exist.....
    except (IOError, FileNotFoundError) as e:
        open_write(f_name, add_data)


# ----- leaderboard functions

def to_integer(data):
    # Leaderboard helper function.
    # Casts values for out_of and percentage to integer, so they can be sorted
    for each in data:
        each['percentage'] = int(each['percentage'])
        each['out_of'] = int(each['out_of'])
    return data


def sort_data(data):
    # Leaderboard helper function
    # Sorts the scores by number of rounds column and then by percentage column
    sorted_data = sorted(sorted(data, key=lambda x: x['out_of'], reverse=True),
                  key=lambda x: x['percentage'], reverse=True)
    return sorted_data


def display_LB(data):
    # Leaderboard helper function
    # displays the leaderboard
    # formatted so that the data appears clearly in columns
    print("\n***************  LEADERBOARD  ***************\n")
    for x in range(len(data)):
        print(f"{x + 1:3}: {data[x]['username']:12} "
              f"Score: {data[x]['score']}/{data[x]['out_of']} = {data[x]['percentage']}%\n")


def leaderboard(file):
    # puts together all the functions to sort the data for the leaderboard and display it
    data = open_read(f_name)
    with_numbers = to_integer(data)
    in_order = sort_data(with_numbers)
    to_LB = in_order[0: min(10, len(data))]
    display_LB(to_LB)
    open_write('leaderboard.csv', in_order)

# -----  all question types

# format of each question:

# INPUT: lst (shuffled list of remaining characters or full list of characters)

# OUTPUTS:
# str ('question' being asked)
# str or bool (the answer 'given' by user)
# str or bool (the 'actual' / correct answer)
# bool (stating if 'is_correct')
# int (index 'ind' to remove from characters list)


def is_student(chars):
    # asks if a given character is a Hogwarts students, True or False
    char = chars[0]
    question = f"Is {char['name']} a student at Hogwarts?"
    print("QUESTION: " + question)
    given = ask_TF()
    actual = char['hogwartsStudent']
    return [question, given, actual, check_ans(given, actual), 0]


def is_staff(chars):
    # asks if a given character is a Hogwarts staff member, True or False
    char = chars[0]
    question = f"Is {char['name']} a staff member at Hogwarts?"
    print("QUESTION: " + question)
    given = ask_TF()
    actual = char['hogwartsStaff']
    return [question, given, actual, check_ans(given, actual), 0]


def is_wizard(chars):
    # asks if a given character is a wizard, True or False
    char = chars[0]
    question = f"Is {char['name']} a wizard?"
    print("QUESTION: " + question)
    given = ask_TF()
    actual = char['wizard']
    return [question, given, actual, check_ans(given, actual), 0]


def is_house(chars):
    # asks if a given character belongs to a particular Hogwarts House, True or False
    ind = 0
    while True:
        if chars[ind]['house'] == '':
            ind += 1
        else:
            break
    char = chars[ind]
    # setting rand_house to have 2 in 5 chance of being correct
    rand_house = rd.choice(all_values['house']+[char['house']])
    question = f"Is {char['name']} in {rand_house} house?"
    print("QUESTION: " + question)
    given = ask_TF()
    actual = char['house'] == rand_house
    return [question, given, actual, check_ans(given, actual), ind]


def is_patronus(chars):
    # asks if a given patronus belongs to a particular wizard, True or False
    ind = 0
    while True:
        if chars[ind]['patronus'] == '':
            ind += 1
        else:
            break
    char = chars[ind]
    # setting rand_patronus to have about 1 in 3 chance of being correct
    rand_patronus = rd.choice(rd.sample(all_values['patronus'], k=3) + [char['patronus']])
    question = f"{char['name']}'s patronus is a/an: {rand_patronus}"
    print("QUESTION: " + question)
    given = ask_TF()
    actual = char['patronus'] == rand_patronus
    return [question, given, actual, check_ans(given, actual), ind]


def is_alt_name(chars):
    # asks if a given alternate name is that of a particular character, True or False
    ind = 0
    while True:
        if chars[ind]['alternate_names'] == []:
            ind += 1
        else:
            break
    char = chars[ind]
    # setting rand_alt_name to have about 1 in 2 chance of being correct
    rand_alt_name = rd.choice(rd.choice(all_values['alternate_names'])+char['alternate_names'])
    question = f"One of {char['name']}'s alternate names is: {rand_alt_name}"
    print("QUESTION: " + question)
    given = ask_TF()
    actual = rand_alt_name in char['alternate_names']
    return [question, given, actual, check_ans(given, actual), ind]


def is_wand_wood(chars):
    # asks if a given wood type is used in a particular wizard's wand, True or False
    chs = chars[:]
    rd.shuffle(chs)

    i = 0
    while True:
        if chs[i]['wand']['wood'] == '':
            i += 1
        else:
            break

    char = chs[i]
    ind = chars.index(char)

    while True:
        option = rd.choice(all_values['wand'])['wood']
        if option != '' and option != char['wand']['wood']:
            other_wand_wood = option
            break

    # rand_wand_wood has 1 in 2 chance of being correct
    rand_wand_wood = rd.choice([other_wand_wood, char['wand']['wood']])
    question = f"The wood type of {char['name']}'s wand is: {rand_wand_wood}"
    print("QUESTION: " + question)
    given = ask_TF()
    actual = rand_wand_wood == char['wand']['wood']
    return [question, given, actual, check_ans(given, actual), ind]


# ----- importing and organizing HP characters data to be used in quiz

# importing Harry Potter characters data using API
url = 'https://hp-api.onrender.com/api/characters'
response = rq.get(url).json() # two steps, request and convert, result is list

n_characters = len(response)


# list of all characters with chosen attributes (keys)
characters = []
for x in range(n_characters):
    character = {
        'name': response[x]['name'],
        'alternate_names': response[x]['alternate_names'],
        'species': response[x]['species'],
        'house': response[x]['house'],
        'wizard': response[x]['wizard'],
        'ancestry': response[x]['ancestry'],
        'wand': response[x]['wand'],
        'patronus': response[x]['patronus'],
        'hogwartsStudent': response[x]['hogwartsStudent'],
        'hogwartsStaff': response[x]['hogwartsStaff']
    }
    characters.append(character)


# list of available attributes (keys) for each character
all_keys = characters[0].keys()


# copying characters list and shuffling to randomize
# will remove characters after being used in a question
chars_left = characters[:]
rd.shuffle(chars_left)


# dictionary with sets of all possible values for each attribute (key), excluding empty
all_values = {}
for key in all_keys:
    values = []
    for character in characters:
        if character[key] != '' and character[key] not in values:
            values.append(character[key])
    all_values.update({key: values})


# ----- setting up for game play (questions types, files to write)

# list of question types to be chosen from randomly
question_types = [is_student, is_staff, is_wizard, is_house, is_patronus, is_alt_name, is_wand_wood]

# for writing question and answers file
today = datetime.datetime.now()
date_short = today.strftime("%d-%m-%Y")

# for csvs
f_name = "scores.csv"
field_names = ['username', 'score', 'out_of', 'percentage']

# ----- game play

def play(chars_left):

    # adding quiz data to save to txt file
    qs_txt = f"\t\t\t>>> Harry Potter Quiz - Your Questions and Answers <<< \n\ndate: {date_short}\n\n"

    # asking number of rounds
    while True:
        num = input("\n>>> Welcome to the Harry Potter Characters Quiz! <<< "
                    "\n\nHow many rounds would you like to play? ").strip()
        if not num.isdigit() or int(num) not in range(1, 51):
            print("You can play 1 to 50 rounds. Please enter a number in that range.")
        else:
            max_rounds = int(num)
            break
            
    # initializing score and starting round
    score = 0
    round_ = 1

    # creating selection of questions
    questions = rd.choices(question_types, k = max_rounds)

    # going through questions
    for question in questions:
        if round_ == max_rounds:
            print(f"\n***** Round {round_} - Last One! *****")
        else:
            print(f"\n***** Round {round_} *****")

        q, given, actual, bool, ind = question(chars_left)

        qs_add = f"{round_}. {q}\n\t\tyour answer: {str(given)}\n\t\tcorrect answer: {str(actual)}\n\n"
        qs_txt += qs_add

        if bool:
            score += 1
        round_ += 1

        chars_left.pop(ind)
        if len(chars_left) < 100:
            chars_left = characters[:]
            rd.shuffle(chars_left)


    # after final round

    end_text = f"\nYou scored {score} out of {max_rounds}."
    p_cent = round(score / max_rounds * 100)
    if p_cent > 75:
        end_text += "\nIncendio! This witch is on fire! You just scored A* in all your O.W.Ls!"
    elif p_cent > 50:
        end_text += "\nWhat a fine wizard you are! You can learn Harry Potter trivia quicker than a Nimbus 2000!"
    elif p_cent > 25:
        end_text += ("\nSome progress made but Professor McGonagall would not be impressed. "
                     "\nRevise your History of Magic!")
    else:
        end_text += ("\nHave you even read Harry Potter? Poor effort young wizard. "
                     "\nGo back to Hogwarts School of Witchcraft and Wizardry for a catch up class!")

    print(end_text)

    qs_txt += f"{end_text}"

    with open('HPquiz_qs.txt', 'w') as file:
        file.write(qs_txt)

    print("\nSee the file HPquiz_qs.txt if you'd like to see your questions and answers.")

    # Restrict score save to 5 or more rounds
    if max_rounds >= 5:
        # If user wants to log their scores
        msg1 = "\nWould you like to save your score?"

        save_score = ask_YN(msg1)

        if save_score:
            username = input("\nEnter a username: ")
            username = limit(username, 10)
            new_data = {'username': username, 'score': score, 'out_of': max_rounds, 'percentage': p_cent}
            log_score(f_name, new_data)

    else:
        print("\nIf you play five rounds or more you have a chance to see your score on the leaderboard!")



# ----- play game

play_again = True
while play_again:
    play(chars_left)
    leaderboard(f_name)
    play_again = ask_YN("Would you like to play again?")



