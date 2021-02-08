import matplotlib as mpl
import matplotlib.pyplot as plt
import PySimpleGUI as gui
import re
import math
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
mpl.use('TkAgg')

while True:
	window = gui.Window(title="Calculus", layout=[[gui.Text("Calculus Viewer", font=["",25])],
												  [gui.Text("This is a program to that allows you to visualise differentiation and definite integration problems on a graph.")],
												  [gui.Text("It is intended to be used as a revision resource for students, or can be used by teachers to show how calculus works on a graph.")],
												  [gui.Button("Start")]], element_justification='center')
	window.read()
	window.close()
	
	
	while True:
		window2 = gui.Window(title="Calculus", layout=[[gui.Text("Please select if you want to visualise Diffferentiation or Integration")],
													  [gui.Radio("Differentiation", "selection", key='-SEL-'), gui.Radio("Integration", "selection",)],
													  [gui.Text("Please Enter Your Equation (example input: 5x^2-3x+6)")],
													  [gui.Input(key='-EQ-')],
													  [gui.Button("Go")],
													  [gui.Canvas(key='-CANVAS-')],
													  [gui.Text("                                                  ",key='-ANSLAB-', enable_events=False)],
													  [gui.Text("                                                  ", font=["", 20],key='-ANSFIN-', enable_events=False)],
													  [gui.Text("                                                  ",key='-WKDLAB-', enable_events=False)],
													  [gui.Button("Click to view", key='-WKDBTN-', visible=False)],
													  [gui.Button("Solve Another", key='-RPT-', visible=False)]], element_justification='center')
	
		event, values = window2.read()
		if values['-EQ-'] == "":
		  gui.Popup("No Equation entered, please enter an equation")
		  window2.finalize()
		  window2.Close()
		  break
		EQ = values['-EQ-']
		check = re.match('^(([\+\-]?\d*\/?\d*x?\^?[\+\-]?\d*\/?\d*))+$', EQ)
		if bool(check) == False:
			gui.popup("Please Enter a Valid equation")
			window2.finalize()
			window2.Close()
			break
		Selection = values['-SEL-']
		Equation = re.sub('\s*((?<=((\+|-)))|^)\s*x', '1x', values['-EQ-']) #REGEX to add 1 to any x with no coefficient
		Equation = re.sub('\s*x(?!\^)', 'x^1', Equation) #REGEX to add x^1 to any x with no exponent
		if bool(re.match('\d$', Equation)) == False:
			Equation = Equation + "x^0"
		coefficient = [] #creates empty list to add the coefficients to
		exponent = []    #creates empty list to add the exponents to
		newcoeff = []
		newexp = []
		UL = 0.0
		LL = 0.0
		
		if Selection == False: # Integration
			window3 = gui.Window(title="Integral Limiters", layout=[[gui.Text("Please enter upper and lower bounds to integrate between")], [gui.Text("Lower Limit:"), gui.Input(key='-LL-', size=(20,20)), gui.Text("Upper Limit"), gui.Input(key='-UL-', size=(20,20))], [gui.Button("Go")]])
			event, values = window3.read()
			window3.finalize()
			window3.close()
			UL = float(values['-UL-'])
			LL = float(values['-LL-']) # displays a window asking for an upper and lower bound for definite integration
		def Split():
			if Selection == False: # Integration
				coeffpattern = '\s*(^|(\+|-))\s*\d+([\.\/]\d+)?\s*((?=x)|$)' #checked and works with fractions
			else:
				coeffpattern = '\s*(^|(\+|-))\s*\d+([\.\/]\d+)?\s*((?=x))' #checked and works with fractions 
			coeff = re.finditer(coeffpattern, Equation, re.MULTILINE) #REGEX to find every number before an x but after an exponent
			exp = re.finditer('\s*(?<=x\^)\s*[\+-]*\s*\d+([\.\/]\d+)?', Equation, re.MULTILINE)  #REGEX to find every exponent after a ^ symbol but before the next coefficient 
			for matchnum, match in enumerate(coeff, start=1):
				coefficient.append(match.group()) #takes all coefficients from the equation and appends them to the coefficients list	
			for matchnum, match in enumerate(exp, start=1):
				exponent.append(match.group()) #takes all exponents from the equation and appends them to the exponents list
	
		def Differentiation():
				
			for i in range(0, len(coefficient)):
				newcoeff.append(float(coefficient[i]) * float(exponent[i])) # multiplies the coefficient by its corrosponding exponent to get the new coefficient
				if newcoeff[i] == math.floor(newcoeff[i]):
					newcoeff[i] = int(newcoeff[i]) # checks if the coefficient could be better represented by an integer and converts if it can
				if (float(exponent[i]) > 0):  # makes sure the expoent is not 0
					newexp.append(float(exponent[i]) - 1) # adds one to the exponent and sets it to the new exponent
					if newexp[i] == math.floor(newexp[i]):
						newexp[i] = int(newexp[i]) # checks if the exponent could be better represented by an integer and converts if it can
				elif (float(exponent[i]) < 0): # makes sure the expoent is not 0
					newexp.append(float(exponent[i]) - 1) # adds one to the exponent and sets it to the new exponent
					if newexp[i] == math.floor(newexp[i]):
							newexp[i] = int(newexp[i]) # checks if the exponent could be better represented by an integer and converts if it can
								
		def Integration():
			for i in range(0, len(coefficient)):
				newcoeff.append(float(coefficient[i]) / (float(exponent[i]) + 1)) # increses exponent and divides the coefficient by the new exponent
				if newcoeff[i] == math.floor(newcoeff[i]):
					newcoeff[i] = int(newcoeff[i]) # checks if the coefficient could be better represented by an integer and converts if it can
				newexp.append(float(exponent[i]) + 1) # increses the exponent by one
				if newexp[i] == math.floor(newexp[i]):
					newexp[i] = int(newexp[i]) # checks if the exponent could be better represented by an integer and converts if it can
	
		def FinalAnswer():
		
			if Selection == True: # Differentiation
				answer = ""
				for i in range(0, len(newexp)):
					if (newcoeff[i] > 0) and (i > 0):
						answer += "+" + str(np.round(newcoeff[i], 8)) + "x^" + str(newexp[i]) # formats the answer for differentiation so it displays in the same format as the input
					else:
						if (newexp[i] != 0):
							answer += str(newcoeff[i]) + "x^" + str(newexp[i])
						else:
							answer += str(newcoeff[i])
							answer = re.sub('\s*\^[10]', "", answer)
				return answer
			else:
				answer = 0.0
				upper = 0.0
				lower = 0.0
				for i in range(0, len(newexp)):
					if newexp[i] != 1:
						upper += newcoeff[i] * (UL ** newexp[i]) # calculates the upper limit for the equation
						lower += newcoeff[i] * (LL ** newexp[i]) # calculates the lower limit for the equation
					else:
						upper += newcoeff[i] * UL # just multiplies the coefficient by the limit if the exponent is 1
						lower += newcoeff[i] * LL
				answer = upper - lower # calculates the final answer by taking the lower from the upper
				if float(answer) == math.floor(answer):
					answer = int(answer) # checks if the answer is better represented as an integer and converts if it can
				return np.round(answer, 4)
		
		Split()
		def fractions(fraction):
			parts = fraction.split("/")
			return float(parts[0]) / float(parts[1]) # handles any division within the calculation
		
		if Selection == False: # Integration
			for i in range(0, len(coefficient) - 1): # Detects if there is a fraction anywhere
				if "/" in coefficient[i]:
					coefficient[i] = fractions(coefficient[i])
				if "/" in exponent[i]:
					exponent[i] = fractions(exponent[i])
		else: # Differentiation
				for i in range(0, len(coefficient)): # Detects if there is a fraction anywhere but this time without minusing 1
					if "/" in coefficient[i]:
						coefficient[i] = fractions(coefficient[i])
					if "/" in exponent[i]:
						exponent[i] = fractions(exponent[i])
		
		if Selection == True: # Calls Differentiation() if Differentiation was selected
			Differentiation()
		elif Selection == False: # Calls Integration() if Integration was selected
			Integration()
		
	
		eq = ""
		def Formatting(inp):
			eq = str(inp).replace("x", "*x") # formats the equation so when you use eval() in it, it will be able to be graphed
			eq = eq.replace("^","**")
			return str(eq)
			
	
		if (Selection == True): # Differentiation
			fig = plt.figure()
			plt.grid(True)
			x = np.linspace(-100,100,100) # creates x values to plot
			y1 = eval(str(Formatting(FinalAnswer()))) # the differentiated graph
			y2 = eval(str(Formatting(Equation))) # the original graph
			plt.plot(x, y1) # drawing the data to the graph
			plt.plot(x, y2)
		else: # Integration
			fig = plt.figure()
			plt.grid(True)
			x = np.linspace(LL - 20, UL + 20, 100) # creating dynamic x values based on the entered limits
			y = eval(str(Formatting(Equation))) # the original graph
			plt.plot(x,y) # draws the data to the graph
			xbounds = np.linspace(LL, UL, 100) # the region to highlight
			XU = np.ma.masked_greater(x, UL) # masks the data so it fits to the original graph
			XL = np.ma.masked_less(XU, LL)
			plt.fill_between(XL, y) # highlights between the curve and y=0 between the limits entered
			plt.xlim(LL - 10, UL + 10)
			plt.ylim()
		
	
	
		def embedgraph(canvas, figure): # takes the graph stored in fig and draws it to the canvas in the GUI.
			fig_canv_agg = FigureCanvasTkAgg(figure, canvas)
			fig_canv_agg.draw()
			fig_canv_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
			return fig_canv_agg
		
	
	
		fig_canv_agg = embedgraph(window2['-CANVAS-'].TKCanvas, fig) # adds the graph to the existing window
		window2['-ANSLAB-'].Update("Final Answer:")
		window2['-ANSFIN-'].Update(FinalAnswer()) # adds the final answer to the existing window
		window2['-WKDLAB-'].Update("Worked Answer:")
		window2['-WKDBTN-'].Update(visible=True) # adds a button to view the worked answer to the existing window
		window2['-RPT-'].Update(visible=True)
		
		event, values = window2.read()
		
		
		if event == '-WKDBTN-':
		
			if Selection == True: # differentiation
				window4 = gui.Window(title="Worked Answer", layout=[[gui.Text("Differentiation")],
																	[gui.Text("Differentiating " + EQ)],
																	[gui.Text("Pair exponents and coefficients together")],
																	[gui.Text("Coefficients: " + str(coefficient))],
																	[gui.Text("Exponents: " + str(exponent))],
																	[gui.Text("Multiply together the pairs of exponents and coefficients to make the new coefficients.")],
																	[gui.Text("New coefficients: " + str(np.round(newcoeff, 4)))],
																	[gui.Text("ecrease each of your exponents by one")],
																	[gui.Text("New exponents: " + str(np.round(newexp, 4)))],
																	[gui.Text("Recombine the new coefficients and exponents into one equation:")],
																	[gui.Text(FinalAnswer())]])
			else: # integration
				window4 = gui.Window(title="Worked Answer", layout=[[gui.Text("Integration")],
																	[gui.Text("Integrating " + EQ + " between " + str(LL) + " and " + str(UL))],
																	[gui.Text("Pair exponents and coefficients together")],
																	[gui.Text("Coefficients: " + str(coefficient))],
																	[gui.Text("Exponents: " + str(exponent))],
																	[gui.Text("Increase exponents by one")],
																	[gui.Text("New exponents: " + str(np.round(newexp, 4)))],
																	[gui.Text("Divide coefficients by the new exponents")],
																	[gui.Text("New coefficients: " + str(np.round(newcoeff, 4)))],
																	[gui.Text("Recombine the new coefficients and exponents into one equation")],
																	[gui.Text("Substitute your upper and lower bounds for x")],
																	[gui.Text("Take your equation for the lower bound and take it away from the equation for the upper bound")],
																	[gui.Text("Area under the curve " + str(EQ) + " between " + str(LL) + " and " + str(UL) + " is " + str(FinalAnswer()))]])
			window4.Finalize()
			window4.read()
			event, values = window2.read()
			window2.close()
		elif event == '-RPT-':
			temp = 0
			temp = temp
		else:
			exit()

	