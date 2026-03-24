# AgroClima

> API RESTful completa para monitoramento climático agrícola com dados de clima, notícias, preços de commodities e insights agronômicos

[![Django](https://img.shields.io/badge/Django-5.2.12-green.svg)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.16.1-red.svg)](https://www.django-rest-framework.org/)
[![React](https://img.shields.io/badge/React-19.2.0-61DAFB.svg?logo=react)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.9.3-blue.svg)](https://www.typescriptlang.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791.svg?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED.svg?logo=docker&logoColor=white)](https://www.docker.com/)
[![Licença](https://img.shields.io/badge/licença-MIT-blue.svg)](LICENSE)

[🇺🇸 English Version](README.md)

## Sobre

O AgroClima é uma plataforma moderna de monitoramento climático agrícola, que combina dados de clima em tempo real, notícias agrícolas, preços de commodities e insights agronômicos em uma única solução integrada. Desenvolvido para agricultores, agrônomos e profissionais do agronegócio, o sistema entrega atualizações diárias automatizadas, alertas e visualização de dados intuitiva.

### Diferenciais

- 🌤️ **Dados Climáticos em Tempo Real** via OpenWeather API
- 📰 **Notícias Agrícolas Curadas** com categorias, fontes e destaques
- 💰 **Preços de Commodities** com variação e alertas
- 🌾 **Insights Agronômicos** com recomendações de culturas e detecção de seca
- ⏰ **Agendador Diário Automático** para atualização dos dados
- 🌐 **API REST versionada (v1)** com documentação OpenAPI/Swagger
- ⚛️ **Frontend React Moderno** com TypeScript, Tailwind CSS e gráficos

## Funcionalidades

### Módulo de Clima

- ✅ Condições atuais e previsão de 7 dias por geolocalização
- ✅ Alertas climáticos para eventos extremos
- ✅ Histórico dos últimos N dias
- ✅ Coordenadas de cidade configuráveis via variáveis de ambiente

### Módulo de Notícias

- ✅ Agregação de notícias agrícolas e do agronegócio
- ✅ Categorias, fontes e notícias em destaque
- ✅ Filtros por categoria, fonte e período
- ✅ Parsing de feeds RSS via Feedparser

### Módulo de Preços

- ✅ Catálogo de produtos com categorias e status ativo
- ✅ Cotações diárias com variação
- ✅ Histórico e estatísticas por produto
- ✅ Alertas de preço com verificação automática

### Insights Agrícolas

- ✅ Recomendações de culturas por estação, temperatura e chuva
- ✅ Detecção de seca com base no histórico de precipitação
- ✅ Endpoint consolidado de insights com contexto climático atual

### Agendador Diário

- ⏰ Atualização automática diária em horário configurável (padrão: 06:00)
- 🔄 Atualização em segundo plano para clima, notícias e preços
- 🔒 Mecanismo de lock para evitar execuções duplicadas
- 📊 Rastreamento do estado de atualização via JSON
- ⚙️ Ativação/desativação via `AUTO_DAILY_UPDATE_ENABLED`

### Administração

- 🏥 Endpoint de health check para monitoramento
- 📖 Documentação interativa com Swagger UI
- 🌐 Suporte a CORS para integração com o frontend
- 📈 Throttling e rate limiting de uso da API

## Stack Tecnológica

### Backend

- **Linguagem:** Python 3.11
- **Framework:** Django 5.2.12
- **API:** Django REST Framework 3.16.1
- **Documentação:** drf-spectacular 0.29.0
- **CORS:** django-cors-headers 4.9.0
- **Servidor:** Gunicorn 23.0.0
- **Extensões:** django-extensions 4.1
- **Env:** python-dotenv 1.2.1

### Banco de Dados e APIs Externas

- **Banco de Dados:** PostgreSQL 16
- **Clima:** OpenWeather API
- **Notícias:** News API
- **Parsing de Feeds:** Feedparser 6.0.12
- **Cliente HTTP:** Requests 2.32.5

### Frontend

- **Framework:** React 19.2.0 com TypeScript 5.9.3
- **Build:** Vite 7.3.1
- **Estilização:** Tailwind CSS 4.1.18
- **Gráficos:** Recharts 3.7.0
- **Roteamento:** React Router DOM 7.13.0
- **Cliente HTTP:** Axios 1.13.5

### Infraestrutura

- **Containers:** Docker e Docker Compose
- **Frontend estático:** Nginx (build estático)
- **Node:** Node 20 (imagem de desenvolvimento)

## Documentação da API

### Documentação Interativa

Após iniciar o servidor, acesse:

- **Swagger UI:** http://localhost:8000/docs/
- **Schema OpenAPI:** http://localhost:8000/schema/

### Principais Endpoints (v1)

#### Health Check

```http
GET /api/v1/health/    # Status de saúde do sistema
```

#### Clima

```http
GET /api/v1/weather/current/          # Dados climáticos atuais
GET /api/v1/weather/forecast/         # Previsão de 7 dias
GET /api/v1/weather/alerts/           # Alertas climáticos ativos
GET /api/v1/weather/history/?days=7   # Histórico
```

#### Notícias

```http
GET /api/v1/news/articles/            # Listar notícias
GET /api/v1/news/articles/featured/   # Notícias em destaque
GET /api/v1/news/categories/          # Categorias
GET /api/v1/news/sources/             # Fontes
```

#### Preços

```http
GET /api/v1/prices/products/                  # Catálogo de produtos
GET /api/v1/prices/prices/latest/             # Últimas cotações
GET /api/v1/prices/prices/by_date/?date=YYYY-MM-DD
GET /api/v1/prices/alerts/                    # Alertas de preço
POST /api/v1/prices/alerts/check_alerts/      # Verificar alertas
```

#### Agricultura

```http
GET /api/v1/agriculture/insights/             # Insights (alertas/seca/recomendações)
GET /api/v1/agriculture/recommendations/      # Recomendações de culturas
```

### Exemplos de Uso

#### 1. Obter Clima Atual

```bash
curl -X GET http://localhost:8000/api/v1/weather/current/ \
  -H "Content-Type: application/json"
```

**Resposta:**

```json
{
  "temperature": 24.5,
  "humidity": 68,
  "wind_speed": 12.3,
  "pressure": 1012,
  "rain_1h": 0.0,
  "description": "Parcialmente nublado",
  "updated_at": "2026-02-19T06:00:00-03:00"
}
```

#### 2. Listar Notícias em Destaque

```bash
curl -X GET http://localhost:8000/api/v1/news/articles/featured/ \
  -H "Content-Type: application/json"
```

#### 3. Consultar Últimas Cotações

```bash
curl -X GET http://localhost:8000/api/v1/prices/prices/latest/ \
  -H "Content-Type: application/json"
```

#### 4. Obter Insights Agrícolas

```bash
curl -X GET "http://localhost:8000/api/v1/agriculture/insights/?days=7" \
  -H "Content-Type: application/json"
```

## Licença

Este projeto está licenciado sob a Licença MIT — veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👥 Autores

- **Lucas Blanger** - [![LinkedIn](https://img.shields.io/badge/LinkedIn-Perfil-0077B5?style=flat&logo=linkedin)](https://www.linkedin.com/in/lucas-blanger-4668a2210/)

---

**Feito com ❤️ para o setor da agricultura familiar**
