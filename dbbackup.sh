#!/bin/bash
fmtdate=$(date +%y%m%d)
path_prefix=$(cd "$(dirname "$0")"; pwd)

# export moodle database
dbmoodle="moodledb"$fmtdate
moodleoutpath=$path_prefix/$dbmoodle
/usr/bin/mysqldump -u moodle -p -e -C -Q --create-options --skip-lock-tables moodle > $moodleoutpath.sql

# export student database
dbstudent="studentdb"$fmtdate
studentoutpath=$path_prefix/$student
/usr/bin/mysqldump -u attendance -p -e -C -Q --create-options --skip-lock-tables student > $studentoutpath.sql

# export wiki database
dbwiki="wikidb"$fmtdate
wikioutpath=$path_prefix/$dbwiki
/usr/bin/mysqldump -u wiki -p -e -C -Q --create-options --skip-lock-tables wiki > $wikioutpath.sql

# compress database file into file
/bin/tar czf $path_prefix/dbbackup$fmtdate.tgz -C $path_prefix *$fmtdate.sql

# send database file to my email
/bin/echo "dbbackup:$fmtdate " | /usr/bin/mutt yusuke2000@163.com -a $path_prefix/dbbackup$fmtdate.tgz -s "backup content"

#remove old backup file(30 days)
/usr/bin/find . -name "dbbackup*.tgz" -ctime +30 -exec rm -f {} \;

rm -f $path_prefix/*.sql
