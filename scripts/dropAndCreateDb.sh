sudo -u postgres dropdb geodjango
sudo -u postgres createdb -T template_postgis geodjango
python manage.py syncdb --migrate
python manage.py check_permissions
