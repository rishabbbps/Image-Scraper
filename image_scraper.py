import urllib
opener = urllib.FancyURLopener()
import re
import mechanize
import cookielib
from BeautifulSoup import BeautifulSoup

number1 = input("Starting Page : ")
number = input("Last Page : ")

br = mechanize.Browser()

cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

# Browser options
br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

br.addheaders = [('User-agent', 'Chrome')]

# The site we will navigate into, handling it's session
br.open('https://login-page-of-the-website')

# Select the second (index one) form (the first form is a search query box)
br.select_form(nr=2)
# br.select_form(name="sign-in")
# User credentials
br.form['email'] = 'username'
br.form['password'] = 'password'

# Login
br.submit()
print 'Logged in successfully'
for i in range(number1, number+1):
    str1= "https://website-to-scrape" + str(i)
    print str1
    RR = br.open(str1)
    html = RR.read()
    soup = BeautifulSoup(html)
    table = soup.find('table', {'class': 'products-table'})
    for row in table.findAll('tr')[1:]:
        link=[]
        cols = row.findAll('td')
        link = cols[1].find('a').get('href')
        print link
        R1 = br.open(link)
        html1 = R1.read()
        soup1 = BeautifulSoup(html1)
        images = soup1.findAll("img")
        for j in range(2, len(images)-1):
            li = soup1.findAll('img')[j].get('src')
            print li
            filename = str(soup1.find('div', attrs={'class': 'product-desc'}).h1)
            filename =  filename[4:len(filename)-5] + str(j)
            final_name = re.sub('[^A-Za-z0-9]+', '', filename)
            final_name = 'pg' + str(i) + '-' + final_name + '.jpg'
            print final_name
            urllib.urlretrieve(li, final_name)
