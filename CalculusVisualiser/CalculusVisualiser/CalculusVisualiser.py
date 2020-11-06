import matplotlib.pyplot as plt
import matplotlib as mpl
import PySimpleGUI as gui
import re
import math
mpl.use('TkAgg')

  

window = gui.Window(title="Calculus", layout=[[gui.Text("Please select if you want t ovisualise Diffferentiation or Integration")],
											  [gui.Radio("Differentiation", "selection", key='-SEL-'), gui.Radio("Integration", "selection",)],
											  [gui.Text("Please Enter Your Equation (example input: 5x^2-3x+6)")],
											  [gui.Input(key='-EQ-')],
											  [gui.Button("Go")],
											  [gui.Text("###PLACE GRAPH HERE###")],
											  [gui.Text("Worked Solution:")],
											  [gui.Text("###PLACE WORKED SOLUTION HERE###")],
											  [gui.Text("Final Answer:")],
											  [gui.Text("###PLACE ANSWER HERE###")],
											  [gui.Text("###PLACE SOLVED GRAPH HERE###")]], margins=(500,300))

event, values = window.read()
window.close
gui.Popup(values['-SEL-'], values['-EQ-'])

def Split():
	if Selection == False:
		coeffpattern = '\s*(^|(\+|-))\s*\d+(.\d+)?\s*((?=x)|$)'
											  



Selection = values['-SEL-']
Equation = re.sub('\s*((?<=((\+|-)))|^)\s*x', '1x', values['-EQ-']) #REGEX to add 1 to any x with no coefficient
Equation = re.sub('\s*x(?!\^)', 'x^1', Equation) #REGEX to add x^1 to any x with no exponent
gui.Popup(Equation)

coefficient = [] #creates empty list to add the coefficients to
exponent = []    #creates empty list to add the exponents to
newcoeff = []
newexp = []
FL = ""
LL = ""

if Selection == False:
	window2 = gui.Window(title="Calculus", layout=[[gui.Text("Integrate between: ")], [gui.Text("First Limit: "), gui.Input(key='-FL-'), gui.Text("Last Limit: "), gui.Input(key='-LL-')], [gui.Button("Go")]])
	event, values = window2.read()
	FL = values['-FL-']
	LL = values['-LL-']
else:
	coeffpattern = '\s*(^|(\+|-))\s*\d+(.\d+)?\s*((?=x))'

coeff = re.finditer(coeffpattern, Equation, re.MULTILINE) #REGEX to find every number before an x but after an exponent
exp = re.finditer('\s*(?<=x\^)\s*(\+|-)*\s*\d+(\.\d+)?', Equation, re.MULTILINE)  #REGEX to find every exponent after a ^ symbol but before the next coefficient

for matchnum, match in enumerate(coeff, start=1):
	coefficient.append(match.group()) #takes all coefficients from the equation and appends them to the coefficients list
for matchnum, match in enumerate(exp, start=1):
	exponent.append(match.group()) #takes all exponents from the equation and appends them to the exponents list
print (coefficient, exponent)

def fractions(fraction):
	parts = fraction.split("/")
	return float(parts[0]) / float(parts[1])

	for i in range(0, len(coefficient) - 1):
		if "/" in coefficient[i]:
			coefficient[i] = fractions(coefficient[i] - 1)
	if "/" in exponent[i]:
		exponent[i] = fractions(exponent[i])
	gui.popup(coefficient, exponent)

def Differentiation():

	for i in range(0, len(coefficient)):
		newcoeff.append(float(coefficient[i]) * float(exponent[i]))
		if newcoeff[i] == math.floor(newcoeff[i]):
			newcoeff[i] = int(newcoeff[i])
		newexp.append(float(exponent[i]) - 1)
		if newexp[i] == math.floor(newexp[i]):
			newexp[i] = int(newexp[i])
	gui.Popup(newcoeff, newexp)

def Integration():
	for i in range(0, len(coefficient) - 1):
		newcoeff.append(float(coefficient[i]) / float(exponent[i]) + 1)
		if newcoeff[i] == math.floor(newcoeff[i]):
			newcoeff[i] = int(newcoeff[i])
		newexp.append(float(exponent[i]) + 1)
		if newexp[i] == math.floor(newexp[i]):
			newexp[i] = int(newexp[i])
	gui.Popup(newcoeff, newexp)

def FinalAnswer():
	answer = ""
	for i in range(0, len(newexp)):
		if (newcoeff[i] > 0) and (i > 0):
			answer += "+" + str(newcoeff[i]) + "x^" + str(newexp[i])
		else:
			answer += str(newcoeff[i]) + "x^" + str(newexp[i])
	answer = re.sub('\s*\^[10]', "", answer)
	answer = re.match('^.*(?=.$)', answer)
	gui.Popup(answer.group(0))


Split()
if Selection == True:
	Differentiation()
elif Selection == False:
	Integration()

FinalAnswer()

plt.show(block=True)
plt.interactive(False)
