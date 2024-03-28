#!/bin/bash 
echo "Creating Migrations..." 
python manage.py makemigrations app
echo ====================================

echo "Collecting Static Files..." 
python manage.py collectstatic --noinput
echo ==================================== 

echo "Starting Migrations..." 
python manage.py migrate 
echo ====================================  

echo "Importing data..."
python manage.py import_locations
echo ====================================  

echo "Creating Vehicles"
python manage.py generate_vehicles 100
echo ====================================  

echo "Starting Server..." 
python manage.py runserver 0.0.0.0:8000