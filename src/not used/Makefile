.DEFAULT_GOAL := all
# all, install, uninstall, clean, dvi, dist, tests. 

setup: clean requirements.txt
    pip install -r requirements.txt

install: setup
    cd .. && mkdir build && cd build && pyinstaller --onefile --windowed ../src/gui.py
    mv gui.app ~/src

uninstall:
	rm -rf ../build
	echo "Uninstall completed!"


all: setup install
    python3 gui.py #добавить запуск самого приложения

tests: clean
    python3 test/all_tests.py

dvi: clean
    cd source && make html
    open build/html/index.html

dist: install
	mkdir -p ../dist
	cp -R ../build/$(TARGET).app ../dist
	cp -R . ../dist/src
	cd ../dist && tar cvzf $(TARGET).tgz *
	cd ../dist && rm -rf $(TARGET).app
	rm -rf ../dist/src
	echo "Archive creation completed successfully!"	


clean: rm -rf __pycache__ tests/.pytest_cache

.PHONY: run