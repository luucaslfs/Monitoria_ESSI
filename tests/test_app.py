import pytest
import sys
import os

# Adiciona o diretório raiz ao path do Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_page(client):
    """Testa se a página inicial retorna status code 200 e contém elementos esperados"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'LUMON INDUSTRIES' in response.data
    assert b'Departamento de Deploy Refinement' in response.data
    assert b'ACESSO AUTORIZADO' in response.data

def test_numerical_elements(client):
    """Testa se os elementos numéricos estão presentes na resposta"""
    response = client.get('/')
    # Verifica se existem 4 divs com a classe number-box
    assert response.data.count(b'<div class="number-box">') == 4
    # Verifica se tem um Terminal ID
    assert b'Terminal: MDR-Deploy-' in response.data

def test_time_display(client):
    """Testa se o horário está sendo exibido"""
    response = client.get('/')
    assert b'Hora Atual:' in response.data

def test_waffle_party_status(client):
    """Testa se o status da Waffle Party está presente"""
    response = client.get('/')
    # Deve conter ou 'APROVADO' ou 'EM ANÁLISE'
    response_text = response.data.decode('utf-8')
    assert any(status in response_text for status in ['APROVADO', 'EM ANÁLISE'])

def test_supervisor_name(client):
    """Testa se o nome do supervisor (Vinicius) está presente na página"""
    response = client.get('/')
    response_text = response.data.decode('utf-8')
    assert 'Refinador Sênior Vinicius' in response_text