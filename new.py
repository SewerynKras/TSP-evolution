import matplotlib
matplotlib.use('module://kivy.garden.matplotlib.backend_kivy')
from matplotlib.figure import Figure
from kivy.app import App
from kivy.utils import get_hex_from_color
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.garden.matplotlib import FigureCanvasKivyAgg
import matplotlib.pyplot as plt
import Evolution
from kivy.clock import Clock

class EvolutionSimulator(App):

	title = "Evolution Simulator!"

	def build(self):
		self.population = []
		self.fig = plt.figure()
		self.canvas = self.fig.canvas
		self.best = []
		self.aver = []
		self.worst = []
		main_layout = BoxLayout(orientation="vertical")
		self.gen_label = Label(markup = True)
		self.best_label = Label(markup = True)
		self.score_label = Label(markup = True)
		self.input = TextInput(text="Design must be simple. Elegant. Implementation, less so.")
		start = Button(text="Start",size_hint = [.1,1])
		self.stop = Button(text="Stop",size_hint = [.1,1])
		box = BoxLayout(padding = 10, size_hint = [1,.1])
		box2 = BoxLayout(padding = 10, size_hint = [1,.1])
		start.bind(on_press=lambda a:self.sstart())
		self.stop.bind(on_press =lambda a:self.sstop())
		box.add_widget(start)
		box.add_widget(self.stop)
		box.add_widget(Label(text="Target: ",size_hint=(0.1,1)))
		box.add_widget(self.input)
		box2.add_widget(self.gen_label)
		box2.add_widget(self.best_label)
		box2.add_widget(self.score_label)
		main_layout.add_widget(box)
		main_layout.add_widget(self.canvas)
		main_layout.add_widget(box2)
		return main_layout

	def sstop(self):
		Clock.unschedule(self.update)
		if(self.stop.text=="Restart"):
			self.population = []
			self.best = []
			self.aver = []
			self.worst = []
			self.fig.clf()
			self.canvas.draw_idle()
			self.input.disabled=False
		self.stop.text = "Restart"

	def sstart(self):
		self.input.disabled=True
		self.stop.text = "Stop"
		self.target = self.input.text
		if self.population == []:
			self.population = Evolution._firstPopulation(1000,self.target)
			self.population = Evolution._ratePopulation(self.population,self.target)
		Clock.schedule_interval(self.update,.1)

	def update(self,dt):
		self.population = Evolution.evolvePopulation(population = self.population,Target = self.target)
		self.best.append(self.population[0][1])
		self.aver.append(self.population[int(len(self.population)/2)][1])
		self.worst.append(self.population[len(self.population)-1][1])
		self.plotGraph(self.best,self.aver,self.worst,len(self.best))
		#self.label.text = "[color={}]Generation:[/color]{} Best: \"{}\" Score: {}/{}".format(get_hex_from_color((1, 0, 0)),len(self.best),self.population[0][0],self.population[0][1],len(self.target))
		self.gen_label.text = "Generation: {}".format(len(self.best))
		self.best_label.text = "Best individual: \"{}\"".format(self.population[0][0])
		self.score_label.text = "Score: {}/{}".format(self.population[0][1],len(self.target))
		if self.population[0][1] == len(self.target): self.sstop()

	def plotGraph(self,best=[],aver=[],worst=[],generation=0):
		self.fig.clf()
		axes = self.fig.add_axes([0.1,0.1,0.9,0.9])
		axes.set_xlabel("Generation")
		axes.set_ylabel("Points")
		axes.plot(range(generation),best, label = "Best", color = "#4DE289",lw=4)
		axes.plot(range(generation),aver, label = "Average", color = "#E8FF26",lw=4)
		axes.plot(range(generation),worst, label = "Worst", color = "#DF1F1F",lw=4)
		self.canvas.draw_idle()
	def get_color_text(self,text):
		target = self.target
		#for gene in range(len(text)):


if __name__ == '__main__':
	EvolutionSimulator().run()