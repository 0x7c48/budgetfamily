INVE=./inve

run: .env
	$(INVE) ./manage.py runserver

shell: .env
	$(INVE) ./manage.py shell

syncdb: .env
	$(INVE) ./manage.py syncdb

create_superuser: .env
	$(INVE) ./manage.py create_superuser

.env: requirements.txt requirements/*.txt
	test -d $@ || virtualenv --system-site-packages $@
	$(INVE) pip install -r requirements.txt
	@touch $@

# Connect to DB
# psql -U budgetfamily_user -h localhost -W budgetfamily_db

# Delete DB
# sudo -u postgres dropdb budgetfamily_db
