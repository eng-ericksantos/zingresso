# 🚀 Plataforma de Gestão de Eventos - Zingresso

Este repositório contém o código-fonte do TCC para a Pós-Graduação em Engenharia de Software USP/Esalq. O projeto consiste em uma plataforma completa para venda de ingressos e gestão de eventos, construída utilizando uma arquitetura moderna baseada em Micro Front-ends e Microsserviços Poliglotas.

![Logo Zingresso](./img/logo.png)

## ✨ Arquitetura Central

A aplicação é dividida em dois domínios principais:

1.  **Micro Front-ends (MFE):** Duas aplicações Angular independentes que são carregadas em um "casco" (App Shell). A comunicação entre elas é feita via **Module Federation** (Webpack 5).
    * **Portal do Participante:** Permite ao usuário buscar eventos, ver detalhes e comprar ingressos.
    * **Painel do Organizador:** Permite ao criador do evento gerenciar seus eventos, criar novos e ver dashboards de vendas.

2.  **Microsserviços (Polyglot):** Três serviços de back-end independentes, cada um com seu próprio banco de dados e lógica de negócio, utilizando as linguagens e frameworks mais adequados para cada tarefa.
    * **Serviço de Usuários (NestJS):** Gerencia autenticação, perfis e autorização.
    * **Serviço de Eventos (FastAPI):** Um catálogo de alta performance para CRUD de eventos.
    * **Serviço de Pedidos (NestJS):** Lida com a lógica transacional de compra de ingressos e comunicação assíncrona.

## 🛠️ Stack de Tecnologias

| Categoria | Tecnologia | Propósito |
| :--- | :--- | :--- |
| **Micro Front-ends** | **Angular (v20)** | Framework para construção dos dois portais. |
| | **Module Federation** | Arquitetura para carregar os MFEs dinamicamente. |
| **Microsserviço 1** | **NestJS (TypeScript)** | `svc-usuarios`: Autenticação (JWT) e perfis. |
| **Microsserviço 2** | **FastAPI (Python)** | `svc-eventos`: CRUD de alta performance para eventos. |
| **Microsserviço 3** | **NestJS (TypeScript)** | `svc-pedidos`: Lógica transacional de pedidos e ingressos. |
| **Bancos de Dados** | **PostgreSQL** | Dados relacionais (Usuários, Pedidos, Ingressos). |
| | **MongoDB** | Dados NoSQL flexíveis (Detalhes dos Eventos). |
| **Mensageria** | **RabbitMQ** | Comunicação assíncrona entre serviços (ex: Pedido Pago). |
| **Infra/DevOps** | **Docker** | Containerização dos serviços e bancos de dados. |
| | **Minikube** | Simulação local de um cluster Kubernetes para documentação. |
| **Deployment** | **Vercel / Netlify** | Deploy (gratuito) dos Micro Front-ends. |
| | **Render / MongoDB Atlas**| Deploy (gratuito) dos Microsserviços e Bancos. |

## 🚀 Como Rodar o Ambiente (Desenvolvimento Híbrido)

O ambiente de desenvolvimento foi otimizado para **produtividade** e **hot-reload** instantâneo.

1.  **Rodamos a Infraestrutura (Bancos) no Docker.**
2.  **Rodamos as 5 Aplicações (Código) localmente na máquina.**

Siga os passos abaixo:

### Passo 1: Subir a Infraestrutura (Bancos e Mensageria)

Abra um terminal na raiz do projeto e suba os contêineres do Docker:

```bash
docker-compose up -d
```
💬 Isso irá iniciar o PostgreSQL, MongoDB e o RabbitMQ em background. Você só precisa fazer isso uma vez.

### Passo 2: Instalar o 'Concurrently' (Apenas uma vez)

Para rodar todas as aplicações de uma só vez, usamos o concurrently. Crie um package.json na raiz do projeto (use npm init -y) e instale-o:

```bash
pnpm install concurrently --save-dev
```

### Passo 3: Configurar o package.json Raiz

Adicione os seguintes scripts ao seu package.json raiz. Eles são os "atalhos" para iniciar cada serviço:

```json
"scripts": {
  "start:dev": "concurrently \"npm run dev:mfe1\" \"npm run dev:mfe2\" \"npm run dev:svc1\" \"npm run dev:svc2\" \"npm run dev:svc3\"",
  "dev:mfe1": "cd mfe-portal-participante && ng serve --port 4200",
  "dev:mfe2": "cd mfe-painel-organizador && ng serve --port 4201",
  "dev:svc1": "cd svc-usuarios && npm run start:dev",
  "dev:svc2": "cd svc-eventos && uvicorn app.main:app --reload --port 8000",
  "dev:svc3": "cd svc-pedidos && npm run start:dev"
}
```

> Nota: Os serviços NestJS (`svc-usuarios` e `svc-pedidos`) devem ser configurados em seus respectivos main.ts para rodar em portas diferentes, ex: 3000 e 3001.

### Passo 4: Subir TODAS as Aplicações

Com tudo configurado, abra um único terminal na raiz do projeto e execute:

```bash
pnpm run start:dev
```

O concurrently irá iniciar os 2 front-ends e os 3 back-ends em paralelo. Qualquer arquivo que você salvar em qualquer um dos 5 projetos terá hot-reload instantâneo.

---

## 📦 Simulação de Produção (Minikube)

Para validar a arquitetura Cloud Native e documentar para o TCC, o projeto também pode ser executado inteiramente dentro de um cluster Kubernetes local via Minikube.

> Esta etapa é para documentação e não para o desenvolvimento do dia-a-dia.

### Iniciar o Minikube:

```bash
minikube start
```

### Construir as Imagens Docker:

(Serão criados 5 Dockerfiles, um para cada serviço)

```bash
docker build -t svc-usuarios ./svc-usuarios
docker build -t svc-eventos ./svc-eventos
# ... etc
```

### Aplicar os Manifestos Kubernetes:

(Serão criados arquivos `.yml` de Deployment e Service para cada serviço)

```bash
kubectl apply -f ./kubernetes
```

---

## 🐳 Arquivo `docker-compose.yml`

O último passo é o `docker-compose.yml`. Este arquivo irá definir e configurar os três serviços de infraestrutura que usamos no **Ambiente Híbrido**.

💡 **Pontos Importantes sobre este arquivo:**

- **Senhas:** Todas as senhas estão como `admin`. Isso é ótimo para desenvolvimento, mas lembre-se de trocá-las (ou usar secrets) em produção.
- **RabbitMQ UI:** A imagem `management` do RabbitMQ permite acessar [http://localhost:15672](http://localhost:15672) (login: admin/admin) para ver as filas e mensagens, o que é extremamente útil para debugar.
- **Volumes:** As linhas `volumes:` garantem que seus dados sejam persistidos mesmo após `docker-compose down`.
- **Rede (Network):** A rede `tcc-network` permite que os contêineres se "enxerguem" pelos nomes de serviço (ex: `postgres-db` em vez de `localhost`).
