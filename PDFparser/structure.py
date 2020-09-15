from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
import re

path_to_pdf = "./innovate.pdf"

with open('txtbook.txt', 'r') as file:
    content = file.read().replace('\n', '')


def get_pdf_file_structure(path_to_pdf):
    fp = open(path_to_pdf, 'rb')
    parser = PDFParser(fp)
    document = PDFDocument(parser, password="")

    outlines = document.get_outlines()
    chapters = list()
    for (level, title, dest, a, se) in outlines:
        chapters.append(title)

    fp.close()
    return (chapters)


structure = get_pdf_file_structure(path_to_pdf)


def divide_string(string):
    words = string.split()

    phrases = list()

    for i in range(len(words)):
        for j in range(len(words)):
            l = len(words) - j
            phrases.append(words[i:l])

    # phrases = sorted(phrases, key=len)

    strings = list()

    for phrase in phrases:
        sentence = ""
        for word in phrase:
            sentence = sentence + word + ' '
        sentence = sentence[:-1]
        strings.append(sentence)

    strings = sorted(strings, key=len)

    indices = list()

    for i in range(len(strings)):
        if strings[i] == '':
            indices.append(i)

    strings = [i for j, i in enumerate(strings) if j not in indices]
    strings.reverse()
    srtings = strings.remove(string)

    return (strings)


def search_deeper(chapter, content):
    phrases = divide_string(chapter)

    for phrase in phrases:
        positions = [m.start() for m in re.finditer(phrase, content, flags=re.I)]
        if len(positions) > 1:
            break

    return (positions, phrase)


def possible_chapters_positions(structure, content):
    global_list = list()

    for chapter in structure:
        indicies = [m.start() for m in re.finditer(chapter, content, flags=re.I)]

        if indicies:
            global_list.append([[structure.index(chapter), chapter], indicies])
        else:
            indicies = search_deeper(chapter, content)[0]
            phrase = search_deeper(chapter, content)[1]
            global_list.append([[structure.index(chapter), phrase], indicies])

    for each in global_list:

        each_ind = global_list.index(each)

        while len(each[1]) == 1:
            chapter = each[0][1]
            each[1] = search_deeper(chapter, content)[0]
            each[0][1] = search_deeper(chapter, content)[1]

        global_list[each_ind] = each

    return (global_list)


print(*possible_chapters_positions(structure, content), sep="\n")

global_list = possible_chapters_positions(structure, content)

def insert(pos, lst):
    next = list()

    for each in lst:
        if pos < each:
            next.append(each)

    lst_new = [pos, next]

    return lst_new


print(insert(1410, [179, 884, 1418, 2670, 6666, 9102, 10967, 11443]))


def build_tree(global_list):

    tree = list()

    for chapter in global_list:
        if not tree:
            tree.append(chapter[1])
            parent = chapter[1]
            print(parent)
        else:
            for each in parent:
                each = insert(each, chapter[1])
                print(parent, each)

build_tree(global_list)
