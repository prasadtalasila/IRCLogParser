from numpy import genfromtxt
import glob
import plotly.plotly as py
import plotly.graph_objs as go
py.sign_in('RohanGoel', 'kzoibsptzm')

def pyplot_csv_heatmap_generator(csv_dir):
	# csv_dir = "/home/rohan/tmp/csv/"
	file_list = glob.glob(csv_dir+"*.csv")

	for file in file_list:
		csv_data = genfromtxt(file , delimiter=',')

		trace = go.Heatmap(
		        z=csv_data,
		        x=list(range(48)),
		        y=list(range(1,12)),
				colorscale = [
	        [0, 'rgb(255, 255, 204)'],
	        [0.13, 'rgb(255, 237, 160)'],
	        [0.25, 'rgb(254, 217, 118)'],
	        [0.38, 'rgb(254, 178, 76)'],
	        [0.5, 'rgb(253, 141, 60)'],
	        [0.63, 'rgb(252, 78, 42)'],
	        [0.75, 'rgb(227, 26, 28)'],
	        [0.88, 'rgb(189, 0, 38)'],
	        [1.0, 'rgb(128, 0, 38)']
	    ]
		)

		data = [trace]
		layout = go.Layout(title='A Simple Plot', width=800, height=640)
		fig = go.Figure(data=data, layout=layout)

		py.image.save_as(fig, filename=csv_dir+file[file.rfind("/")+1:-4]+'_heatmap.png')
