# AgroClima

> Complete RESTful API for agricultural climate monitoring with weather, news, and commodity price data

[![Django](https://img.shields.io/badge/Django-6.0.2-green.svg)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.16.1-red.svg)](https://www.django-rest-framework.org/)
[![React](https://img.shields.io/badge/React-19.2.0-61DAFB.svg?logo=react)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.9.3-blue.svg)](https://www.typescriptlang.org/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0-orange.svg)](https://www.mysql.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

[🇧🇷 Versão em Português](README.pt-BR.md)

## About

AgroClima is a modern platform for agricultural climate monitoring, combining real-time weather data, agricultural news, and commodity price tracking in a single integrated solution. Designed for farmers, agronomists, and agribusiness professionals, the system delivers automated daily updates and intuitive data visualization.

### Key Differentiators

- 🌤️ **Real-Time Weather Data** via OpenWeather API
- 📰 **Aggregated Agricultural News** via News API
- 💰 **Commodity Price Tracking** with daily updates
- ⏰ **Automated Daily Scheduler** for automatic data refresh
- 🌐 **Complete REST API** with OpenAPI/Swagger documentation
- ⚛️ **Modern React Frontend** with TypeScript and Tailwind CSS

## Features

### Weather Module

- ✅ Current weather conditions by geolocation
- ✅ Temperature, humidity, wind speed, and precipitation data
- ✅ Configurable city coordinates via environment variables
- ✅ Cached responses for performance optimization

### News Module

- ✅ Aggregated agricultural and agribusiness news
- ✅ RSS feed parsing via Feedparser
- ✅ Filtering and categorization by topic
- ✅ Scheduled automatic content refresh

### Prices Module

- ✅ Commodity price tracking (grains, livestock, etc.)
- ✅ Historical price comparison
- ✅ Daily automatic updates
- ✅ Data visualization with charts

### Daily Scheduler

- ⏰ Automatic daily update at configurable time (default: 06:00)
- 🔄 Background data refresh for all modules
- 🔒 Lock mechanism to prevent duplicate executions
- 📊 Update state tracking via JSON

### Administration

- 🏥 Health check endpoint for monitoring
- 📖 Interactive Swagger UI documentation
- 🌐 CORS support for frontend integration
- 📈 API usage throttling and rate limiting

## Tech Stack

### Backend

- **Framework:** Django 6.0.2
- **API:** Django REST Framework 3.16.1
- **Documentation:** drf-spectacular 0.29.0
- **Extensions:** django-extensions 4.1

### Database & External APIs

- **Database:** MySQL 8.0
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

## API Documentation

### Interactive Documentation

After starting the server, access:

- **Swagger UI:** http://localhost:8000/docs/
- **OpenAPI Schema:** http://localhost:8000/schema/

### Main Endpoints

#### Health Check

```http
GET /api/health/    # System health status
```

#### Weather

```http
GET /api/weather/                    # Current weather data
GET /api/weather/forecast/           # Weather forecast
```

#### News

```http
GET /api/news/                       # List agricultural news
GET /api/news/{id}/                  # News article details
```

#### Prices

```http
GET /api/prices/                     # List commodity prices
GET /api/prices/{commodity}/         # Specific commodity price
GET /api/prices/history/             # Price history
```

### Example Usage

#### 1. Get Current Weather

```bash
curl -X GET http://localhost:8000/api/weather/ \
  -H "Content-Type: application/json"
```

**Response:**

```json
{
  "temperature": 24.5,
  "humidity": 68,
  "wind_speed": 12.3,
  "description": "Partly cloudy",
  "city": "Erechim",
  "updated_at": "2026-02-19T06:00:00-03:00"
}
```

#### 2. Get Agricultural News

```bash
curl -X GET http://localhost:8000/api/news/ \
  -H "Content-Type: application/json"
```

#### 3. Get Commodity Prices

```bash
curl -X GET http://localhost:8000/api/prices/ \
  -H "Content-Type: application/json"
```

#### 4. Health Check

```bash
curl -X GET http://localhost:8000/api/health/
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **Lucas Blanger** - [![LinkedIn](https://img.shields.io/badge/LinkedIn-Profile-0077B5?style=flat&logo=linkedin)](https://www.linkedin.com/in/lucas-blanger-4668a2210/)

---

**Made with ❤️ for the agribusiness sector**
