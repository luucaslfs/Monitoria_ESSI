# Implementando CI/CD com GitHub Actions e AWS
*Um guia prático para refinadores de código*

## Índice
1. [Estrutura do Projeto](#estrutura-do-projeto)
2. [Implementando Testes](#implementando-testes)
3. [Configurando GitHub Actions](#configurando-github-actions)
4. [Deploy Automatizado na AWS](#deploy-automatizado-na-aws)

## Estrutura do Projeto

Para implementar CI/CD em nosso projeto, precisamos de uma estrutura organizada que separe claramente o código, testes e configurações:

```
projeto/
├── app.py                 # Aplicação Flask
├── requirements.txt       # Dependências
├── Dockerfile            # Configuração do container
├── docker-compose.yml    # Configuração multi-container
├── tests/                # Diretório de testes
│   ├── __init__.py
│   └── test_app.py      # Testes da aplicação 
└── .github/workflows/    # Workflows do GitHub Actions
    ├── test.yml         # Pipeline de testes
    └── deploy.yml       # Pipeline de deploy
```

## Implementando Testes

Os testes são fundamentais no CI/CD pois garantem que novas mudanças não quebrem funcionalidades existentes.

### 1. Configuração do Ambiente de Testes
```bash
# Criar diretório de testes
mkdir tests
touch tests/__init__.py

# Instalar dependências
pip install pytest
```

### 2. Criando Testes (`tests/test_app.py`)
```python
import pytest
from app import app

@pytest.fixture
def client():
    """
    Fixture que configura um cliente de teste.
    Isso permite testar nossa aplicação sem iniciar um servidor real.
    """
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_page(client):
    """Testa se a página inicial retorna status code 200"""
    response = client.get('/')
    assert response.status_code == 200

def test_content(client):
    """
    Testa se o conteúdo esperado está presente.
    Importante: Usamos decode('utf-8') para lidar com caracteres especiais.
    """
    response = client.get('/')
    response_text = response.data.decode('utf-8')
    assert 'LUMON INDUSTRIES' in response_text
```

### 3. Executando Testes Localmente
```bash
# Da raiz do projeto
pytest -v  # -v para output mais detalhado
```

## Configurando GitHub Actions

GitHub Actions nos permite automatizar nossos processos de teste e deploy. Cada workflow é um arquivo YAML que define quando e como esses processos devem acontecer.

### 1. Workflow de Testes (`test.yml`)
```yaml
name: Run Tests

on:  # Define quando o workflow será executado
  push:
    branches: [ main ]  # Em pushes para main
  pull_request:
    branches: [ main ]  # Em PRs para main

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3  # Faz checkout do código
    
    - name: Set up Python  # Configura o ambiente Python
      uses: actions/setup-python@v3
      with:
        python-version: '3.10'
    
    - name: Install dependencies  # Instala dependências
      run: |
        python -m pip install --upgrade pip
        pip install pytest
        pip install -r requirements.txt
    
    - name: Run tests  # Executa os testes
      run: |
        pytest -v
```

### 2. Workflow de Deploy (`deploy.yml`)
```yaml
name: Deploy to Amazon ECS

on:
  push:
    branches:
      - main

# Estas variáveis serão usadas em todo o workflow
env:
  AWS_REGION: us-west-2          # Região onde seus serviços AWS estão
  ECR_REPOSITORY: monitoria-essi # Nome do seu repositório no ECR
  ECS_SERVICE: meu-deploy       # Nome do seu serviço ECS
  ECS_CLUSTER: cluster          # Nome do seu cluster ECS
  ECS_TASK_DEFINITION: monitoria-essi # Nome da sua task definition
  CONTAINER_NAME: monitoria-essi      # Nome do container

jobs:
  deploy:
    name: Deploy
    runs-on: ubuntu-latest
    environment: production

    steps:
    - name: Checkout
      uses: actions/checkout@v3

    - name: Configure AWS credentials
      uses: aws-actions/configure-aws-credentials@v1
      with:
        aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
        aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        aws-region: ${{ env.AWS_REGION }}

    # ... (outros steps do deploy)
```

## Deploy Automatizado na AWS

### 1. Configurando Secrets no GitHub
As secrets são credenciais sensíveis que não devem ser expostas no código.

1. Acesse: Settings > Secrets and variables > Actions
2. Adicione:
   - `AWS_ACCESS_KEY_ID`: Sua Access Key da AWS
   - `AWS_SECRET_ACCESS_KEY`: Sua Secret Key da AWS

### 2. Obtendo Valores AWS
Precisamos obter os valores corretos da nossa infraestrutura AWS para configurar o workflow de deploy. Estes comandos nos ajudam a encontrar esses valores:

```bash
# Listar clusters - precisamos do nome do cluster onde a aplicação rodará
aws ecs list-clusters
# Exemplo de retorno: arn:aws:ecs:us-west-2:123456789:cluster/meu-cluster

# Listar serviços - precisamos do nome do serviço ECS que gerencia nossos containers
aws ecs list-services --cluster seu-cluster
# Exemplo de retorno: arn:aws:ecs:us-west-2:123456789:service/cluster/meu-deploy

# Listar task definitions - precisamos do nome da task definition que define nosso container
aws ecs list-task-definitions
# Exemplo de retorno: arn:aws:ecs:us-west-2:123456789:task-definition/monitoria-essi:1
```

Estes valores são necessários porque:
- O workflow precisa saber exatamente onde fazer o deploy
- Cada valor identifica um componente específico na sua infraestrutura AWS
- Erros nesses valores impedirão o deploy de funcionar

### 3. Fluxo de Trabalho
O processo completo funciona assim:
1. Push na branch main
2. Workflow de testes é executado
3. Se os testes passam:
   - Imagem Docker é construída
   - Push para ECR (registro de containers da AWS)
   - Deploy no ECS (serviço que executa os containers)

## Boas Práticas

1. **Desenvolvimento**
   - Desenvolva em branches para isolar mudanças
   - Faça PRs para a main para revisão de código
   - Mantenha os testes atualizados para cada nova feature

2. **Testes**
   - Execute testes localmente antes de commit para economia de tempo
   - Mantenha cobertura de testes adequada para prevenir regressões
   - Use fixtures para evitar duplicação de código de teste

3. **Secrets e Variáveis**
   - Nunca comite secrets - use as configurações do GitHub
   - Use environment secrets para diferentes ambientes (dev/staging/prod)
   - Mantenha variáveis de ambiente no workflow para facilitar manutenção

4. **Workflows**
   - Mantenha workflows separados por responsabilidade (princípio SOLID)
   - Use comentários para documentar steps complexos
   - Configure timeouts adequados para evitar jobs presos

## Troubleshooting

### Testes Não Encontrados
Se seus testes não estão sendo encontrados:
```bash
# Verificar estrutura dos arquivos
ls -la tests/

# Verificar se pytest está instalado
pip list | grep pytest

# Rodar com verbose para mais detalhes
pytest -v
```

### Falhas no Deploy
Se seu deploy falhar, verifique nesta ordem:
1. Verifique as credenciais AWS no GitHub Secrets
2. Confirme os valores das variáveis de ambiente no workflow
3. Verifique logs no GitHub Actions
4. Verifique logs no ECS Console da AWS

## Referências
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [AWS ECS Documentation](https://docs.aws.amazon.com/ecs/)
- [Pytest Documentation](https://docs.pytest.org/)