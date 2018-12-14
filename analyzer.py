#!/bin/env python

from sys import argv

LANGUAGES=["EN"]
STAT_POSITIONS = {
    "FR": "aeisnrtoludcmpégbvhfqyxjèàkwz",
    "EN": "etaoinshrdlcumwfgypbvkjxqz",
    "LA": "ieautsrnomclpdbqgvfhxyzk"
}
SPACES=True

def usage():
    print(f"{argv[0]}: word (language)")
    return -1

def count_valid_words(dico, words):
    count = 0
    for word in words:
        if word in dico and len(word) >= 3:
            count+=len(word)
    return count

def stat_decypher(string, chars):
    for language in LANGUAGES:
        stat_positions = STAT_POSITIONS[language]
        stat_positions = ' ' + stat_positions if SPACES else stat_positions
        output = string
        for index, char in enumerate(chars):
            if index < len(stat_positions):
                output = output.replace(char['char'], stat_positions[index])
        print('%s: %s' %(language, output))
        words = output.split(' ')
        top_valid = 0
        best_bruteforce = output
        for index, word in enumerate(words):
            try:
                print('Word is %s (%s/%s)' %(word, index, len(words)))
                with open('dictionaries/%s.txt' %language) as f:
                    dico = [line.replace('\n', '') for line in f.readlines()]
                    for index, line in enumerate(dico):
                        print("line: %s" %(index), end='\r')
                        if len(word) == len(line):
                            test = output
                            for index, char in enumerate(line):
                                test = test.replace(word[index], line[index])
                            valid_words = count_valid_words(dico, test.split(' '))
                            if valid_words > top_valid:
                                top_valid = valid_words
                                best_bruteforce = test
                                print('-- %s (%s)' %(best_bruteforce, top_valid))
            except Exception as e:
                print(e)
                pass
    return string

def main():
    if len(argv) < 2:
        return usage()
    chars = []
    enumerated = []
    string = argv[1]
    for index, char in enumerate(string):
        if char not in enumerated:
            enumerated.append(char)
            chars.append({"char": char, "count": string.count(char)})
    chars.sort(key=lambda c: c["count"], reverse=True)
    stat_decypher(string, chars) 

if __name__ == "__main__":
    exit(main())
