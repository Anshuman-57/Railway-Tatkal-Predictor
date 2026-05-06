
# Railway Tatkal Intelligence Platform - Advanced Python Internship Project

An advanced full-stack Python project that predicts railway waitlist confirmation probability and provides route-demand analytics, risk scoring, and decision recommendations.

## Why this is internship-level
This is not a basic todo app. It demonstrates backend engineering, ML pipeline design, API development, feature engineering, database logging, dashboard visualization, Dockerization, and product thinking.

## Core Features
- WL/RAC/Confirmed probability prediction
- PQWL/GNWL/RLWL/TQWL-aware scoring
- Tatkal and Premium Tatkal demand risk
- Route popularity analytics
- Expected waitlist movement forecast
- Explainable prediction output
- Similar history samples
- Recommendation engine
- FastAPI Swagger docs
- React analytics dashboard
- SQLite default, PostgreSQL-ready architecture
- Docker Compose support

## Tech Stack
Backend: Python, FastAPI, SQLAlchemy, scikit-learn, pandas
Frontend: React, Vite, Recharts
Database: SQLite by default, PostgreSQL-ready
Deployment: Docker / Render / Railway / Vercel

## Run Backend
```bash
cd backend
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Backend API docs:
```text
http://localhost:8000/docs
```

## Train ML Model
```bash
cd backend
python -m app.ml.train_model
```

This creates:
```text
backend/app/ml/artifacts/tatkal_model.joblib
```

## Run Frontend
```bash
cd frontend
npm install
npm run dev
```

Frontend:
```text
http://localhost:5173
```

## Run with Docker
```bash
docker compose up --build
```

## Important Disclaimer
This project is for learning and portfolio demonstration. It does not claim official IRCTC accuracy. Real production usage requires legally obtained historical railway data and official API permissions.

## Advanced Improvements
- User login and saved predictions
- PostgreSQL migration with Alembic
- Real historical dataset ingestion
- Background scheduled PNR tracker
- Email/WhatsApp alerts
- SHAP explainability
- Model performance dashboard
- Role-based admin panel
- Cloud deployment with CI/CD

## Resume Points
- Built a full-stack Railway Tatkal Intelligence Platform using FastAPI, React, SQLAlchemy, and scikit-learn.
- Designed an ML-ready feature engineering pipeline for waitlist movement prediction using quota, class, route distance, seasonality, and demand score.
- Implemented explainable prediction APIs with probability breakdown, risk level, expected movement, and recommendation engine.
- Developed a responsive React dashboard with route analytics, train popularity charts, and real-time API integration.
- Dockerized backend and frontend services for reproducible deployment.
