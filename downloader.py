import requests
import bs4
from bs4 import BeautifulSoup



class Pdf_table:
    def __init__(self, graduate, faculty_name, spec_code, spec_name, course_value, group_name, link):
        self.graduate = graduate
        self.faculty_name = faculty_name
        self.spec_code = spec_code
        self.spec_name = spec_name
        self.course_value = course_value
        self.group_name = group_name
        self.link = link


try:
    full_time_page = requests.get(
        'https://www.vyatsu.ru/studentu-1/spravochnaya-informatsiya/raspisanie-zanyatiy-dlya-studentov.html')
    # url ='https://www.vyatsu.ru/studentu-1/spravochnaya-informatsiya/raspisanie-zanyatiy-dlya-studentov.html'
    # full_time_page = open('test.html', 'r')
    soup = BeautifulSoup(full_time_page.text, 'html.parser')
    rasp = soup.find('div', attrs={'class': 'column-center_rasp'})
    RASP_CONTENT = rasp.findAll('div', recursive=False)
    pdf_table = []
    for each in range(len(RASP_CONTENT)):
        # graduate = ''
        # faculty_name = ''
        if type(RASP_CONTENT[each]) is not bs4.NavigableString:
            if (RASP_CONTENT[each].attrs is not None) and (RASP_CONTENT[each].attrs != {}):###
                if RASP_CONTENT[each].attrs['class'][0] == 'headerEduPrograms':
                    graduate = RASP_CONTENT[each].text
                    rasp_table = rasp.contents[each*6 + 4]
                    grad_table = rasp_table.contents[3].findAll('td', attrs={'style': 'border: none !important;'})
                    for i in grad_table:
                        if getattr(i, 'contents'):
                            faculty_name = i.contents[1].text
                            if len(i.contents) >= 4:
                                fac = i.contents[3].contents[1].contents[1].findAll('tr', recursive=False)
                                for j in fac:
                                    if j.find(attrs={'colspan': '2'}) is not None:  # if string ['06.03.01', 'Biology']
                                        spec_code, spec_name = j.next.next.text.split(maxsplit=1)
                                    else:
                                        course_value = j.find('td', attrs={'align': 'center'}).text.split()[1]
                                        one_course_groups = j.contents[3].contents[1].findAll('tr', recursive=False)
                                        for k in one_course_groups:
                                            if k.find(attrs={'style': 'width: 220px; border: none !important;'}) is None:
                                                one_row = k.findAll(
                                                    attrs={'style': 'border: none !important; vertical-align: top;'})
                                                for l in one_row:
                                                    one_cell = l.findAll('div')
                                                    if one_cell:
                                                        group_name = l.findAll('div')[0].text.split()[0]
                                                    else:
                                                        continue
                                                    link = l.findAll('div')[1].findAll('a')[0].attrs['href']
                                                    ###init class
                                                    pdf_table.append(
                                                        Pdf_table(graduate, faculty_name, spec_code, spec_name, course_value,
                                                                  group_name, link))

                                                    print('pdf_table consist {0} items'.format(len(pdf_table)))

                    print('')
except requests.RequestException:
    print('Something wrong, perhabs with vyatsu, not with your script, ofc')

print('')
