#!/bin/bash -e
#
# Backup MySQL tables

db="guttormsgaardsarkiv_no"
keep="7"
basename="mysql_${db}"
dest="/var/backups/${basename}_`date +%Y%m%d-%H%M%S`.sql.xz"
media="/srv/www/media/guttormsgaardsarkiv.no/media"

touch $dest
chmod 600 $dest
chown root.root $dest

mysqldump --add-drop-table --extended-insert --quote-names $db | xz > $dest
find /var/backups -type f -name "${basename}*" -mtime +$keep -delete

s3cmd --no-progress put "$dest" s3://hoffy-obsobsarkiv 

s3cmd --no-progress --recursive sync "$media" s3://hoffy-obsobsarkiv
