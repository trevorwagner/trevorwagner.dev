clean:
	rm -fR ./_dist

devserver:
	bash ./_start_dev_server.sh

inventory:
	if [[ ! -f '_dist/site_inventory.db' ]]; then python3 -m collect_inventory; fi

modtimes: 
	bash ./_fix_modtimes.sh

timestamp:
	TZ=America/Chicago date -Iseconds

pages: inventory
	python3 -m generate_html
		
rss: inventory
	python3 -m generate_rss_feed
	cp ./_static/public/feed/index.php ./_dist/html/blog/feed/

sane:
	bash ./_sanitize_markdown.sh

site: sane modtimes inventory pages sitemap rss
	cp -R ./_static/public/{.htaccess,css,js,images,robots.txt} ./_dist/html/

sitemap: inventory
	python3 -m generate_xml_sitemap

test:
	python -m pytest tests/ --verbose
