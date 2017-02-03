FILES :=                              						\
  apiary.apib                      							\
  IDB.log                      								\
  model.html                           						\
  flaskapp/models.py                         				\
  flaskapp/tests.py                          				\
  flaskapp/loader.py 											\
  UML.pdf		  
\

all:

check:
	@for i in $(FILES);                                         		\
    do                                                          		\
        [ -e $$i ] && echo "$$i found" || echo "$$i NOT FOUND"; 		\
    done

ifeq ($(CI), true)
    COVERAGE := coverage
    PYLINT   := pylint
else
    COVERAGE := coverage-3.5
	PYLINT   := pylint3
endif

.pylintrc:
	$(PYLINT) --disable=bad-whitespace,missing-docstring,pointless-string-statement --reports=n --generate-rcfile > $@

pylint: .pylintrc 
	-$(PYLINT) flaskapp/models.py
	-$(PYLINT) flaskapp/tests.py

clean:
	rm -f  .coverage
	rm -f  *.pyc
	rm -f  models.html
	rm -f  IDB1.log
	rm -rf __pycache__

models.html:
	pydoc -w flaskapp/models.py
	
IDB.log:
	git log > IDB2.log

test:
	python flaskapp/tests.py

format:
	autopep8 -i flaskapp/tests.py
	autopep8 -i flaskapp/models.py

server-restart:
	/etc/init.d/postgresql reload
	service apache2 reload

error.log:
	tail /var/log/apache2/error.log


load:
	python flaskapp/loader.py

