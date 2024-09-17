blogpostjson:
	python3 generate_blog_posts_json.py

clean:
	rm -fR ./_dist

dependencies:
	bash ./_fetch_dependencies.sh

devserver:
	rm -fR _dist/html/.htaccess
	if [[ ! -d '_dist/html/private/config/' ]]; then mkdir -p '_dist/html/private/config/'; fi
	if [[ ! -f '_dist/html/private/config/email_settings.php' ]]; then touch '_dist/html/private/config/email_settings.php'; fi
	bash ./_start_dev_server.sh

inventory:
	if [[ ! -f '_dist/site_inventory.db' ]]; then python3 collect_inventory.py; fi

modtimes: 
	bash ./_fix_modtimes.sh

timestamp:
	TZ=America/Chicago date -Iseconds

pages: inventory
	python3 generate_html.py
		
rss: inventory
	python3 generate_rss_feed.py
	cp ./_static/assets/feed/index.php ./_dist/html/blog/feed/

sane:
	bash ./_sanitize_markdown.sh

site: sane modtimes inventory pages sitemap rss blogpostjson dependencies
	cp -R ./_static/assets/{.htaccess,css,js,images,robots.txt} ./_dist/html/

sitemap: inventory
	python3 generate_xml_sitemap.py

test:
	python -m pytest tests/ --verbose
