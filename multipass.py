import pyinputplus as pyip
import sqlite3
import math
import string
import clipboard
import time
import random
from argon2.exceptions import VerifyMismatchError
from argon2 import PasswordHasher
import os
from AES_Python import AES

MAIN_MENU = [
    "Edit Master Password",
    "Add password",
    "Edit Password",
    "Delete Password",
    "View Password",
    "Exit"
]
ADD_MENU = [
    "Add existing",
    "Generate new password",
]
EDIT_MENU = [
    "Edit Website",
    "Edit Username",
    "Edit Password",
    "Generate new password",
]

charsets = [
    string.ascii_lowercase,
    string.ascii_uppercase,
    string.digits,
    string.punctuation
]


def pw_gen():
    # 5 Trigram + 4 sep
    valid = False
    while not valid:
        password = ""
        for i in range(9):
            if i % 2 == 0:
                charset = random.choice([string.ascii_lowercase, string.ascii_uppercase])
                for _ in range(3):
                    password += random.choice(charset)
            else:
                charset = random.choice([string.digits, string.punctuation])
                password += random.choice(charset)

        for charset in charsets:
            if not any(p in charset for p in password):
                break

        else:
            E, valid = entropy(password)

    print(f'Succesfully created password "{password}" with {E} bits of entropy')
    return password


def pw_lookup(term, cat):
    """
    returns list(tuples(0=id, 1=website, 2=usename, 3=password, 4=mfa))
    """
    res = cur.execute(f"SELECT id, website, username, password, mfa FROM pwmanager WHERE {cat} LIKE '%{term}%'")
    return res.fetchall()


def precise_lookup(term, cat):
    """
    returns list(tuples(0=id, 1=website, 2=usename, 3=password, 4=mfa))
    """
    res = cur.execute(f"SELECT id, website, username, password, mfa FROM pwmanager WHERE {cat}='{term}'")
    return res.fetchone()


def update_record(term, cat, rowid):
    cur.execute(f"UPDATE pwmanager SET {cat}='{term}' WHERE id={rowid}")
    con.commit()


def create_record(website, username, password, mfa):
    cur.execute(f"INSERT INTO pwmanager (website, username, password, mfa) VALUES (?, ?, ?, ?)", (website, username, password, mfa))
    con.commit()


def delete_record(rowid):
    cur.execute(f"DELETE FROM pwmanager WHERE id={rowid}")
    con.commit()


def entropy(pw):
    possibilities = 1
    for char in pw:
        if char in string.ascii_letters:
            possibilities *= 26
        elif char in string.digits:
            possibilities *= 10
        elif char in (string.punctuation + ' '):
            possibilities *= 17


    bw_entropy = round(math.log2(possibilities), 5)
    if bw_entropy < 50:
        print('bad')
        return bw_entropy, False
    elif bw_entropy < 60:
        print('meh')
        return bw_entropy, False
    elif bw_entropy < 80:
        print('getting there')
        return bw_entropy, True

    elif bw_entropy > 100:
        print('perfect')
        return bw_entropy, True
    else:
        print('so close')
        return bw_entropy, True


def create_password():
    while True:
        pw = pyip.inputPassword(f'Enter the password: ') 
        E, valid = entropy(pw)
        if valid:
            break
        else:
            print('Password is too weak')
            continue

    return pw


def db_search():
    term = pyip.inputStr("Enter a search term: ")
    category = pyip.inputMenu(['website', 'username', 'password', 'mfa'], "Choose a category:\n", numbered=True)
    records = pw_lookup(term, category)
    if len(records) == 1:
        record = records[0]
    elif len(records) == 0:
        print('No result for this search')
        return None
    else:
        website = pyip.inputMenu([r[1] for r in records], "Select the desired record", numbered=True)
        record = precise_lookup(website, 'website')

    return record

PH = PasswordHasher()
MPWFile = 'output/keyfile'

