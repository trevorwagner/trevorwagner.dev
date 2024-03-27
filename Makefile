timestamp:
	TZ=America/Chicago date -Iseconds

clean:
	rm -fR ./_dist

data:
	python3 -m load_db

manifest:
	python3 -m generate_site_manifest

rss: manifest
	python3 -m generate_rss_feed
	cp ./public/feed/index.php ./_dist/html/blog/feed/

sitemap: manifest
	python3 -m generate_xml_sitemap

pages: manifest
	python3 -m generate_html

site: manifest pages sitemap rss
	cp -R ./public/{.htaccess,css,js,images,robots.txt} ./_dist/html/

test:
	python -m pytest tests/ --verbose

devserver:
	bash ./dev_server.sh


