all::
	@true

clean::
	@true

distclean:: clean
	@true

gh-pages:
	docker run --network none \
		-t --rm -u `id -u`:`id -g` \
		-w $$PWD \
		-v $$PWD:$$PWD:rw \
		ghcr.io/ldalek/docker-sphinx-latex \
		sphinx-build -M html . .
	touch html/.nojekyll

clean::
	[ -d html ] && rm -r html || true
	[ -d doctrees ] && rm -r doctrees || true
