all::
	@true

clean::
	@true

distclean:: clean
	@true

FORCE:

# gh-pages: FORCE
# 	docker run --network none \
# 		-t --rm -u `id -u`:`id -g` \
# 		-w $$PWD \
# 		-v $$PWD:$$PWD:rw \
# 		ghcr.io/ldalek/docker-sphinx-latex \
# 		sphinx-build -M html . .
# 	touch html/.nojekyll

# clean::
# 	[ -d html ] && rm -r html || true
# 	[ -d doctrees ] && rm -r doctrees || true

pdf: index.rst results.rst FORCE
	docker run --network none \
		-t --rm -u `id -u`:`id -g` \
		-w $$PWD \
		-v $$PWD:$$PWD:rw \
		ghcr.io/ldalek/docker-sphinx-latex \
		sphinx-build -M latex . .
	docker run --network none \
		-t --rm -u `id -u`:`id -g` \
		-w $$PWD \
		-v $$PWD:$$PWD:rw \
		ghcr.io/ldalek/docker-sphinx-latex \
		make -C latex all

clean::
	[ -d latex ] && rm -r latex || true
	[ -d doctrees ] && rm -r doctrees || true



simple.map: simple.c
	gcc -O0 -pipe -o /dev/null $< -Wl,-Map=$@

results.rst: simple.map gen.py
	./gen.py --map-file=$< --output=$@

clean::
	rm -f simple.map results.rst
