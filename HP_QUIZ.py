#----- importing libraries

import random as rd
import requests as rq
import datetime
import csv


#----- basic helper functions


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


def ask_MC():
    # asks for A, B, C, or D input until a clear answer is provided, returns choice as string
    while True:
        ans = input("Enter 'A', 'B', 'C' or 'D' to indicate your answer: ").upper()
        if ('A' in ans) and not (('B' in ans) or ('C' in ans) or ('D' in ans)):
            print("Your answer: A")
            return 'A'
        elif ('B' in ans) and not (('A' in ans) or ('C' in ans) or ('D' in ans)):
            print("Your answer: B")
            return 'B'
        elif ('C' in ans) and not (('B' in ans) or ('A' in ans) or ('D' in ans)):
            print("Your answer: C")
            return 'C'
        elif ('D' in ans) and not (('B' in ans) or ('C' in ans) or ('A' in ans)):
            print("Your answer: D")
            return 'D'
        else:
            print("Your response is not clear, try again. ")


def mix_MC(ans, x, y, z):
    lst = [ans, x, y, z]
    rd.shuffle(lst)
    actual_ind = lst.index(ans)
    actual = ['A', 'B', 'C', 'D'][actual_ind]
    A, B, C, D = lst
    return A, B, C, D, actual


def print_MC(q, A, B, C, D):
    # asks for true or false input until a clear answer is provided, returns choice as boolean
    return f"{q}\n\tA: {A}\n\tB: {B}\n\tC: {C}\n\tD: {D}"


def check_ans(given, actual):
    # compares the given response to the actual answer, returns boolean stating if response is correct
    if given == actual:
        print("\t>>> Correct! :D")
        return True
    else:
        print("\t>>> Sorry, wrong answer. :(")
        return False


def ask_YN():
    # asks for yes/no input until a clear answer is provided, returns choice as boolean
    while True:
        ans = input("\nWould you like to save your score? Y/N: ").upper()
        if ('Y' in ans) and not ('N' in ans):
            return True
        elif ('N' in ans) and not ('Y' in ans):
            return False
        else:
            print("Your response is not clear, try again. ")

def limit(string):
    if len(string)>10:
        string = input("Please enter a username that does not exceed 10 characters: ")
    return string

def open_read(file):
    with open(file, 'r') as csv_file:
        spreadsheet = csv.DictReader(csv_file)
        data = []
        for row in spreadsheet:
            data.append(row)
    return data


def open_write(file, data):
    with open(file, 'w') as csv_file:
        spreadsheet = csv.DictWriter(csv_file, fieldnames=field_names, lineterminator='\n')
        spreadsheet.writeheader()
        spreadsheet.writerows(data)


def to_integer(data):
    # Leaderboard helper function.
    # Casts values for out_of and percentage to integer so they can be sorted
    for each in data:
        each['percentage'] = int(each['percentage'])
        each['out_of'] = int(each['out_of'])
    return data


def sort_data(data):
    # Leaderboard helper function
    # Sorts the scores by number of rounds column and then by percentage column
    sorted_data = sorted(sorted(data, key=lambda x: x['out_of'], reverse=True), key=lambda x: x['percentage'], reverse=True)
    return sorted_data


def no_in_LB(data):
    # Leaderboard helper function
    # Ensures that the leaderboard has a maximum of 10 entries or less.
    if len(data)>10:
        return 10
    else:
        return len(data)


def display_LB(data):
    print("\n***************   LEADERBOARD  ***************\n")
    for x in range(no_in_LB(data)):
        print(f"{x+1}: {data[x]['username']:<20}Score:{data[x]['score']}/{data[x]['out_of']:<20}Percentage: {data[x]['percentage']:<20}\n")


#-----  all question types, each with the following form:

# INPUT: lst (shuffled list of remaining characters or full list of characters)

# OUTPUTS:
# str ('question' being asked)
# str or bool (the answer 'given' by user)
# str or bool (the 'actual' / correct answer)
# bool ('is_correct')
# int (index 'ind' to remove from characters list, None if not removing one)


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
    char = chars_left[ind]
    rand_house = rd.choice(all_values['house']+[char['house']]) # 2 in 5 chance correct
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
    char = chars_left[ind]
    rand_patronus = rd.choice(rd.sample(all_values['patronus'], k = 3) + [char['patronus']])
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

    # ind = CAN pass back index, but need to calculate correctly
    # in reference to chars_left - TRY

    while True:
        option = rd.choice(all_values['wand'])['wood']
        if option != '' and option != char['wand']['wood']:
            other_wand_wood = option
            break

    rand_wand_wood = rd.choice([other_wand_wood, char['wand']['wood']])
    question = f"The wood type of {char['name']}'s wand is: {rand_wand_wood}"
    print("QUESTION: " + question)
    given = ask_TF()
    actual = rand_wand_wood == char['wand']['wood']
    return [question, given, actual, check_ans(given, actual), None]


#----- importing and organizing HP characters data to be used in quiz


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
# can remove characters after being used in a question
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
    # print(key, values)


#----- setting up for game play (questions types, files to write)


# list of question types to be chosen from randomly
question_types = [is_student, is_staff, is_wizard, is_house, is_patronus, is_alt_name, is_wand_wood]


# for writing question and answers file
today = datetime.datetime.now()
date_short = today.strftime("%d-%m-%Y")
qs_txt = f"\t\t\t>>> Harry Potter Quiz - Your Questions and Answers <<< \n\ndate: {date_short}\n\n"


#-----  game play


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
roundx = 1

# creating selection of questions
questions = rd.choices(question_types, k = max_rounds)

# going through questions
for question in questions:

    if roundx == max_rounds:
        print(f"\n***** Round {roundx} - Last One! *****")
    else:
        print(f"\n***** Round {roundx} *****")

    if question in [is_wand_wood]:  # ADD MC_species when done
        q, given, actual, bool, ind = question(characters)
    else:
        q, given, actual, bool, ind = question(chars_left)

    qs_add = f"{roundx}. {q}\n\t\tyour answer: {str(given)}\n\t\tcorrect answer: {str(actual)}\n\n"
    qs_txt += qs_add

    if bool:
        score += 1

    roundx += 1

    if ind is not None:
        chars_left.pop(ind)

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


#-----  leaderboard


def log_score(file, add_data):
    # If file exists......
    try:
        data = open_read(file)
        data.append(add_data)
        open_write(f_name, data)

    # if the file doesn't exist:
    except (IOError, FileNotFoundError) as e:
        open_write(f_name, add_data)

def leaderboard():
    data = open_read(f_name)
    with_numbers = to_integer(data)
    in_order = sort_data(with_numbers)
    display_LB(in_order)
    open_write('leaderboard.csv', in_order)


f_name = "scores.csv"
field_names = ['username', 'score', 'out_of', 'percentage']

# If user wants to log their scores
save_score = ask_YN()
if save_score:
    username = input("Enter a username: ")
    username = limit(username)
    new_data = {'username': username, 'score': score, 'out_of': max_rounds, 'percentage': p_cent}
    log_score(f_name, new_data)

# Display leaderboard
leaderboard()





