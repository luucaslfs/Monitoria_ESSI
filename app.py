from flask import Flask
import random
from datetime import datetime
import pytz

app = Flask(__name__)

@app.route('/')
def hello_world():
    # Configurando timezone para São Paulo
    sp_timezone = pytz.timezone('America/Sao_Paulo')
    current_time = datetime.now(sp_timezone).strftime("%H:%M")
    
    numbers = [random.randint(100, 999) for _ in range(4)]
    
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Lumon Industries - MDR Division</title>
        <style>
            body {{
                background-color: #000;
                color: #33ff33;
                font-family: monospace;
                margin: 40px;
                line-height: 1.6;
            }}
            
            .container {{
                max-width: 800px;
                margin: 0 auto;
                border: 1px solid #33ff33;
                padding: 20px;
                box-shadow: 0 0 20px #33ff33;
            }}
            
            .header {{
                text-align: center;
                border-bottom: 1px solid #33ff33;
                padding-bottom: 20px;
                margin-bottom: 20px;
            }}
            
            .numbers {{
                display: flex;
                justify-content: space-around;
                margin: 20px 0;
            }}
            
            .number-box {{
                border: 1px solid #33ff33;
                padding: 10px;
                text-align: center;
                width: 100px;
            }}
            
            .blink {{
                animation: blink 1s infinite;
            }}
            
            @keyframes blink {{
                50% {{
                    opacity: 0;
                }}
            }}
            
            .status {{
                text-align: center;
                margin-top: 20px;
                padding: 10px;
                border-top: 1px solid #33ff33;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>LUMON INDUSTRIES</h1>
                <p>Departamento de Deploy Refinement</p>
                <p class="blink">ACESSO AUTORIZADO</p>
            </div>
            
            <p>Saudações, valoroso(a) aprendiz designado(a) à supervisão do Refinador Sênior Vinicius.</p>
            <p>Você foi selecionado(a) para experimentar a alegria do deploy refinado.</p>
            <p>Por favor, não questione os métodos de lecionamento. Eles são misteriosos e importantes.</p>
            
            <p>Terminal: MDR-Deploy-{random.randint(1000, 9999)}</p>
            
            <div class="numbers">
                <div class="number-box">{numbers[0]}</div>
                <div class="number-box">{numbers[1]}</div>
                <div class="number-box">{numbers[2]}</div>
                <div class="number-box">{numbers[3]}</div>
            </div>
            
            <p>Status do Sistema: OPERACIONAL</p>
            <p>Métricas de Refinamento em Processamento...</p>
            
            <div class="status">
                <p>Hora Atual: {current_time}</p>
                <p>Status da Waffle Party: {'APROVADO' if sum(numbers) > 3000 else 'EM ANÁLISE'}</p>
                <p class="blink">Por favor, mantenha seu cartão de segurança visível durante toda a aula.</p>
            </div>
        </div>
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)