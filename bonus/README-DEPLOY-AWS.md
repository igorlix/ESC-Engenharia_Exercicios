# Guia de Deploy na AWS

Este guia detalha como fazer o deploy do portal de exercícios na AWS.

## Arquitetura de Produção

```
Internet → CloudFront → S3 (frontend estático)
                     ↓
                  ALB (Load Balancer)
                     ↓
              EC2 (Docker Containers)
              - APIs (Ex 1,2,4,6)
              - Django (Ex 5)
              - Streamlit (Ex 3)
```

## Opções de Deploy

### Opção 1: Docker + EC2 (Recomendado para começar)

**Componentes:**
- 1x EC2 t3.medium (~$30/mês)
- 1x S3 Bucket + CloudFront (~$5/mês)
- **Total: ~$35/mês**

**Vantagens:**
- Mais simples de configurar
- Controle total
- Pode rodar tudo em uma instância

### Opção 2: Docker + ECS Fargate

**Componentes:**
- ECS Fargate (containers)
- ALB (Load Balancer)
- S3 + CloudFront
- **Total: ~$50-70/mês**

**Vantagens:**
- Sem gerenciamento de EC2
- Auto-scaling automático
- Mais profissional

### Opção 3: Serverless (Lambda)

**Componentes:**
- Lambda Functions (APIs)
- API Gateway
- S3 + CloudFront
- **Total: ~$10-20/mês**

**Vantagens:**
- Mais barato
- Escalável automaticamente
- Pay-per-use

**Desvantagens:**
- Precisa adaptar código para Lambda
- Cold start
- Django e Streamlit não funcionam bem em Lambda

## Passo a Passo: Deploy Docker + EC2

### 1. Preparar Código Localmente

```bash
cd bonus

# Testar Docker Compose localmente
docker-compose -f docker/docker-compose.yml up --build
```

### 2. Criar EC2 Instance

**AWS Console → EC2 → Launch Instance:**

1. **Nome**: `portal-exercicios-esc`
2. **AMI**: Amazon Linux 2023 ou Ubuntu 22.04
3. **Instance Type**: t3.medium (2 vCPU, 4 GB RAM)
4. **Key Pair**: Criar ou usar existente
5. **Security Group**:
   - SSH (22) - Seu IP
   - HTTP (80) - 0.0.0.0/0
   - HTTPS (443) - 0.0.0.0/0
   - Custom TCP (5001-5006, 8000, 8501) - 0.0.0.0/0

### 3. Conectar e Configurar EC2

```bash
# Conectar via SSH
ssh -i sua-chave.pem ec2-user@seu-ip-publico

# Instalar Docker
sudo yum update -y
sudo yum install -y docker
sudo service docker start
sudo usermod -a -G docker ec2-user

# Instalar Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Verificar
docker --version
docker-compose --version
```

### 4. Transferir Código para EC2

**Opção A: Via Git (Recomendado)**
```bash
# No EC2
git clone https://github.com/seu-usuario/ESC-Engenharia_Exercicios.git
cd ESC-Engenharia_Exercicios/bonus
```

**Opção B: Via SCP**
```bash
# No seu computador local
cd bonus
tar -czf bonus.tar.gz .
scp -i sua-chave.pem bonus.tar.gz ec2-user@seu-ip:/home/ec2-user/

# No EC2
tar -xzf bonus.tar.gz
```

### 5. Configurar Variáveis de Ambiente

```bash
# No EC2
cd bonus
cp api/exercicio4/.env.example api/exercicio4/.env

# Editar com suas credenciais AWS
nano api/exercicio4/.env
```

### 6. Iniciar Containers

```bash
cd docker
docker-compose up -d --build

# Verificar status
docker-compose ps

# Ver logs
docker-compose logs -f
```

### 7. Deploy Frontend no S3

#### Criar Bucket S3

```bash
# AWS CLI (no seu computador)
aws s3 mb s3://portal-exercicios-esc --region us-east-1

# Configurar como website
aws s3 website s3://portal-exercicios-esc \
  --index-document index.html \
  --error-document index.html

# Configurar permissões públicas
aws s3api put-bucket-policy --bucket portal-exercicios-esc --policy '{
  "Version": "2012-10-17",
  "Statement": [{
    "Sid": "PublicReadGetObject",
    "Effect": "Allow",
    "Principal": "*",
    "Action": "s3:GetObject",
    "Resource": "arn:aws:s3:::portal-exercicios-esc/*"
  }]
}'
```

#### Atualizar URLs no Frontend

Editar `frontend/js/config.js`:

```javascript
production: {
    ex1: 'http://SEU-IP-EC2:5001/api/ex1',
    ex2: 'http://SEU-IP-EC2:5002/api/ex2',
    ex4: 'http://SEU-IP-EC2:5004/api/ex4',
    ex6: 'http://SEU-IP-EC2:5006/api/ex6',
    ex3: 'http://SEU-IP-EC2:8501',
    ex5: 'http://SEU-IP-EC2:8000'
}
```

#### Upload para S3

```bash
cd frontend
aws s3 sync . s3://portal-exercicios-esc/ --delete

# URL do site
echo "http://portal-exercicios-esc.s3-website-us-east-1.amazonaws.com"
```

