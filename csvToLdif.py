#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import sys
import codecs

reload(sys)
sys.setdefaultencoding('utf8')

csv_filename = sys.argv[1].split('.')[0]


ldif_tmpl = '\
dn: cn={4},ou={3},ou={2},ou={1},cn={0},ou=People,dc=neuq,dc=edu.cn\n\
objectClass: inetOrgPerson\n\
objectClass: top\n\
cn: {5}\n\
sn: {6}\n\
givenName: {7}\n\
displayName: {8}\n\
o: {9}\n\
departmentNumber: {10}\n\
userPassword: {11}\n\
roomNumber: {12}\n\n'

create_grade_tree = '\
dn: ou={3},ou={2},ou={1},cn={0},ou=People,dc=neuq,dc=edu.cn\n\
objectClass: organizationalUnit\n\
objectClass: top\n\
ou: {4}\n\n'

department = {'1' : '经济系',
              '2' : '管理系',
              '3' : '商贸系',
              '4' : '电子信息系', 
              '5' : '自动化系',
              '6' : '外语系',
              '7' : '信息与计算科学系',
              '8' : '材料系', 
              '9' : '环境系'}

if len(sys.argv) != 3:
    print '请输入正确的参数：{0} [csv文件名], [专业名]\n'.format(sys.argv[0])
if len(csv_filename) != 3 or not csv_filename.isdigit():
    print 'csv文件名不符合规范，请修改为学号的前三位以标识系别与年级\n'

csv_file = codecs.open(sys.argv[1], 'r', "utf-8")
ldif_file = codecs.open('./{0}.ldif'.format(csv_filename), 'w', "utf-8");
try:
    dept = department[csv_filename[0]]
    grade = ''.join(["20", csv_filename[1:3]])
    pro = sys.argv[2]
    ldif_file.writelines(create_grade_tree.format('学生', dept, pro, grade, grade))
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
        ldif_item = ldif_tmpl.format('学生', dept, pro, grade, idnumber, idnumber, lastname, firstname, fullname, dept, pro, "{MD5}ISGMyneATSuhkiwz4BURBQ==", classnum)
        ldif_file.writelines(ldif_item)
finally:
    ldif_file.close()
