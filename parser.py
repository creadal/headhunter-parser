import urllib.request
import xlsxwriter
from html.parser import HTMLParser

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
    # Print New Line on Complete
    if iteration == total: 
        print()

class VacancyLinksParser(HTMLParser):
    list_of_links = []

    def handle_starttag(self, tag, attrs):
        if tag == 'a' and ('data-qa', 'vacancy-serp__vacancy-title') in attrs:
            for name, value in attrs:
                if name == 'href':
                    self.list_of_links.append(value)


parser = VacancyLinksParser()

print('Searching for vacancies:')

for i in range(0, 1):
    response = urllib.request.urlopen('https://spb.hh.ru/search/vacancy?items_on_page=100&text=UI+UX')
    html = response.read()
    html = html.decode('utf-8')


    parser.feed(html)
    parser.reset()

    printProgressBar(i, 1, prefix = 'Progress:', suffix = 'Complete', length = 50)

class VacancyPagesMiner(HTMLParser):
    list_of_skills = {}

    def handle_starttag(self, tag, attrs):
        if tag == 'span' and ('data-qa', 'skills-element') in attrs:
            for name, value in attrs:
                if name == 'data-tag-id':
                    if value in self.list_of_skills:
                        self.list_of_skills[value] += 1
                    else:
                        self.list_of_skills[value] = 1


print(parser.list_of_links)

miner = VacancyPagesMiner()

leng = len(parser.list_of_links)
print(leng)
i = 0

print("Processing vacancies:")
for link in parser.list_of_links:
    i+=1

    response = urllib.request.urlopen(link)
    html = response.read()
    html = html.decode('utf-8')

    miner.feed(html)
    miner.reset()

    printProgressBar(i, leng, prefix = 'Progress:', suffix = 'Complete', length = 50)

workbook = xlsxwriter.Workbook('demo.xlsx')
worksheet = workbook.add_worksheet()

l = len(miner.list_of_skills)

for i in range(l):
    values = list(miner.list_of_skills.values())
    keys = list(miner.list_of_skills.keys())

    worksheet.write(i, 0, keys[i])
    worksheet.write(i, 1, values[i])

workbook.close()