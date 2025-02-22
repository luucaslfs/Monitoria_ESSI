# DevOps e CI/CD: Automatizando seu Deploy

## 1. O que é DevOps?

DevOps é uma cultura organizacional que promove a colaboração entre Desenvolvimento (Dev) e Operações (Ops), eliminando silos e otimizando o ciclo de vida do software.

Principais Pilares:
- Colaboração
- Automação
- Integração Contínua
- Entrega Contínua
- Monitoramento
- Feedback Rápido

É como uma linha de montagem moderna onde:
- Cada etapa é automatizada
- Problemas são detectados rapidamente
- Correções são implementadas de forma ágil
- O produto final é entregue com qualidade e consistência

## 2. O que é CI/CD?

**Continuous Integration (CI)**
- Integração frequente de código
- Execução automática de testes
- Detecção precoce de problemas
- Garantia de qualidade constante

**Continuous Delivery/Deployment (CD)**
- Delivery: Automação até o ambiente de staging
- Deployment: Automação até a produção
- Deploy consistente e confiável
- Redução de erros humanos

*"CI/CD é como ter um chef de confiança que não só prepara o prato, mas também prova, ajusta o tempero e serve automaticamente."*

## 3. Por que usar CI/CD no meu Projeto?

Benefícios Tangíveis:
1. Redução de tempo entre desenvolvimento e deploy
2. Menor índice de bugs em produção
3. Deploy mais seguros e previsíveis
4. Feedback mais rápido
5. Time mais produtivo

Impacto no Desenvolvimento:
- Menos tempo gasto com tarefas repetitivas
- Mais foco em desenvolvimento de features
- Maior confiança nas entregas
- Processo de deploy padronizado

## 4. GitHub Actions

O GitHub Actions é como um assistente pessoal que:
- Observa seu repositório
- Executa tarefas automaticamente
- Gerencia todo o processo de CI/CD
- Integra-se naturalmente com seus projetos

Vantagens:
- Já integrado ao GitHub
- Interface amigável
- Marketplace com actions prontas
- Configuração via YAML
- Execução em containers

## 5. Actions

Actions são os blocos de construção dos seus workflows:

Tipos Comuns:
```markdown
📦 Checkout de código
🔧 Setup de ambientes
🧪 Execução de testes
🚀 Deploy
📊 Relatórios
```

Como Escolher Actions:
- Verifique o marketplace
- Observe número de stars
- Cheque a documentação
- Valide a manutenção ativa
- Procure exemplos de uso

## 6. Arquivos YAML

YAML é a linguagem de configuração do GitHub Actions:
```yaml
name: Deploy
on: [push]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
```

Dicas de YAML:
- Indentação é importante
- Usa espaços, não tabs
- Suporta strings, arrays, objetos
- Case sensitive
- Comentários com #

## 7. Workflows

Workflows são as receitas de automação:

Componentes:
- Trigger (quando executar)
- Jobs (o que executar)
- Steps (como executar)
- Environment (onde executar)

Boas Práticas:
- Nomes descritivos
- Comentários claros
- Reutilização de código
- Tratamento de erros
- Logs informativos

## 8. Como desligar tudo pra não gastar

Checklist de Limpeza:
1. Parar serviços ECS
2. Excluir task definitions não usadas
3. Remover imagens não utilizadas do ECR
4. Verificar outros recursos AWS

Comandos Úteis:
```bash
# Parar serviço ECS
aws ecs update-service --cluster seu-cluster --service seu-service --desired-count 0

# Limpar imagens ECR
aws ecr delete-repository --repository-name repo-name --force
```

## 9. Desafio

"Refine seu Deploy!"

Objetivo:
Implementar CI/CD em seu projeto pessoal usando GitHub Actions

Etapas Sugeridas:
1. Fork do repositório exemplo
2. Configurar secrets
3. Adaptar workflows
4. Implementar testes
5. Fazer deploy

Dicas de Sucesso:
- Comece pequeno
- Incremente gradualmente
- Teste em branches
- Monitore os logs
- Peça ajuda quando necessário