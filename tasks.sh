cd reservation_management
python manage.py migrate
cd frontend
npm install
npm run build
cd ..
python manage.py collectstatic