# Point-Of-Service (POS) Tracking Dashboard

A **work-in-progress web application** for managing and tracking POS (Point-of-Service) devices. It includes dashboards to monitor device configurations, repairs, and departmental handoffs.

This project is part of my **personal portfolio** and reflects my **ongoing learning journey** in backend and frontend development.

## Tech Stack

- Backend: Python, Flask  
- Database: MySQL, SQLAlchemy  
- Frontend: HTML, Bootstrap, JavaScript, CSS  

## Project Structure

- `app.py` – Main application file  
- `templates/` – HTML templates (dashboards, layouts)  
- `models/`, `crud.py` – Data handling logic  
- Other folders for config, data, and database setup  

## Security

- Database credentials are **secured using environment variables** (e.g., via `.env` file and `python-dotenv`) to prevent sensitive information from being hard-coded or committed to the repository.  
- `.gitignore` excludes configuration files containing sensitive information.  
- Follow best practices to **never commit secrets or passwords** directly into version control.

## Status

Actively under development — updates are being made regularly.

---

Note: This project simulates POS device tracking using publicly available models for demonstration purposes only.
All serial numbers, client names, and configurations used in this project are fictitious and randomly generated.
They are not based on any real-world client data and are intended solely for demonstration and educational purposes.

> *Created by Tumelo Lenity Mabilo as part of a growing portfolio.*

