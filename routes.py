import requests
from flask import Flask, render_template, request, redirect
import pandas as pd
import quandl
from bokeh.plotting import figure, show, reset_output
from bokeh.charts import TimeSeries
from bokeh.palettes import Spectral11
from bokeh.embed import components 
from forms import SignupForm



quandl.ApiConfig.api_key = 'xx15tPCkmMzchc5HW3mp'

app = Flask(__name__)

app.secret_key = "development-key"

TOOLS = "pan,wheel_zoom,box_zoom,reset"

numlines = 2
mypalette=Spectral11[0:numlines]

print('inside app')
@app.route("/")
def index():
  print('at /')
  return render_template("index.html")

@app.route("/about")
def about():
  return render_template("about.html")

@app.route("/signup", methods=['GET', 'POST'])
def signup():
	print('in signup')
	form = SignupForm()
	if request.method == 'POST':
		if form.validate() == False:
			return render_template('signup.html', form=form)
		else:
			print('Stock ticker: ', form.stock_name.data)
			nameStock = 'EOD/{}'.format(form.stock_name.data)
			stock_df = quandl.get(nameStock, index_col='Year')
			tsStock = stock_df['Close']
			print('got the data from Quandl')
			print('Stock ticker: ', nameStock)

			numlines = 2
			mypalette=Spectral11[0:numlines]
			moving_avg = tsStock.rolling(center=False,window=102).mean()

			p = figure(tools=TOOLS, title='from Quandle WIKI set',
                        x_axis_label='date', y_axis_label = '{} daily closing value'.format(form.stock_name.data),
                        x_axis_type="datetime")
    
			print('starting script p: ',p)

			p.multi_line(xs=[tsStock.index.values]*numlines,
                ys=[tsStock.values, moving_avg.values],
                line_color=mypalette,
                line_width=2)
        
			script, div = components(p)
			print('will render graph.html')
			return render_template('graph.html', script=script, div=div)

			#return  "Success!"

	elif request.method == "GET":
		return render_template('signup.html', form=form)


if __name__ == "__main__":
 	app.run()