if not os.path.isfile(MPWFile):
    print('You need to set a master password')
    mpw = create_password()

    with open(MPWFile, 'w') as fp:
        fp.write(PH.hash(mpw))

    aes = AES(key=mpw)

    DB = "output/pw_db.sqlite"
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS pwmanager(id INTEGER PRIMARY KEY ASC, website, username, password, mfa)")
    con.commit()
    aes.enc(file_path=DB)
    exit()

with open(MPWFile) as fp:
    MPWhash = fp.read()

for _ in range(3):
    try:
        MPW = pyip.inputPassword('Enter the master password: ')
        PH.verify(MPWhash, MPW)
        break
    except VerifyMismatchError:
        continue

else:
    print('3 Incorrect attemps, exiting')
    exit()

DB = "output/pw_db.sqlite"
aes = AES(key=MPW)
aes.dec(file_path=f'{DB}.enc')
con = sqlite3.connect(DB)
cur = con.cursor()


def main():
    while 1:
        try:
            match pyip.inputMenu(MAIN_MENU, "Pick an option\n", numbered=True):
                case "Add password":
                    website = pyip.inputURL('Enter the website: ')
                    username = pyip.inputStr('Enter the username/email address: ')
                    match pyip.inputMenu(ADD_MENU, "Pick an option\n", numbered=True):
                        case "Add existing":
                            pw = create_password()

                        case "Generate new password":
                            pw = pw_gen()

                        case _:
                            print("Feature not yet implemented")
                            continue

                    mfa = pyip.inputStr('Enter the MFA string leave blank if not set up: ', blank=True)
                    create_record(website, username, pw, mfa)

                case "Edit Password":
                    # Search by Website, username
                    record = db_search()
                    if record is None:
                        continue
                    match pyip.inputMenu(ADD_MENU, "Pick an option\n", numbered=True):
                        # returns list(tuples(0=id, 1=website, 2=usename, 3=password, 4=mfa))
                        case "Edit Website":
                            wsite = pyip.inputURL(f'Enter the new website (old {record[1]}): ') 
                            update_record(wsite, 'website', record[0])

                        case "Edit Username":
                            user = pyip.inputStr(f'Enter the new username (old {record[2]}): ') 
                            update_record(user, 'username', record[0])

                        case "Edit Password":
                            pw = create_password()
                            update_record(pw, 'password', record[0])


                        case "Generate new password":
                            passwd = pw_gen()
                            update_record(passwd, 'password', record[0])


                        case _:
                            print("Feature not yet implemented")
                            continue
                    
                case "Delete Password":
                    # Search by Website, username
                    record = db_search()
                    if record is None:
                        continue
                    yn = pyip.inputYesNo(f'Are you sur you want to delete {record}')
                    if yn == 'yes':
                        delete_record(record[0])


                case "View Password":
                    # returns list(tuples(0=id, 1=website, 2=usename, 3=password, 4=mfa))
                    record = db_search()
                    if record is None:
                        continue

                    print(f'Website: {record[1]}')
                    print(f'Username: {record[2]}')
                    pw = record[3] # TODO point to pass
                    print(f"Password: {pw} (copied to clipboard!)")
                    if record[4]:
                        print(f"MFA: {record[4]}")
                    clipboard.copy(pw)
                    time.sleep(30)
                    print(chr(27) + "[2J")
                    clipboard.copy('')

                
                case "Exit":
                    aes.enc(DB)
                    break

                case "Edit Master Password":
                    while True:
                        oldmpw = pyip.inputPassword('Enter the old password: ')
                        try:
                            ph.verify(MPW, oldmpw)
                            break
                        except VerifyMismatchError:
                            print('Password is incorrect try again')
                            continue

                        

                case _:
                    print("Feature not yet implemented")
                    continue

        except KeyboardInterrupt:
            print("Caught Ctrl+C Please exit through menu")
            continue

if __name__ == "__main__":
    main()


# SuperPassword$9$