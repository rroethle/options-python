from bs4 import BeautifulSoup #used to scrape data from url converted from requets
import requests #converts url page content into html DOM tree

#following 3 imports are for referencing dates and times. Since I used different
#To-Do: referencing throughout the document, I have some redundant calls that should be fixed
from datetime import date
import datetime
import time

#helps assist with path creation for output files.
import os.path
import os

#provides regular expression matching in an easier format.
from re import search
import re

#used for outputing data files.
import csv
import json

#globals that shouldn't change unless market_times change.
placeholder_time = datetime.datetime.now().time()
market_open = placeholder_time.replace(hour=8, minute=30, second=0, microsecond=0) 
market_close = placeholder_time.replace(hour=23, minute=0, second=0, microsecond=0)

'''
file checks for input errors using special characters.
'''
def checkFileName(input_text):
    #I don't want special characters in file names, this function checks for that.
    print input_text
    if re.match("^[A-Za-z0-9]+$",input_text):
        return True
    else:
        print "Value entered must not contain numbers, Please re-enter file name: "
        print input_text
        return False

def checkStockSymbol(stock_input):
    #checks to make sure stock symbol exists and asks user for a new value if it doesn't.
    try:
        print stock_input
        getLastUnderlyingPrice(stock_input)
        return True
    except:
        print "Stock doesn't exist, please re-enter valid stock symbol"
        return False


