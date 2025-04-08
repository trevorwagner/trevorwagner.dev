blogpostjson:
	python3 generate_blog_posts_json.py

clean:
	rm -fR ./_dist

dependencies:
	bash ./util/bin/fetch_dependencies.sh

devserver:
	rm -fR _dist/html/.htaccess
	if [[ ! -d '_dist/html/private/config/' ]]; then mkdir -p '_dist/html/private/config/'; fi
	if [[ ! -f '_dist/html/private/config/email_settings.php' ]]; then touch '_dist/html/private/config/email_settings.php'; fi
	bash ./util/bin/start_dev_server.sh

inventory:
	if [ ! -f '_dist/site_inventory.db' ]; then python3 collect_inventory.py; fi

modtimes: 
	bash ./util/bin/fix_modtimes.sh

timestamp:
	TZ=America/Chicago date -Iseconds

pages: inventory
	python3 generate_html.py

rss: inventory
	python3 generate_rss_feed.py
	cp ./_static/assets/feed/index.php ./_dist/html/blog/feed/

sane:
	printf $$'\nRemoving smart characters and unnecessary formatting from markdown files...\n\n';
	find ./_static -name "*.md" -exec bash ./util/bin/sanitize_markdown.sh "{}" \;

site: sane modtimes inventory pages sitemap rss blogpostjson dependencies
	for asset in '.htaccess' 'css' 'js' 'images' 'robots.txt'; do cp -R _static/assets/"${asset}" ./_dist/html/ ; done

sitemap: inventory
	python3 generate_xml_sitemap.py

test: test.py test.sh
	rm -fR ./test

test.py:
	python -m pytest tests/ --verbose

test.sh: 
	./util/test/bats/bin/bats \
		$$(find util/test -type f -name "test*.bats" -not \( -path "util/test/bats/*" -o -path "util/test/test_helper/*" \))