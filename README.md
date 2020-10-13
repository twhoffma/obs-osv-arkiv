cp -r static/* /srv/www/static/
 sudo certbot certonly --webroot --webroot-path=/srv/www/production/guttormsgaardsarkiv.no/guttormsgaardsarkiv_no -d arkiv.guttormsgaardsarkiv.no