'''
will take in etf or stock name and if available on yahoo finance will collect full options 
expiration data by the minute for the closest upcoming expiration date. The program will run 
until market close. A CSV file is generated to my desktop folder named Options.
'''
def getOptionPrices(etfName,file_name):
    current_time = datetime.datetime.now().time()
    #checks to see if market is open. If it is creates paths for files and allows main loop to run.
    #else it will set currentEtfCompleted to True and main loop will not run because the market isn't open.
    if current_time >= market_open and current_time <= market_close:
        print "Market is Open. Data will start to collect."
        checkName = False
        if checkName == False:
            file_name = file_name
            checkName = checkFileName(file_name)
        #TO DO: path should be changed.
        #save_path = 'C:\\Users\\rroethle_he\\Desktop\\Options\\'
        save_path = ""
        completeNameCSV = os.path.join(save_path,file_name + ".csv")
        completeNameJSON = os.path.join(save_path,file_name + ".json")
        currentEtfCompleted = False
    else:
        print "Market is Closed, no data to collect."
        currentEtfCompleted = True
        dailyOptionsList = []
        return False
    #yahoo finance base url is used for creating options quotes.
    urlBase='http://finance.yahoo.com'
    #<TO DO> will use later to check later expiration dates - urlIndex
    urlIndex=0
    #-------------------------------begin url loop:-------------------------------------
    for i in range(1):
    #while currentEtfCompleted==False:
        #used to collect minute by minute snapshot of all the options expirations.
        dailyOptionsList = []
        current_time = datetime.datetime.now().time()
        if current_time >= market_open and current_time <= market_close:
            print "Market is Open. Data will start to collect."
            currentEtfCompleted = False
        else:
            print "Market is Closed, no data to collect."
            currentEtfCompleted = True
            return False
        if urlIndex==0:
            #creates suffix to navigate to closest options expiration page.
            urlSuffix=urlSuffix='/q/op?s='+etfName+'+Options'
            #updating urlIndex will hopefully allow me to check future options expiration dates.
            urlIndex=urlIndex+1
        #else: TO DO!!!!!! this is commented out because this will hopefully check for other options expiration dates
            #urlIndex=urlIndex+1
            #use the html from the previous loop to get the link for the next expiry month.
            #print('expiry month number '+str(urlIndex)+' is being scraped.')
            #currentMonth=maintd.find('strong')
            #get two siblings over.  It might be the next expiry month.  If string length is 6 (formatted ex. May 13) then it
            #is the next expiry month.
            #potentialNextMonth=maintd.find('strong').next_sibling.next_sibling
            #if potentialNextMonth.string is not None:
                #print('Current expiry month\'s URL is correct.')
                #print(potentialNextMonth['href'])
                #urlSuffix=potentialNextMonth['href']
            #else:
                #currentEtfCompleted=True
        #response will take the urlBase and suffice to use requests to generate tree of page.
        response=requests.get(urlBase+urlSuffix)
        results = response.content
        #soup uses BeautifulSoup to take the webpage we got from requests and allow us to use the data.
        soup=BeautifulSoup(results)
        mainTables=[' ',' ']
        #finds the two tabls labeled for calls and puts. May need to look at this in the future if Yahoo changes it.
        superParentsOfMainTables=soup.findAll('table',{'class':'details-table quote-table Fz-m'})
        #details-table quote-table Fz-m - this is the class yahoo uses for the tables.
        #TO DO I was unable to get the other dates but can review in the future.
        #maintd is used for referencing links to other expiry dates.
        #maintd=soup.find('table',{'class':'yfnc_mod_table_title1'}).parent
        #maintd=soup.find('table',{'class':'details-header quote-table-headers'}).parent
        #for i in range(2):
        #maintableholder = superParentsOfMainTables.
        #mainTables[0]=superParentsOfMainTables[0].find('tbody')
        #number_rows_calls = mainTables[0].findAll('tr')
        #table_length_rows = len(number_rows_calls)
        #mainTables[1]=superParentsOfMainTables[1].find('tbody')
            #mainTables[i]=superParentsOfMainTables[i].findAll('tbody')
        tableIndex=0
        #adds header row to results and appends.
        header_row = ["StockSymbol","Options Symbol", "Strike", "Expiration Date", "OptionType","Price","Bid","Ask","Volume","Open Interest"]
        optionsResults=[]
        optionsResults.append(header_row)
        #placeholders for option symbols and types.
        optionSymbol=' '
        optionType=' '
        last=0
        for tableIndex in range(2):
            #generates how many rows are in the calls and puts table to now how many rows to iterate over.
            tableLength=len(mainTables[tableIndex])
            mainTables[tableIndex]=superParentsOfMainTables[tableIndex].find('tbody')
            number_rows_calls = mainTables[tableIndex].findAll('tr')
            table_length_rows = len(number_rows_calls)
            print "Table Length Rows",table_length_rows
            for i in range(0,table_length_rows):
                #the loop starting on the above line is the loop iterating over all rows in the table.
                # 9 is hardcoded in because I am only interested in data up to the 8th row.
                for j in range(9):
                    if j==0:
                        #collects strike price - 1st column
                        try:
                            strike= float(mainTables[tableIndex].find_all('tr', limit = i+1)[-1].find_all('td', limit = j+1)[-1].contents[1].contents[0].string)
                        except:
                            print "Options do not exist for this stock. Re-enter new stock symbol: "
                            return 0
                    elif j==1:
                        #collects optionSymbol - 2nd column - generates stock symbol as well
                        optionSymbol=mainTables[tableIndex].find_all('tr', limit = i+1)[-1].find_all('td', limit = j+1)[-1].find('a').string
                        firstDigitPosition=search('\d',optionSymbol).start()
                        stockSymbol=optionSymbol[:firstDigitPosition]
                        #for most options, the option symbol will be len(stocksymbol)+14 characters long
                        #those are type 1 options.  However, some stocks have a second category of options
                        #(this category depends on the particular stock) with an extra 1 appended within
                        #the option symbol.  This becomes a type 2 option for this program's purposes.
                        #because of the extra character, characterBump is used to shift character pointers
                        #in the case of type 2 options.
                        if len(optionSymbol)==len(stockSymbol)+15:
                            #the option is a type 1 option in this case
                            specialType="type 1"
                            characterBump=0
                        elif len(optionSymbol)==len(stockSymbol)+16:
                            #the option is a type 2 option in this case
                            specialType="type 2"
                            characterBump=1
                        else:
                            print('option string not of the appropriate length.  quitting.')
                            quit()
                        #generates the expiration year, month, day, date, and option type letter from
                        #complete options call symbol.
                        expiryYear='20'+optionSymbol[firstDigitPosition+characterBump:firstDigitPosition+characterBump+2]
                        expiryMonth=optionSymbol[firstDigitPosition+characterBump+2:firstDigitPosition+characterBump+4]
                        expiryDay=optionSymbol[firstDigitPosition+characterBump+4:firstDigitPosition+characterBump+6]
                        expiryDate=date(int(expiryYear),int(expiryMonth),int(expiryDay))
                        if optionSymbol[firstDigitPosition+characterBump+6]=='C':
                            optionType='Call'
                        if optionSymbol[firstDigitPosition+characterBump+6]=='P':
                            optionType='Put'
                    elif j==2:
                        #collects current price - 3rd column
                        price = mainTables[tableIndex].find_all('tr', limit = i+1)[-1].find_all('td', limit = j+1)[-1].contents[1].string
                    elif j==3:
                        #collects bid price - 4th column
                        bid = mainTables[tableIndex].find_all('tr', limit = i+1)[-1].find_all('td', limit = j+1)[-1].contents[1].string
                    elif j==4:
                        #collects ask price - 5th column
                        ask = mainTables[tableIndex].find_all('tr', limit = i+1)[-1].find_all('td', limit = j+1)[-1].contents[1].string
                    elif j==7:
                        #collects volume - 8th column
                        volume = mainTables[tableIndex].find_all('tr', limit = i+1)[-1].find_all('td', limit = j+1)[-1].find('strong').contents[0].string
                    elif j==8:
                        #collects open interest - 9th column
                        open_interest = mainTables[tableIndex].find_all('tr', limit = i+1)[-1].find_all('td', limit = j+1)[-1].contents[1].string
                #appends all of the results collected as one list item      
                appendedResults=[stockSymbol,optionSymbol, strike, expiryDate, optionType,price,bid,ask,volume,open_interest]#, last, dailyValueChange, specialType]
                #list of all things that should be appended into optionsresults:          
                optionsResults.append(appendedResults)
        #appends all results to daily collection file
        dailyOptionsList.append(optionsResults)
        #creates csv file with name given above
        with open(completeNameCSV,"wb") as output_file:
            writer = csv.writer(output_file)
            writer.writerows(dailyOptionsList)
            output_file.close()
        #TO DO fix JSON Output
        #with open(completeNameJSON,"wb") as outfile:
            #json.dump(dailyOptionsList,outfile)
        #sleeps file for 60 seconds so it collect data every minute
        time.sleep(60)
    print('Options have completed generating.')
    return dailyOptionsList

