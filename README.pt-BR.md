# AgroClima API

> API RESTful completa para monitoramento climático agrícola com dados de clima, notícias e preços de commodities

[![Django](https://img.shields.io/badge/Django-6.0.2-green.svg)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.16.1-red.svg)](https://www.django-rest-framework.org/)
[![React](https://img.shields.io/badge/React-19.2.0-61DAFB.svg?logo=react)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.9.3-blue.svg)](https://www.typescriptlang.org/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0-orange.svg)](https://www.mysql.com/)
[![Licença](https://img.shields.io/badge/licença-MIT-blue.svg)](LICENSE)

[🇺🇸 English Version](README.md)

## Sobre

O AgroClima é uma plataforma moderna de monitoramento climático agrícola, que combina dados de clima em tempo real, notícias agrícolas e rastreamento de preços de commodities em uma única solução integrada. Desenvolvido para agricultores, agrônomos e profissionais do agronegócio, o sistema entrega atualizações diárias automatizadas e visualização de dados intuitiva.

### Diferenciais

- 🌤️ **Dados Climáticos em Tempo Real** via OpenWeather API
- 📰 **Notícias Agrícolas Agregadas** via News API
- 💰 **Rastreamento de Preços de Commodities** com atualizações diárias
- ⏰ **Agendador Diário Automático** para atualização dos dados
- 🌐 **API REST Completa** com documentação OpenAPI/Swagger
- ⚛️ **Frontend React Moderno** com TypeScript e Tailwind CSS

## Funcionalidades

### Módulo de Clima

- ✅ Condições climáticas atuais por geolocalização
- ✅ Dados de temperatura, umidade, velocidade do vento e precipitação
- ✅ Coordenadas de cidade configuráveis via variáveis de ambiente
- ✅ Respostas em cache para otimização de desempenho

### Módulo de Notícias

- ✅ Agregação de notícias agrícolas e do agronegócio
- ✅ Parsing de feeds RSS via Feedparser
- ✅ Filtragem e categorização por tema
- ✅ Atualização automática de conteúdo agendada

### Módulo de Preços

- ✅ Rastreamento de preços de commodities (grãos, pecuária, etc.)
- ✅ Comparação histórica de preços
- ✅ Atualizações automáticas diárias
- ✅ Visualização de dados com gráficos

### Agendador Diário

- ⏰ Atualização automática diária em horário configurável (padrão: 06:00)
- 🔄 Atualização em segundo plano para todos os módulos
- 🔒 Mecanismo de lock para evitar execuções duplicadas
- 📊 Rastreamento do estado de atualização via JSON

### Administração

- 🏥 Endpoint de health check para monitoramento
- 📖 Documentação interativa com Swagger UI
- 🌐 Suporte a CORS para integração com o frontend
- 📈 Throttling e rate limiting de uso da API

## Stack Tecnológica

### Backend

- **Framework:** Django 6.0.2
- **API:** Django REST Framework 3.16.1
- **Documentação:** drf-spectacular 0.29.0
- **Extensões:** django-extensions 4.1

### Banco de Dados e APIs Externas

- **Banco de Dados:** MySQL 8.0
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

## Documentação da API

### Documentação Interativa

Após iniciar o servidor, acesse:

- **Swagger UI:** http://localhost:8000/docs/
- **Schema OpenAPI:** http://localhost:8000/schema/

### Principais Endpoints

#### Health Check

```http
GET /api/health/    # Status de saúde do sistema
```

#### Clima

```http
GET /api/weather/             # Dados climáticos atuais
GET /api/weather/forecast/    # Previsão do tempo
```

#### Notícias

```http
GET /api/news/          # Listar notícias agrícolas
GET /api/news/{id}/     # Detalhes de uma notícia
```

#### Preços

```http
GET /api/prices/                  # Listar preços de commodities
GET /api/prices/{commodity}/      # Preço de commodity específica
GET /api/prices/history/          # Histórico de preços
```

### Exemplos de Uso

#### 1. Obter Clima Atual

```bash
curl -X GET http://localhost:8000/api/weather/ \
  -H "Content-Type: application/json"
```

**Resposta:**

```json
{
  "temperature": 24.5,
  "humidity": 68,
  "wind_speed": 12.3,
  "description": "Parcialmente nublado",
  "city": "Erechim",
  "updated_at": "2026-02-19T06:00:00-03:00"
}
```

#### 2. Listar Notícias Agrícolas

```bash
curl -X GET http://localhost:8000/api/news/ \
  -H "Content-Type: application/json"
```

#### 3. Consultar Preços de Commodities

```bash
curl -X GET http://localhost:8000/api/prices/ \
  -H "Content-Type: application/json"
```

#### 4. Verificar Saúde da API

```bash
curl -X GET http://localhost:8000/api/health/
```

## Licença

Este projeto está licenciado sob a Licença MIT — veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👥 Autores

- **Lucas Blanger** - [![LinkedIn](https://img.shields.io/badge/LinkedIn-Perfil-0077B5?style=flat&logo=linkedin)](https://www.linkedin.com/in/lucas-blanger-4668a2210/)

---

**Feito com ❤️ para o setor da agricultura familiar**
