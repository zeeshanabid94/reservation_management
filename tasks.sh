cd reservation_management
python manage.py migrate
python manage.py collectstatic
cd frontend
npm install
npm run build
