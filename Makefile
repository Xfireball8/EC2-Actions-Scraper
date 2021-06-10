SRC_DIR=.

all: clean sloc flakes lint

sloc:
	sloccount --duplicates --wide --details $(SRC_DIR) | fgrep -v .git > sloccount.sc || :

flakes:
	find $(SRC_DIR) -name *.py|egrep -v '^./tests/'|xargs pyflakes  > pyflakes.log || :

lint:
	find $(SRC_DIR) -name *.py|egrep -v '^./tests/' | xargs pylint --output-format=parseable --reports=y > pylint.log || :

clean:
	rm -f pyflakes.log
	rm -f pylint.log
	rm -f sloccount.sc
