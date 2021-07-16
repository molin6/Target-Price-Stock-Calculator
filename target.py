import requests 
import bs4
import tkinter as tk 

EPS_Actual = []
EPS_Estimate = []
price = []

window = tk.Tk()
title = tk.Label(text = "Target Price Calculator ", fg = "purple", width = 40, height = 1)

first_label = tk.Label(text = "Enter Stock Ticker: ",fg = "purple", width = 40, height = 3)
tickers = tk.Entry()
Results = tk.Label(text = "Target Price: ", fg = "purple")


title.pack()
first_label.pack()
tickers.pack()
Results.pack()


def GO():


	for i in tickers:
		try:
			r = requests.get("https://finance.yahoo.com/quote/" + i + "/analysis?p=" + i).text
			soup = bs4.BeautifulSoup(r, "lxml")
			EPS = soup.findAll("td", class_="Ta(end)")

			EPS = EPS[48].get_text()
			EPS_Actual.append(EPS)


			EST = soup.findAll("td", class_="Ta(end)")

			EST = EST[60].get_text()
			EPS_Estimate.append(EST)


			Price = soup.find("span", class_="Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)")
			price.append(Price.get_text())
		except:
			tk.Label(window, text= "Unable to find {} ".format(i) ,width= 50, height = 5,fg = "red").pack()
			window.update()




	for actual, estimate, PRICE, tick in zip(EPS_Actual, EPS_Estimate, price, tickers):
		if actual != 'N/A':
			actual = float(actual)
		if estimate != 'N/A':
			estimate = float(estimate)
		if PRICE != 'N/A':
			PRICE = float(PRICE)
		try:
			target = (PRICE * ((PRICE*actual)/(PRICE*estimate)))
		

			tk.Label(window, text= "The target price for {} is {}".format(tick, target) ,width= 40, height = 5, fg = "green").pack()
			window.update()


		except:
			tk.Label(window, text= "Unable to find {} ".format(tick) ,width= 50, height = 5,fg = "red").pack()
			window.update()

	
def SUBMIT():
	global tickers
	tickers = tickers.get()
	tickers = [tickers]
	print(tickers)
	GO()

button = tk.Button(text = "Find ", fg = "purple",command = SUBMIT, width = 25)
button.pack()

window.mainloop()
