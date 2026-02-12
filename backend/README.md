# Social Media — Backend

Lightweight FastAPI backend providing media upload and feed endpoints.

- Run: [social-media/backend/main.py](social-media/backend/main.py) (starts [`app`](social-media/backend/src/app.py))
- Endpoints: [`upload_post`](social-media/backend/src/app.py) (POST /upload), [`get_feed`](social-media/backend/src/app.py) (GET /feed), [`delete_post`](social-media/backend/src/app.py) (DELETE /posts/{post_id})
- DB & models: [`Post`](social-media/backend/src/db.py), DB config in [`DATABASE_URL`](social-media/backend/src/db.py) and setup via [`create_db_and_tables`](social-media/backend/src/db.py)
- Schemas: [`PostCreate`](social-media/backend/src/schemas.py), [`PostResponse`](social-media/backend/src/schemas.py)
- Image uploads via [`imagekit`](social-media/backend/src/images.py); credentials in [social-media/backend/.env](social-media/backend/.env)
- Dependencies: [social-media/backend/pyproject.toml](social-media/backend/pyproject.toml)

Quickstart:
1. Ensure .env is populated: [social-media/backend/.env](social-media/backend/.env)  
2. Install deps (PEP 517): pip install .  
3. Run: python [social-media/backend/main.py](social-media/backend/main.py) or uvicorn src.app:app --reload --port 5001