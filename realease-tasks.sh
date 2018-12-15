sudo apt-get install npm
cd reservation_management
python manage.py migrate
cd frontend
npm install
npm run build
