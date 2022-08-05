from flask import Flask, render_template, request, redirect, session, flash, url_for
# from .btk_teste import BTK
from btk_c3d_teste import BTK

app = Flask(__name__)
app.secret_key = 'helloworld'

@app.route('/')
def index():
    return render_template('index.html', titulo='Lab Mov')

@app.route('/executar', methods=['POST', ])
def executar():
    #hiperparametro1 = request.form['hiperparametro1']
    #hiperparametro2 = request.form['hiperparametro2']
    arquivo = request.form['arquivo']

    # TODO: Incluir processamento aqui.
    
    btk = BTK(arquivo)
    lAnalysis = btk.listar_analysis_metadata()
    #btk = BTK("A13F22RJ03.c3d")
    resultado = "FUNCIONOU!"

    # return redirect(url_for('resultadoAi', hiperparametro1=hiperparametro1, hiperparametro2=hiperparametro2))
    # return redirect(url_for('resultado', resultado=resultado))
    return render_template('resultado.html', resultado=resultado, arquivo=arquivo, listaAnalysis=lAnalysis)

@app.route('/resultado')
def resultado():
    # hp1 = request.args.get('hiperparametro1')
    # hp2 = request.args.get('hiperparametro1')
    resultado=request.args.get('resultado');
    return render_template('resultado.html', resultado=resultado)

app.run(debug=True, host="0.0.0.0")
