# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import urllib.request
import re
import tinycss
from typing import Dict


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def read_file(name):
    with open(name, 'r') as f:
        return f.readlines()


def write_file(name, content):
    with open(name, 'w') as f:
        f.write(content)


def test():
    d = dict()
    print(is_comment_or_empty('/*hj>>>**/ '))
    print(parse_selector('aaa dsafadfb,ghghc{  '))
    p = SimpleCssParser()
    c = read_file('assets/short.css')
    p.parse(c)
    for k in p.d.keys():
        print(k)
        print(str(p.d.get(k)))


def is_comment_or_empty(string) -> bool:
    s = string.strip()
    return s[:2] == '/*' and s[-2:] == '*/' or s == ''


def is_comment(string) -> bool:
    s = string.strip()
    return s[:2] == '/*' and s[-2:] == '*/'


def parse_selector(string):
    s = string.strip()
    if s[-1:] == '{':
        return s[:-1].strip()
    else:
        return ''


def bracket(string):
    s = string.strip()
    if s[-1:] == '}':
        return -1
    elif s[-1:] == '{':
        return 1
    else:
        return 0


def parse_css(lines):
    d = dict()
    unknown = list()
    for l in lines:
        if is_comment_or_empty(l):
            continue
        else:
            sel = parse_selector(l)
            if sel == '':
                unknown.append(l)
            else:
                if sel not in d:
                    d[sel] = []


class CssParser(object):
    def __init__(self):
        self.d = dict()
        self.unknown = list()
        self.bracketCount = 0
        self.tmpStyle = ''
        self.tmpSel = ''

    def parse(self, lines):

        for aline in lines:
            if is_comment_or_empty(aline):
                continue
            elif self.bracketCount > 0:
                self.bracketCount += bracket(aline)
                if self.bracketCount > 0:
                    self.tmpStyle += aline
                    pass  # continue parse
                else:
                    pass  # save style
            else:
                sel = parse_selector(aline)
                if sel == '':
                    self.unknown.append(aline)
                else:
                    if sel not in self.d:
                        self.d[sel] = []
                    self.tmpSel = sel
                    self.bracketCount = 1
                    self.tmpStyle = ''


class SimpleCssParser(object):
    def __init__(self):
        self.d = dict()
        self.tmpStyle = ''

    def parse(self, lines):

        for aline in lines:
            if is_comment(aline):
                continue
            saline = aline.strip()
            if saline != '':
                self.tmpStyle += saline
            elif self.tmpStyle != '':
                if self.tmpStyle not in self.d:
                    self.d[self.tmpStyle] = list()
                self.d.get(self.tmpStyle).append(self.tmpStyle)
                self.tmpStyle = ''


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

    run = True

    if run:

        after = SimpleCssParser()
        after.parse(read_file('assets/after_main.css'))
        before = SimpleCssParser()
        before.parse(read_file('assets/before_main.css'))

        with open('matchlog.txt', 'w') as f:
            notfound=''

            notfound += 'before:'
            for k in before.d.keys():
                arr = before.d.get(k)
                for i in arr:
                    if i in after.d:
                        if i in after.d.get(i):
                            f.write('match: before: ' + i + '\n')
                        else:
                            notfound += i+'\n'
                    else:
                        notfound += i+'\n'
            notfound += '\n\nafter:'
            for k in after.d.keys():
                arr = after.d.get(k)
                for i in arr:
                    if i in before.d:
                        if i in before.d.get(i):
                            f.write('match: after: ' + i + '\n')
                        else:
                            notfound += i+'\n'
                    else:
                        notfound += i+'\n'
        write_file('notfound.txt', notfound)
    else:
        test()

    # resp = urllib.request.urlopen('https://wwww.baidu.com')
    # html = resp.read().decode()
    # rr = re.compile(r'\'[^\']*\.png\'')
    # pngList = rr.findall(html)
    # for png in pngList:
    # print(png)
    # urllib.request.urlopen(png)
    # an object is an instance of a class.

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
