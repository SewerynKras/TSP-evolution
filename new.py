import matplotlib
matplotlib.use('module://kivy.garden.matplotlib.backend_kivy')
from matplotlib.figure import Figure
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.garden.matplotlib import FigureCanvasKivyAgg
import matplotlib.pyplot as plt
import Evolution
import asyncio
fig = plt.figure()
canvas = fig.canvas
best = []
aver = []
worst = []

#What the fck


class EvolutionSimulator(App):
	title = "Evolution Simulator!"
	def build(self):
		self.target = "Design must be simple."
		self.population = Evolution._firstPopulation(100,self.target)
		self.population = Evolution._ratePopulation(self.population,self.target)
		main_layout = BoxLayout(orientation="vertical")
		self.label = Label(size_hint=[0.9,1])
		btn1 = Button(text="Start",size_hint = [.1,1])
		#btn10 = Button(text="Jump 10",size_hint = [.1,1])
		#btn100 = Button(text="Jump 100",size_hint = [.1,1])
		box = BoxLayout(padding = 10, size_hint = [1,.1])
		btn1.bind(on_press=lambda a:self.refresh())
		#btn10.bind(on_press =lambda a:self.refresh())
		#btn100.bind(on_press =lambda a:self.refresh())
		box.add_widget(btn1)
		#box.add_widget(btn10)
		#box.add_widget(btn100)
		box.add_widget(self.label)
		main_layout.add_widget(box)
		main_layout.add_widget(canvas)
		#canvas.draw_idle()
		return main_layout

	def refresh(self):
		global generation,best,aver,worst
		while self.population[0][1] != len(self.target):
			self.population = Evolution.evolvePopulation(population = self.population,Target = self.target)
			best.append(self.population[0][1])
			aver.append(self.population[int(len(self.population)/2)][1])
			worst.append(self.population[len(self.population)-1][1])
			#print(self.population[0][1])
			#self.plotGraph(best,aver,worst,len(best))
			self.label.text = "Generation:{} Best: {}".format(len(best),self.population[0][0])
	#@asyncio.coroutine
	def plotGraph(self,best=[],aver=[],worst=[],generation=0):
		fig.clf()
		axes = fig.add_axes([0.1,0.1,0.9,0.9])
		axes.set_xlabel("Generation")
		axes.set_ylabel("Points")
		self.label.text = "Generation:{} Best: {}".format(generation,self.population[0][0])
		axes.plot(range(generation),best, label = "Best", color = "#4DE289",lw=5)
		axes.plot(range(generation),aver, label = "Average", color = "#E8FF26",lw=5)
		axes.plot(range(generation),worst, label = "Worst", color = "#DF1F1F",lw=5)
		#canvas.draw_idle()

if __name__ == '__main__':
	EvolutionSimulator().run()