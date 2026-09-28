# C Shells: common tasks. Needs Hugo (see HUGO_VERSION) and, for header work, Python 3.
HUGO_VERSION := 0.166.0

.PHONY: serve build header tokens favicon check-generated header-check

serve:            ## Preview locally with drafts, at http://localhost:1313
	hugo server --buildDrafts --disableFastRender

build:            ## Production build into ./public, exactly as CI does it
	hugo build --gc --minify

tokens:           ## Regenerate assets/css/tokens.css from the design system tokens
	python3 tools/tokens.py

favicon:          ## Regenerate the favicon set from tools/favicon.py
	python3 tools/favicon.py

header:           ## Regenerate the sea header partial and stylesheet
	mkdir -p build
	python3 tools/sea/gen.py tools/sea/template.html build/header.html
	python3 tools/sea/split.py

check-generated:  ## Fail if generated files are out of date with their sources
	$(MAKE) tokens header
	git diff --exit-code -- assets/css/tokens.css assets/css/sea-header.css layouts/partials/sea-header.html

header-check:     ## Frame captures of the header for review (needs Playwright)
	python3 tools/sea/check.py
