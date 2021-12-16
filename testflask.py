import pandas as pd
import numpy as np
import json
import plotly
import plotly.express as px
import monochromator

from flask import Flask,render_template,request,Response
app = Flask(__name__)

#create variables
grating=0
wlfilter=0
entr_slit=2.0
exit_slit=2.0
wavelength=1300.0
wlmin=600.0
wlmax=1600.0
wlstp=20.0
stage_x=0.0
stage_y=0.0
stage_z=0.0

mono=monochromator.Monochromator()

@app.route('/',methods=['GET','POST'])
def index():
    global grating
    global wlfilter
    global entr_slit
    global exit_slit
    global wlmin,wlmax,wlstp
    global stage_x,stage_y,stage_z
    #mock random plot
    N = 40
    x = np.linspace(0, 1, N)
    y = np.random.randn(N)
    df=pd.DataFrame({'x': x, 'y': y})
    fig=px.line(df,x='x',y='y')
    graphJSON=json.dumps(fig,cls=plotly.utils.PlotlyJSONEncoder)
    #deal with html buttons/fields
    if request.method == 'POST':
        if request.form.get('action1') == 'VALUE1':
            print('a')
        elif  request.form.get('action2') == 'VALUE2':
            print('b')
        elif request.form.get('grating_submit')=='Submit':
            mono.set_grating(int(request.form['grating']))
        elif request.form.get('filter_submit')=='Submit':
            mono.set_filter(int(request.form['filter']))
        elif request.form.get('entr_slit_submit')=='Submit':
            try:
                mono.set_entr_slit(float(request.form['entr_slit']))
            except ValueError:
                print("not a float")
        elif request.form.get('exit_slit_submit')=='Submit':
            try:
                mono.set_exit_slit(float(request.form['exit_slit']))
            except ValueError:
                print("not a float")
        elif request.form.get('wavelength_submit')=='Submit':
            try:
                mono.set_wavelength(float(request.form['wavelength']))
            except ValueError:
                print("not a float")
            print(mono.get_wavelength())
        elif request.form.get('wlsweep')=='Spectrum':
            try:
                wlmin=float(request.form['wlmin'])
            except ValueError:
                print("not a float")
            try:
                wlmax=float(request.form['wlmax'])
            except ValueError:
                print("not a float")
            try:
                wlstp=float(request.form['wlstp'])
            except ValueError:
                print("not a float")
            print(wlmin)
            print(wlstp)
            print(wlmax)
        elif request.form.get('savecsv')=='Save CSV':
            print(request.form['filename'])
        elif request.form.get('stage_x_submit')=='Submit':
            try:
                stage_x=float(request.form['stage_x'])
            except ValueError:
                print("not a float")
            print(stage_x)
        elif request.form.get('stage_y_submit')=='Submit':
            try:
                stage_y=float(request.form['stage_y'])
            except ValueError:
                print("not a float")
            print(stage_y)
        elif request.form.get('stage_z_submit')=='Submit':
            try:
                stage_z=float(request.form['stage_z'])
            except ValueError:
                print("not a float")
            print(stage_z)
        elif request.form.get('autoset')=='Autoset':
            print("autoset")
            stage_x=1
            stage_y=2.0
            stage_z=3
    filename="blarg"
    #fill html template
    return render_template('index.html',
                           graphJSON=graphJSON,
                           grating_preselect=mono.get_grating(),
                           filter_preselect=mono.get_filter(),
                           wlmin_preselect=str(wlmin),
                           wlstp_preselect=str(wlstp),
                           wlmax_preselect=str(wlmax),
                           stage_x_preselect=str(stage_x),
                           stage_y_preselect=str(stage_y),
                           stage_z_preselect=str(stage_z),
                           entr_slit_preselect=str(mono.get_entr_slit()),
                           exit_slit_preselect=str(mono.get_exit_slit()),
                           wavelength_preselect=str(mono.get_wavelength()),
                           filename_preselect=filename)

#make plotly available
@app.route('/plotly.js')
def plotlyjs():
    return Response(open('templates/plotly-latest.min.js').read(),mimetype="text/html")

#run app
if __name__ == '__main__':
    app.debug = True
    app.run()

