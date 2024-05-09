timestamp:
	TZ=America/Chicago date -Iseconds

modtimes: 
	bash ./fix_modtimes.sh

clean:
	rm -fR ./_dist

inventory:
	if [[ ! -f '_dist/site_inventory.db' ]]; then python3 -m collect_inventory; fi
		
rss: inventory
	python3 -m generate_rss_feed
	cp ./public/feed/index.php ./_dist/html/blog/feed/

sitemap: inventory
	python3 -m generate_xml_sitemap

pages: inventory
	python3 -m generate_html

site: modtimes inventory pages sitemap rss
	cp -R ./public/{.htaccess,css,js,images,robots.txt} ./_dist/html/

test:
	python -m pytest tests/ --verbose

devserver:
	bash ./dev_server.sh


