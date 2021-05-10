import json
def sq (st):
    return "'"+st+"'"
def GenPyCode(jObj):
    dbtype = 'mysql'
    name = jObj['name']
    tb = 4               # Default tab
    ctb = 0              # current tab
    code = '''
from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import request
import mysql.connector as mysql
import sqlite3
from flask_cors import CORS
import os
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
CORS(app)

@app.route('/webforms/display/', methods=['GET'])
'''
    primaryTblName = jObj["name"]
    code += 'def get_' + primaryTblName + '():\n'
    ctb = tb
    if dbtype !='sqlite':
        code += ctb*' '+'db = mysql.connect(\n'  ; ctb += tb
        code += ctb*' '+'host = "localhost",\n'
        code += ctb*' '+'database = "'+jObj["mysqlDB"]+'",\n'
        code += ctb*' '+'user = "'+jObj["mysqlUserID"]+'",\n'
        code += ctb*' '+'passwd = "'+jObj["mysqlPWD"]+'",\n'
        code += ctb*' '+"auth_plugin='mysql_native_password'\n"; ctb -= tb
        code += ctb*' '+')\n'
    else:
        code += ctb*' '+"db = sqlite3.connect(os.path.join(basedir, 'test.sqlite3'))\n"
    #queries = []
    elements = jObj["elements"]
    #tblNames = [primaryTblName]  #List
    tblCols = {}                 #Dict  {"interests":["sno","sname","degree","interests_pls":["pls"]}
    tblColsDatatypes = {}
    tblColsRequired = {}
    tblColsKey = {}
    for element in elements:
        column_name = element["ename"]
        if element["etype"] in ['textbox','selectlist','radiobutton']:
            tblName = primaryTblName
        if element['etype'] in ['checkbox', 'multiselectlist']:     # Secondary table
            tblName = primaryTblName + '_' + element['ename']
            for i in range(len(tblColsKey[primaryTblName])):
                if tblColsKey[primaryTblName][i] == 'key':
                    tblCols[tblName] = [tblCols[primaryTblName][i]]
                    tblColsDatatypes[tblName] = [tblColsDatatypes[primaryTblName][i]]
                    tblColsKey[tblName] = ['key']
                    tblColsRequired[tblName] = ['required']
        if element['etype'] in ['submit','reset']:
            continue
        if 'required' in element.keys(): required = 'required'
        else: required = ''
        if 'key' in element.keys(): key = 'key'
        else: key = ''
        if tblName in tblCols.keys():
            tblCols[tblName].append(column_name)
            tblColsDatatypes[tblName].append(element['datatype'])
            tblColsKey[tblName].append(key)
            tblColsRequired[tblName].append(required)
        else:
            tblCols[tblName] = [column_name]
            tblColsDatatypes[tblName] = [element['datatype']]
            tblColsKey[tblName] = [key]
            tblColsRequired[tblName] = [required]

    for tblName, colNames in tblCols.items():                      # Tables
        query = 'query = "SELECT '
        for j in range(len(colNames)):               # Columns
            query += '`' + colNames[j] + '`, '
        query = query[0:len(query)-2]                  # remove space and ,
        query += ' FROM `'+tblName + '`;"'
        code += ctb*' '+query+'\n'
        code += ctb*' '+'cursor = db.cursor()\n'
        code += ctb*' '+'cursor.execute(query)\n'
        code += ctb*' '+'records = cursor.fetchall()\n'
        code += ctb*' '+tblName+' = [] \n'
        code += ctb*' '+'for record in records: \n'   ; ctb += tb
        objstr = ''
        for j in range(len(colNames)):
            objstr += "'"+colNames[j]+"':record["+str(j)+'], '
        objstr = objstr[0:len(objstr)-2]
        code += ctb*' '+tblName+'.append({'+objstr+'})\n' ; ctb -= tb
        resultStr = ''
    for tblName, colNames in tblCols.items():  # Tables
        resultStr += "'"+tblName+"':"+tblName+','
    resultStr = resultStr[0:len(resultStr)-1]
    code += ctb*' '+'result = {'+resultStr+'}\n'
    code += ctb*' '+'cursor.close()\n'
    code += ctb*' '+'db.close()\n'
    code += ctb*' '+'return jsonify(result)\n\n'  ;ctb -= tb
    rtStr = "@app.route('/webforms/insert/"
    paramStr = ''
    for i in range(len(tblCols[primaryTblName])):  # Primary Table Columns
        if tblColsRequired[primaryTblName][i] == 'required':
            rtStr += '<string:'+tblCols[primaryTblName][i]+'>/'
            paramStr += tblCols[primaryTblName][i] + ','
    rtStr += "', methods=['POST'])"
    paramStr = paramStr[0:len(paramStr)-1]     # drop the last ,
    code += ctb*' '+rtStr+'\n'
    code += ctb*' '+'def insert_'+primaryTblName+'('+paramStr+'):\n' ; ctb += tb
    if dbtype !='sqlite':
        code += ctb*' '+'db = mysql.connect(\n' ; ctb += tb
        code += ctb*' '+'host = "localhost",\n'
        code += ctb*' '+'database = "'+jObj["mysqlDB"]+'",\n'
        code += ctb*' '+'user = "'+jObj["mysqlUserID"]+'",\n'
        code += ctb*' '+'passwd = "'+jObj["mysqlPWD"]+'",\n'
        code += ctb*' '+"auth_plugin='mysql_native_password'\n"  ; ctb -= tb
        code += ctb*' '+')\n'
    else:
        code += ctb*' '+"db = sqlite3.connect(os.path.join(basedir, 'test.sqlite3'))\n"
    code += ctb*' ' + 'cursor = db.cursor()\n'
    code += ctb*' ' + 'try:\n'    ; ctb += tb
    i  = 1
    for tblName, colNames in tblCols.items():  # Tables
        sql = 'sql'+str(i)+' = "INSERT INTO `'+tblName+'` VALUES ("+'
        st = ''
        for j in range(len(tblCols[tblName])):
            if i > 1 and tblColsKey[tblName][j] == '':          # Non key column in secondary table, Need to loop and use the loop variable
                code += ctb * ' ' + 'for '+tblCols[tblName][j]+' in ' + "request.json['"+tblCols[tblName][j]+"']:\n" ; ctb += tb
            if tblColsDatatypes[tblName][j] == 'integer':
                if i > 1 and tblColsKey[tblName][j] == '':     # Non key column in secondary table, Need to loop and use the loop variable INTEGER eg: "+pls+",
                    st += '"+' + tblCols[tblName][j]+'+",'
                else:                                          # Non-Key in secondary or any Col in Primary INTEGER eg: "request.json['sname']+",
                    st += "request.json["+sq(tblCols[tblName][j])+"]+" + '"' + ","
            else:                    # enclose value in single quotes (string)
                if i > 1 and tblColsKey[tblName][j] == '':     # Non key column in secondary table, Need to loop and use the loop variable STRING eg: '"+pls+"'"+",
                    st += "'" + '"+' + tblCols[tblName][j] + "+" + '"' + "'"  + ','
                else:                                          # Non-Key in secondary or any Col in Primary STRING eg: '"+request.json['sname']+"',
                    st += "'" + '"+' + "request.json[" + sq(tblCols[tblName][j]) + "]+" + '"' + "',"
    # Generate this output for primary table or secondary table, non-key and String type
    #      sql1 = "INSERT INTO `interests` VALUES ("+request.json['sid']+","'"+request.json['sname']+"'","'"+request.json['degree']+"'"+");"
    # Generate this output for secondary table NON-KEY (checkBox or Multi-Select) - Use loop variable eg: '"+pls+"'"+",
    #      sql2 = "INSERT INTO `interests_pls` VALUES ("request.json['sid']+","'"+pls+"'"+");"
        st = st[0:len(st)-1]
        code += ctb*' '+sql+st+'"+");"\n'
        code += ctb*' '+'cursor.execute(sql'+str(i)+')\n'
        if i > 1 and tblColsKey[tblName][j] == '': ctb -= tb
        i += 1
    code += ctb*' '+'db.commit()\n'
    code += ctb*' '+'cursor.close()\n'
    code += ctb*' '+'db.close()\n'
    st = ''
    for i in range(len(tblCols[primaryTblName])):
        if tblColsRequired[primaryTblName][i] == 'required':
            st += '"'+tblCols[primaryTblName][i]+'":'+"request.json['"+tblCols[primaryTblName][i]+"'],"
    st = st[0:len(st)-1]
    code += ctb*' '+'result = {"ok":True,'+st+'}\n'
    code += ctb*' '+'return jsonify(result)\n'  ; ctb -= tb
    code += ctb*' '+'except Exception as e:\n'  ; ctb += tb
    code += ctb*' '+'db.rollback()\n'
    code += ctb*' '+'cursor.close()\n'
    code += ctb*' '+'db.close()\n'
    st = ''
    for i in range(len(tblCols[primaryTblName])):
        if tblColsRequired[primaryTblName][i] == 'required':
            st += '"'+tblCols[primaryTblName][i]+'":'+"request.json['"+tblCols[primaryTblName][i]+"'],"
    st = st[0:len(st)-1]
    code += ctb*' '+'result = {"ok":False,'+st+'}\n'
    code += ctb*' '+'return jsonify(result)\n\n'  ; ctb -= tb  ; ctb -= tb
    code += ctb*' '+'@app.errorhandler(404)\n'
    code += ctb*' '+'def not_found(error):\n'     ; ctb += tb
    code += ctb*' '+"return make_response(jsonify({'error': 'Not found'}), 404)\n\n"  ; ctb -= tb
    code += ctb*' '+"if __name__ == '__main__':\n"  ; ctb += tb
    code += ctb*' '+"app.run(host='localhost',debug=True)"

#    print(tblCols)
#    print(tblColsDatatypes)
#    print(tblColsKey)
#    print(tblColsRequired)
#    print(code)
# write out the html file
    file1 = open(name + '.py', "w")
    file1.write(code)
    file1.close()
    print('python code for backend ' + name + '.py successfully generated')
    return