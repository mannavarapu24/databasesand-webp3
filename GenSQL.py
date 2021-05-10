import json
def getMaxLen(group):
    max = 0
    for item in group:
        if len(item["value"]) > max: max = len(item["value"])
    return max
def GenSQL(jObj):
    primaryTblName = jObj["name"]
    fkcheck = 'SET FOREIGN_KEY_CHECKS = '
    ssql, pkeyline, pkeys  = '', '', []                  # secondarysql  primary key line, Support multiple primary keys
    pkeyDDLline = ''                                     #DDL line for secondary table
    psql = fkcheck + '0;\n' + 'DROP TABLE IF EXISTS `' + primaryTblName + '`;\n'          #primary sql
    psql += 'CREATE TABLE `' + primaryTblName + '` (\n'
    elements = jObj["elements"]
    for element in elements:
        column_name = element["ename"]
    #    print ("processing ---",element)
        if element["etype"] in ['textbox','selectlist','radiobutton']:
            if element['etype'] in ['selectlist', 'radiobutton']:
                maxlength = getMaxLen(element['group'])
            else:
                maxlength = element['maxlength']
            s = '`' + column_name + '` '
            if element['datatype'] == 'integer':
                s += 'int '; ctype = 'int '
            elif element['datatype'] == 'string':
                s += 'varchar(' + str(maxlength) + ') '; ctype = 'varchar(' + str(maxlength) + ') '
            if 'required' in element.keys(): s += 'NOT NULL'
            psql += "    " + s + ',\n'
            if 'key' in element.keys():
                pkeys.append(column_name)
                pk = '('
                for p in pkeys: pk += '`' + p + '`,'
                pk = pk[0:len(pk)-1] + ')'
                pkeyline = '    PRIMARY KEY ' + pk + ' );\n'
                pkeyDDLline += '    `' + p + '` ' + ctype + ',\n'
        if element['etype'] in ['checkbox', 'multiselectlist']:       #Secondary table with secondary sql
            tblName = primaryTblName + '_' + element['ename']
            if pkeyDDLline == '':
                print('Unable to CREATE DDL for secondary TABLE as PRIMARY TABLE ',primaryTblName,'does not have a PRIMARY KEY')
                continue
            ssql += 'DROP TABLE IF EXISTS `' + tblName + '`;\n'
            ssql += 'CREATE TABLE `' + tblName + '` (\n'
            ssql += pkeyDDLline[0:len(pkeyDDLline)-2] + ',\n'
            s = '`' + element['ename'] + '` '
            maxlength = getMaxLen(element["group"])
            if element['datatype'] == 'integer': s += 'int '
            elif element['datatype'] == 'string': s += 'varchar(' + str(maxlength) + ') '
            ssql += "    " + s + ', \n'
            pks = ''
            for i in range(len(pkeys)):
                pks += '`' + pkeys[i] + '`, '
            ssql += '    PRIMARY KEY (' + pks + '`' + element['ename'] + '`),\n'
    #        for i in range(len(pkeys)):
    #            ssql += '    CONSTRAINT (`' + pkeys[i] + '_fk`) FOREIGN KEY (`' + pkeys[i] + '`) REFERENCES `'+  primaryTblName + '` (`' + pkeys[i] + '`),\n'
            ssql = ssql[0:len(ssql)-2] + ');\n'
    if pkeyline == '':
        pkeyline = ' );\n'
        psql = psql[0:len(psql)-2]                 #remove , and \n from the end of psql
    sql = psql + pkeyline + ssql + fkcheck + '1;\n'
#    print(sql)
    # write out the html file
    file1 = open(primaryTblName + '.sql', "w")
    file1.write(sql)
    file1.close()
    print('sql file ' + primaryTblName + '.sql successfully generated')
    return
