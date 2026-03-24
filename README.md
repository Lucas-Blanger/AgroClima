# AgroClima

> Complete RESTful API for agricultural climate monitoring with weather, news, commodity prices, and agronomic insights

[![Django](https://img.shields.io/badge/Django-5.2.12-green.svg)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.16.1-red.svg)](https://www.django-rest-framework.org/)
[![React](https://img.shields.io/badge/React-19.2.0-61DAFB.svg?logo=react)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.9.3-blue.svg)](https://www.typescriptlang.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791.svg?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED.svg?logo=docker&logoColor=white)](https://www.docker.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

[🇧🇷 Versão em Português](README.pt-BR.md)

## About

AgroClima is a modern platform for agricultural climate monitoring, combining real-time weather data, agricultural news, commodity prices, and agronomic insights in a single integrated solution. Designed for farmers, agronomists, and agribusiness professionals, the system delivers automated daily updates, alerts, and intuitive data visualization.

### Key Differentiators

- 🌤️ **Real-Time Weather Data** via OpenWeather API
- 📰 **Curated Agricultural News** with categories, sources, and featured headlines
- 💰 **Commodity Prices** with variation tracking and alerts
- 🌾 **Agronomic Insights** with crop recommendations and drought risk detection
- ⏰ **Automated Daily Scheduler** for data refresh
- 🌐 **Versioned REST API (v1)** with OpenAPI/Swagger documentation
- ⚛️ **Modern React Frontend** with TypeScript, Tailwind CSS, and charts

## Features

### Weather Module

- ✅ Current conditions and 7-day forecast by geolocation
- ✅ Weather alerts for extreme events
- ✅ Historical data for the last N days
- ✅ Configurable city coordinates via environment variables

### News Module

- ✅ Aggregated agricultural and agribusiness news
- ✅ Categories, sources, and featured articles
- ✅ Filters by category, source, and time range
- ✅ RSS feed parsing via Feedparser

### Prices Module

- ✅ Product catalog with categories and active status
- ✅ Daily quotes with variation tracking
- ✅ Historical series and statistics by product
- ✅ Price alerts with threshold checks

### Agriculture Insights

- ✅ Crop recommendations based on season, temperature, and rain
- ✅ Drought detection from recent precipitation history
- ✅ Consolidated insights endpoint with current weather context

### Daily Scheduler

- ⏰ Automatic daily update at configurable time (default: 06:00)
- 🔄 Background data refresh for weather, news, and prices
- 🔒 Lock mechanism to prevent duplicate executions
- 📊 Update state tracking via JSON
- ⚙️ Enable/disable via `AUTO_DAILY_UPDATE_ENABLED`

### Administration

- 🏥 Health check endpoint for monitoring
- 📖 Interactive Swagger UI documentation
- 🌐 CORS support for frontend integration
- 📈 API usage throttling and rate limiting

## Tech Stack

### Backend

- **Language:** Python 3.11
- **Framework:** Django 5.2.12
- **API:** Django REST Framework 3.16.1
- **Documentation:** drf-spectacular 0.29.0
- **CORS:** django-cors-headers 4.9.0
- **Server:** Gunicorn 23.0.0
- **Extensions:** django-extensions 4.1
- **Env:** python-dotenv 1.2.1

### Database & External APIs

- **Database:** PostgreSQL 16
- **Weather:** OpenWeather API
- **News:** News API
- **Feed Parsing:** Feedparser 6.0.12
- **HTTP Client:** Requests 2.32.5

### Frontend

- **Framework:** React 19.2.0 with TypeScript 5.9.3
- **Build Tool:** Vite 7.3.1
- **Styling:** Tailwind CSS 4.1.18
- **Charts:** Recharts 3.7.0
- **Routing:** React Router DOM 7.13.0
- **HTTP Client:** Axios 1.13.5

### Infrastructure

- **Containers:** Docker and Docker Compose
- **Frontend Hosting:** Nginx (static build)
- **Node:** Node 20 (dev image)

## API Documentation

### Interactive Documentation

After starting the server, access:

- **Swagger UI:** http://localhost:8000/docs/
- **OpenAPI Schema:** http://localhost:8000/schema/

### Main Endpoints (v1)

#### Health Check

```http
GET /api/v1/health/    # System health status
```

#### Weather

```http
GET /api/v1/weather/current/          # Current weather data
GET /api/v1/weather/forecast/         # 7-day forecast
GET /api/v1/weather/alerts/           # Active weather alerts
GET /api/v1/weather/history/?days=7   # Historical data
```

#### News

```http
GET /api/v1/news/articles/            # List news articles
GET /api/v1/news/articles/featured/   # Featured news
GET /api/v1/news/categories/          # Categories
GET /api/v1/news/sources/             # Sources
```

#### Prices

```http
GET /api/v1/prices/products/                  # Product catalog
GET /api/v1/prices/prices/latest/             # Latest quotes
GET /api/v1/prices/prices/by_date/?date=YYYY-MM-DD
GET /api/v1/prices/alerts/                    # Price alerts
POST /api/v1/prices/alerts/check_alerts/      # Check alerts
```

#### Agriculture

```http
GET /api/v1/agriculture/insights/             # Insights (alerts/drought/recommendations)
GET /api/v1/agriculture/recommendations/      # Crop recommendations
```

### Example Usage

#### 1. Get Current Weather

```bash
curl -X GET http://localhost:8000/api/v1/weather/current/ \
  -H "Content-Type: application/json"
```

**Response:**

```json
{
  "temperature": 24.5,
  "humidity": 68,
  "wind_speed": 12.3,
  "pressure": 1012,
  "rain_1h": 0.0,
  "description": "Partly cloudy",
  "updated_at": "2026-02-19T06:00:00-03:00"
}
```

#### 2. Get Featured News

```bash
curl -X GET http://localhost:8000/api/v1/news/articles/featured/ \
  -H "Content-Type: application/json"
```

#### 3. Get Latest Prices

```bash
curl -X GET http://localhost:8000/api/v1/prices/prices/latest/ \
  -H "Content-Type: application/json"
```

#### 4. Get Agriculture Insights

```bash
curl -X GET "http://localhost:8000/api/v1/agriculture/insights/?days=7" \
  -H "Content-Type: application/json"
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **Lucas Blanger** - [![LinkedIn](https://img.shields.io/badge/LinkedIn-Profile-0077B5?style=flat&logo=linkedin)](https://www.linkedin.com/in/lucas-blanger-4668a2210/)

---

**Made with ❤️ for the agribusiness sector**
