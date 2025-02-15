# Tutorial de Deploy - Do Docker Local à AWS

## Teoria

Caso você precise revisar a teoria do que vimos na monitoria, acesse o [/Guia_Docker.md](./Guia_Docker.md)

## 1. Aplicação Flask
Criamos uma aplicação Flask temática baseada na série Severance (Ruptura):

```python
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
            <p>Por favor, não questione os métodos de ensino. Eles são misteriosos e importantes.</p>
            
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
    app.run(host='0.0.0.0', port=8080, debug=True)
```

## 2. Configuração Docker Local

### 2.0 Dockerfile
Arquivo `Dockerfile`:
```Dockerfile
FROM python:3.10.12-slim AS base

WORKDIR /app

COPY . .

RUN python -m pip install -r requirements.txt

EXPOSE 8080

CMD python ./app.py
```

### 2.1 Docker Compose
Arquivo `docker-compose.yml`:
```yaml
services:
  server:
    build:
      context: .
    ports:
      - "8080:8080"
  
  db: 
    image: postgres
    restart: always
    user: postgres
    volumes:
      - db-data:/var/lib/postgresql/data	
    environment:
      POSTGRES_DB: mydb
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: suasenha123
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD", "pg_isready"]
      interval: 10s
      timeout: 5s
      retries: 5
  
volumes:
  db-data:
```

### 2.2 Comandos Docker Básicos
```bash
# Construir e iniciar os containers
docker-compose up --build

# Ver containers rodando
docker ps

# Parar os containers
docker-compose down
```

## 3. Testando o Banco PostgreSQL

### 3.1 Conectando ao Banco
```bash
# Via psql no container
docker exec -it <container_id> psql -U postgres -d mydb

# Via psql local
psql -h localhost -p 5432 -U postgres -d mydb
```

### 3.2 Comandos SQL Básicos
```sql
-- Ver banco e usuário atual
SELECT current_database(), current_user;

-- Listar bancos
\l

-- Listar tabelas
\dt

-- Criar tabela de exemplo
CREATE TABLE alunos (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100),
    data_inscricao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Inserir dados
INSERT INTO alunos (nome) VALUES 
    ('Mark Scout'),
    ('Helly Riggs'),
    ('Irving Bailiff'),
    ('Dylan George');

-- Consultar dados
SELECT * FROM alunos;

-- Ver estrutura da tabela
\d alunos

-- Ver versão do PostgreSQL
SELECT version();
```

## 4. Deploy na AWS

### 4.1 Configuração AWS CLI
```bash
# Instalar AWS CLI
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# Configurar credenciais
aws configure
# Inserir:
# - AWS Access Key ID
# - AWS Secret Access Key
# - Default region (ex: us-east-1)
# - Default output format (json)
```

### 4.2 Push da Imagem para ECR
```bash
# Criar repositório no ECR
aws ecr create-repository --repository-name monitoria-essi

# Obter ID da conta AWS
aws sts get-caller-identity --query Account --output text

# Login no ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin YOUR_AWS_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com

# Tagear imagem
docker tag monitoria-essi-img:latest YOUR_AWS_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/monitoria-essi:latest

# Push para ECR
docker push YOUR_AWS_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/monitoria-essi:latest

# Verificar imagens no repositório
aws ecr describe-images --repository-name monitoria-essi
```

### 4.3 Configuração ECS
1. Criar cluster ECS
2. Criar Task Definition
   - Configurar container com a imagem do ECR
   - Mapear porta 8080
3. Criar serviço no cluster usando a Task Definition

### 4.4 Configuração de Segurança
1. Criar novo Security Group
2. Configurar regras de entrada:
   - Type: Custom TCP
   - Port: 8080
   - Source: 0.0.0.0/0
3. Associar Security Group à tarefa ECS

## 5. Verificações e Troubleshooting

### 5.1 Verificar Status da Tarefa
```bash
# Listar tarefas
aws ecs list-tasks --cluster seu-cluster

# Ver detalhes da tarefa
aws ecs describe-tasks --cluster seu-cluster --tasks sua-task-id
```

### 5.2 Logs e Monitoramento
1. Verificar logs no CloudWatch
2. Monitorar métricas do container
3. Verificar status da tarefa no console ECS

## 6. Próximos Passos Sugeridos
1. Implementar HTTPS com certificado SSL
2. Configurar auto-scaling
3. Implementar monitoramento e alertas
4. Criar pipeline de CI/CD
5. Documentar processo de backup e restore

---
**Nota**: Substitua valores como `YOUR_AWS_ACCOUNT`, `seu-cluster`, `sua-task-id` pelos valores reais do seu ambiente.
