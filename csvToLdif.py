#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

# init 
import sys
import codecs
from os.path import basename
reload(sys)
sys.setdefaultencoding('utf8')

# check argument
if len(sys.argv) != 2:
    print u'请输入正确的参数：{0} [csv文件名]\n'.format(sys.argv[0])
    exit()
pyfilename = basename(sys.argv[0])
print basename(sys.argv[1])
csv_filename = basename(sys.argv[1]).split('.')[0]

if len(csv_filename) != 3 or not csv_filename.isdigit():
    print u'csv文件名不符合规范，请修改为学号的前三位以标识系别与年级\n'



ldif_tmpl = '\
dn: cn={3},ou={2},ou={1},cn={0},ou=People,dc=neuq,dc=edu.cn\n\
objectClass: inetOrgPerson\n\
objectClass: top\n\
cn: {4}\n\
sn: {5}\n\
givenName: {6}\n\
displayName: {7}\n\
departmentNumber: {8}\n\
userPassword: {9}\n\
roomNumber: {10}\n\n'

create_grade_tree = '\
dn: ou={2},ou={1},cn={0},ou=People,dc=neuq,dc=edu.cn\n\
objectClass: organizationalUnit\n\
objectClass: top\n\
ou: {3}\n\n'

department = {'1' : '经济系',
              '2' : '管理系',
              '3' : '商贸系',
              '4' : '电子信息系', 
              '5' : '自动化系',
              '6' : '外语系',
              '7' : '信息与计算科学系',
              '8' : '材料系', 
              '9' : '环境系'}

csv_file = codecs.open(sys.argv[1], 'r', "utf-8")
ldif_file = codecs.open('./{0}.ldif'.format(csv_filename), 'w', "utf-8");
try:
    dept = department[csv_filename[0]]
    grade = ''.join(["20", csv_filename[1:3]])
    ldif_file.writelines(create_grade_tree.format('学生', dept, grade, grade))
    for line in csv_file:
        idnumber, fullname = line.rstrip().split(',')
        if len(fullname) <= 3:
            lastname = fullname[:1]
            firstname = fullname[1:]
        else:
            print 'alert: {0}\n'.format(idnumber)
            lastname = fullname[:2]
            firstname = fullname[2:]
        classnum = idnumber[:5]
        ldif_item = ldif_tmpl.format('学生', dept, grade, idnumber, idnumber, lastname, firstname, fullname, dept, "{MD5}ISGMyneATSuhkiwz4BURBQ==", classnum)
        ldif_file.writelines(ldif_item)
finally:
    ldif_file.close()
