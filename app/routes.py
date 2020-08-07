from app import app, db
from app.models import Chart, generate_graph
from datetime import datetime, timedelta
from flask import render_template, request, url_for, redirect, g
import matplotlib.pyplot as plt


@app.route('/')
def index():
    return render_template('index.html')

# @app.route('/price')
@app.route('/price', methods=['GET', 'POST'])
def price():
    if request.method == 'POST':
        now = datetime.utcnow()
        stock = request.form.get('stock')
        date_start = request.form.get('date_start')
        date_end = request.form.get('date_end')

        u = Chart(now=now, date_start=date_start, date_end=date_end, stock=stock)
        g = u
        db.session.add(u)
        db.session.commit()
        generate_graph()
        return redirect('/graph')
    return render_template('price.html')

@app.route('/graph')
def graph():
    print(g)
    return render_template('graph.html')

import io
import random
from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

# @app.route('/plot.png')
# def plot_png():
#     fig = create_figure()
#     output = io.BytesIO()
#     FigureCanvas(fig).print_png(output)
#     return Response(output.getvalue(), mimetype='image/png')

# def create_figure():
#     fig = Figure()
#     axis = fig.add_subplot(1, 1, 1)
#     xs = range(100)
#     ys = [random.randint(1, 50) for x in xs]
#     axis.plot(xs, ys)
#     return fig