
# Architecture

Frontend React dashboard calls FastAPI endpoints. FastAPI validates input, builds features, runs ML model or heuristic fallback, logs results to SQL database, and returns probability explanation.

## Modules
- API Layer: request validation and routing
- Service Layer: business workflow
- ML Layer: feature engineering, model training, inference
- DB Layer: prediction logs and alert rules
- Analytics Layer: route demand and train popularity

## Production Upgrade
Use PostgreSQL, Redis queue, scheduled scraper workers, authentication, monitoring, and cloud deployment.