'''
takes in stock symbol from user and returns underlying price from yahoo
'''
def getLastUnderlyingPrice(symbol):
    #using stock symbol, gets last underlying price.
    urlBase='http://finance.yahoo.com/q?s='
    response=requests.get(urlBase+symbol)
    results = response.content
    soup=BeautifulSoup(results)
    superParent=soup.find('span',{'class':'time_rtq_ticker'})
    forDate=superParent.parent.contents[4]
    date=forDate.contents[1].string
    print('------------------------')
    print('Valid Stock Symbol')
    price=float(superParent.contents[0].string)
    print (symbol + "   " + str(price))
    return [price, date]

def display_header():
        os.system('cls')
        print ""
        print "{0:^60}".format("Options Market Data Collector")
        print "==============================================================="
        print "If your stock trades options, enter a stock symbol below and "
        print "have this program collect data on this current month's options"
        print "BY THE MINUTE! Data is returned via csv file. Data collected "
        print "values are Options Call or Put Symbol, Expiration Date, Current"
        print "Price, Bid, Ask, Volume, and Open Interest."
        print "======================================================"
        print ""


#main function for running program and collecting data
#if __name__ == '__main__':
    #enter_stock_symbol = False
#     display_header()
#     while enter_stock_symbol == False:
#         user_input = raw_input("Please enter stock symbol interested in tracking? ")
#         enter_stock_symbol = checkStockSymbol(user_input)
#         if enter_stock_symbol == True:
#             end_result = getOptionPrices(user_input)