### 8. Configurar CloudFront (Opcional mas Recomendado)

**AWS Console → CloudFront → Create Distribution:**

1. **Origin Domain**: portal-exercicios-esc.s3-website-us-east-1.amazonaws.com
2. **Viewer Protocol Policy**: Redirect HTTP to HTTPS
3. **Cache Policy**: CachingOptimized
4. **Create Distribution**

Aguardar deployment (~15 minutos).

URL final: `https://d123456789.cloudfront.net`

### 9. Domínio Personalizado (Opcional)

#### Com Route 53:

1. **Comprar domínio** em Route 53
2. **Criar certificado SSL** no ACM (us-east-1 para CloudFront)
3. **Adicionar CNAME** no CloudFront
4. **Atualizar Route 53** apontando para CloudFront

#### Atualizar config.js:

```javascript
production: {
    ex1: 'https://api.seudominio.com/api/ex1',
    ex2: 'https://api.seudominio.com/api/ex2',
    ...
}
```

## Scripts Automatizados

### Script de Deploy Frontend

`deploy/deploy-s3.sh`:
```bash
#!/bin/bash
BUCKET_NAME="portal-exercicios-esc"

cd ../frontend
aws s3 sync . s3://$BUCKET_NAME/ --delete --exclude ".git/*"

echo "✅ Frontend deployed to S3!"
echo "URL: http://$BUCKET_NAME.s3-website-us-east-1.amazonaws.com"
```

### Script de Deploy Backend

`deploy/deploy-ec2.sh`:
```bash
#!/bin/bash
EC2_IP="SEU-IP-EC2"
KEY_PATH="sua-chave.pem"

# Transferir código
tar -czf ../bonus.tar.gz ../
scp -i $KEY_PATH ../bonus.tar.gz ec2-user@$EC2_IP:~/

# Conectar e executar
ssh -i $KEY_PATH ec2-user@$EC2_IP << 'EOF'
  cd ~
  tar -xzf bonus.tar.gz
  cd bonus/docker
  docker-compose down
  docker-compose up -d --build
  docker-compose ps
EOF

echo "✅ Backend deployed to EC2!"
```

## Configurar CORS para Produção

Editar cada `api/exercicioX/app.py`:

```python
from flask_cors import CORS

# Desenvolvimento
# CORS(app)

# Produção
CORS(app, origins=[
    "https://seudominio.com",
    "https://d123456789.cloudfront.net"
])
```

## Monitoramento

### CloudWatch Logs

```bash
# Instalar CloudWatch Agent no EC2
sudo yum install amazon-cloudwatch-agent

# Configurar logs dos containers
docker-compose logs > /var/log/docker-app.log
```

### Health Checks

Cada API tem endpoint `/health`:

```bash
curl http://seu-ip:5001/health
curl http://seu-ip:5002/health
curl http://seu-ip:5004/health
curl http://seu-ip:5006/health
```

## Backup e Disaster Recovery

### Backup do EC2

1. **AWS Console → EC2 → Snapshots**
2. Criar snapshot do volume EBS
3. Agendar snapshots automáticos (AWS Backup)

### Backup do S3

```bash
# Versioning habilitado
aws s3api put-bucket-versioning \
  --bucket portal-exercicios-esc \
  --versioning-configuration Status=Enabled
```

## Custos Estimados

### Configuração Básica
- EC2 t3.medium: $30/mês
- S3 + transferências: $2-5/mês
- CloudFront: $1-3/mês
- **Total: ~$33-38/mês**

### Configuração com ALB
- EC2 t3.medium: $30/mês
- ALB: $16/mês
- S3 + CloudFront: $5/mês
- **Total: ~$51/mês**

### Configuração Serverless
- Lambda (1M requests): $0.20
- API Gateway: $3.50
- S3 + CloudFront: $5/mês
- **Total: ~$8-10/mês** (baixo tráfego)

## Troubleshooting

### Container não inicia

```bash
# Ver logs
docker-compose logs apis

# Entrar no container
docker-compose exec apis /bin/bash

# Reiniciar
docker-compose restart apis
```

### Erro de CORS

Verificar `origins` nas APIs Flask e URL no `config.js`.

### Site S3 não carrega

Verificar:
1. Bucket policy (público)
2. Static website hosting habilitado
3. index.html existe

### API não responde

Verificar:
1. Security Group do EC2
2. Container rodando: `docker ps`
3. Porta exposta corretamente

## Próximos Passos

1. ✅ Deploy básico funcionando
2. ⬜ Configurar domínio personalizado
3. ⬜ Configurar HTTPS (certificado SSL)
4. ⬜ Implementar CI/CD (GitHub Actions)
5. ⬜ Configurar auto-scaling
6. ⬜ Implementar monitoramento (CloudWatch)
7. ⬜ Configurar backups automáticos

## Suporte

Para dúvidas sobre deploy AWS, consulte:
- [AWS EC2 Documentation](https://docs.aws.amazon.com/ec2/)
- [AWS S3 Static Website](https://docs.aws.amazon.com/AmazonS3/latest/userguide/WebsiteHosting.html)
- [Docker Compose](https://docs.docker.com/compose/)
