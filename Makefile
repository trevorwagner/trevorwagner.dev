timestamp:
	TZ=America/Chicago date -Iseconds

modtimes: 
	bash ./_fix_modtimes.sh

clean:
	rm -fR ./_dist

inventory:
	if [[ ! -f '_dist/site_inventory.db' ]]; then python3 -m collect_inventory; fi
		
rss: inventory
	python3 -m generate_rss_feed
	cp ./_static/public/feed/index.php ./_dist/html/blog/feed/

sitemap: inventory
	python3 -m generate_xml_sitemap

pages: inventory
	python3 -m generate_html

site: sane modtimes inventory pages sitemap rss
	cp -R ./_static/public/{.htaccess,css,js,images,robots.txt} ./_dist/html/

test:
	python -m pytest tests/ --verbose

devserver:
	bash ./_start_dev_server.sh

sane:
	bash ./_make_markdown_sane.sh


