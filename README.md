1. Clone the repository:

git clone <repo_url>
cd techcorp_performance


2. Install dependencies:

pip install -r requirements.txt


3. Setup .env file:

SECRET_KEY=your_django_secret
DEBUG=True


4. Apply migrations:

python manage.py migrate


5. Seed sample data:

python scripts/seed_db.py


6. Run the server:

python manage.py runserver


7. Swagger API docs:

http://localhost:8000/api/login/
