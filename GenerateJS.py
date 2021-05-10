import json
def GenJS(jObj):
    tb = 4
    ctb = 0
    js, err = '',''
    js = ctb * ' ' + 'function runQuery() {\n'
    ctb += tb
    for element in jObj['elements']:
        ename = element['ename']              #sid
        etype = element['etype']              #textbox
        if etype == 'textbox':
            js += ctb * ' ' +'const '+ename+' = document.getElementById("'+ename+'").value.trim();\n'
# 	const sid = document.getElementById("sid").value.trim();
        elif etype == 'selectlist':
            js += ctb * ' ' + 'const ' + ename + ' = document.querySelector("#' + ename + '").value;\n'
#    const degree = document.querySelector('#degree').value;
        elif etype == 'radiobutton':
            js += ctb * ' ' + 'const '+ename + ' = document.querySelector(\'input[name="' + ename + '"]:checked\').value;\n'
#    const semester = document.querySelector('input[name="semester"]:checked')
        elif etype == 'checkbox':
            js += ctb * ' ' + 'var ' + ename + ' = [];\n'
            js += ctb * ' '+ 'const '+etype + ' = document.querySelectorAll(\'input[name="' + ename +'"]:checked\');checkbox.forEach((checkbox) => { ' + ename + '.push(checkbox.value); });\n'


 #  const checkboxes = document.querySelectorAll('input[name="pls"]:checked');
 # let  pls = [];
 # checkboxes.forEach((checkbox) = > {
 #    pls.push(checkbox.value);
 # });

        elif etype == 'multiselectlist':
            js += ctb * ' ' + 'var ' + ename + ' = [];\n'
            js += ctb * ' ' + 'document.querySelectorAll(\'#' + ename + ' option:checked\').forEach((msl) => { ' + ename + '.push(msl.value);})\n'
#   var hobbies = [];
#    document.querySelectorAll('#hobbies option:checked').forEach((msl) = > {
#   hobbies.push(msl.value) });
#   checks the required field in the JSON format
    reqEnames = []
    for element in jObj['elements']:
        ename = element['ename']


        if ( 'required'in element.keys() ):
            if (element['required']== "true"):
                reqEnames.append(ename)
                js += ctb * ' ' + "var errors = '"+ "';\n"
                js += ctb * ' ' + 'if (' + ename + ' == "" ) {\n'
                ctb+=tb
                js += ctb * ' ' + 'errors += "Please fill  '+element['caption'] + ' " \n   }\n'
                ctb-=tb

                if (element['datatype'] == "integer"):
                    err += ctb * ' ' + 'var myRe =/\d*/;\n'
                    err += ctb * ' ' + 'if (myRe.exec('+ename+') == null) { \n'
                    ctb+=tb
                    err += ctb * ' ' + 'console.log(' + ename + '+" is not Number "+' + ename+');\n'
                    err += ctb * ' ' + 'errors += "Student Id must be a number" + '+ ename +';}\n'
                    ctb-=tb
# var errors = '';
#   if (sid == "") {
#        errors += "Student Id required\n"    }
  #   var  myRe = /\d {4} /;
#    if (myRe.exec(sid) == null) {
#    console.log("sid is not Number"+sid);
#    errors += "Student Id must be a 4 digit number "+ sid +"\n";
#    }
    err+= '''
        if (errors != '') {
	        console.log(errors);
	        alert(errors);
		    errors = '';
		    return
	    }
    '''

    js+=err
    creName = jObj["name"]
    sendName= creName[0:1].upper() + creName[1:]
    creName = "new" + creName[0:1].upper() + creName[1:]


    js+= ctb * ' ' + 'var ' + creName + '= {};\n'
    for element in jObj['elements']:
        ename = element['ename']
        etype = element['etype']
        if not(etype in ["submit","reset"] ):
            js += ctb * ' ' + creName + '["'+ ename + '"] = ' + ename + '\n'
#var newStudent = {};
#    newStudent["sname"] = sname;
#    newStudent["sid"] = sid;
#    newStudent["pls"] = pls;
#    newStudent["degree"] = degree;
#    newStudent["hobbies"] = hobbies;
#	console.log(newStudent);
    message =""
    collectedData =""
    for st in reqEnames:
        collectedData += "+" + st + " + '/' "
        message += "response." + st + '+ " " + '

#var htmlCode = "<p><b>Student " + response.sid + " " + response.sname + " " + "has been inserted";
#
    js += ctb * ' '+ "var url = '" + jObj["backendURL"] + "insert/'  " + collectedData + ";\n"
#var url = 'http://localhost:5000/webforms/insert/' + sid + '/' + sname + '/' ;

    messageSuccess = '"<p><b>' + sendName + ' " + ' + message + '" has been inserted; "'
    messageFailure = '"<p><b>' + sendName + ' " + ' + message + '" could not be inserted; "'
   # print (messageSuccess)
   # print (messageFailure)

    webString = '''
    $.ajax({
        url: url,
        type: 'POST',
        data: JSON.stringify('''+ creName + '''),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function (response) {
            if (response.ok)
            {  
        '''
    js += webString
    js += ctb * ' ' + 'var htmlCode = ' + messageSuccess + '\n'
    ctb += tb
    ctb += tb
    js += ctb * ' ' + '$("#insert_result").html(htmlCode)\n'
    js += ctb * ' ' + '} else { \n '
    js += ctb * ' ' + 'var htmlCode = ' + messageFailure + '\n'
    js += ctb * ' ' + '$("#insert_result").html(htmlCode); } },\n'
    js += ctb * ' ' + 'error: function (error) {\n'
    js += ctb * ' ' + 'alert("ERROR");\n'
    js += ctb * ' ' + '}\n'
    js += ctb * ' ' + ' });\n'
    js += ctb * ' ' + '};'

    '''
                var htmlCode = "<p><b>Student " + response.sid + " " + response.sname + " " + "has been inserted";
                $("#insert_result").html(htmlCode);
           
            } else {
                var htmlCode = "<p><b>Student " + response.sid + " " + response.sname + " " + "could not be inserted";
                $("#insert_result").html(htmlCode);
                
            }
        },
        error: function (error) {
            alert("ERROR");
            
        }
    }); 
    };
    '''
    js += '''
    function clearData() {
            document.getElementById("insert_result").innerHTML = "";
			return
    }
    function displayData() {
    '''

# var url = 'http://localhost:5000/webforms/display/';
    js += ctb * ' '+ "var url = '" + jObj["backendURL"] + "display/';\n"
    js += '''    
        $.ajax({
            url: url,
            type: 'GET',
            success: function (response) {
                Object.keys(response).forEach(function (key) {
            })
            var finalhtml = "";
            const tblNames = Object.keys(response);
            for (var i = 0; i < tblNames.length; i++) // loop thru the response for each table
            {
                html = `<table style="border:1px solid">`;
                html += "<br><b> Tablename: " + tblNames[i] + "</b><br><br>"
                const row1 = response[tblNames[i]][0]; // get first row of data for this table
                const columnNames = Object.keys(row1);
                for (var j = 0; j < columnNames.length; j++) { // loop thru first row to get the column names
                }
                var Row = '<tr>';
                columnNames.forEach(colm => {
                    Row += '<th style="border:1px solid">' + colm + '</th>';
                });
                Row += "</tr><tr>";
                for (var k = 0; k < response[tblNames[i]].length; k++) //loop thru all the rows of data
                {
                    const oneRow = response[tblNames[i]][k];
                    for (var l = 0; l < columnNames.length; l++) // loop thru each column in the row
                    {
                        Row += '<td style="border:1px solid">' + oneRow[columnNames[l]] + '</td>';
                    };
                    Row += "</tr><tr>";
                };
                html += Row + '</table>';
                finalhtml += html;
            }
            document.getElementById("dpResults").innerHTML = finalhtml;
        },
        error: function (error) {
            alert("ERROR");
        }
    });
    };

    '''
    #print(js)
    file1 = open(jObj['name'] + '.js', "w")
    file1.write(js)
    file1.close()
    print('js file ' + jObj['name'] + '.js successfully generated')
    return

'''
function clearData() {
            document.getElementById("insert_result").innerHTML = "";
			return
}
function displayData() {
    var url = 'http://localhost:5000/webforms/display/';
    $.ajax({
        url: url,
        type: 'GET',
        success: function (response) {
            console.log(response.interests);
            Object.keys(response).forEach(function (key) {
                console.log('Key : ' + key + ', Value : ' + response[key])
            })
            var finalhtml = "";
            console.log(response.interests_pls);
            console.log(response.interests_hobbies);
            const tblNames = Object.keys(response);
            for (var i = 0; i < tblNames.length; i++) // loop thru the response for each table
            {
                console.log("Table Name = " + tblNames[i]);
                html = `<table style="border:1px solid">`;
                html += "<br><b> Tablename: " + tblNames[i] + "</b><br><br>"
                const row1 = response[tblNames[i]][0]; // get first row of data for this table
                console.log('Row 1 = ' + row1);
                const columnNames = Object.keys(row1);
                for (var j = 0; j < columnNames.length; j++) { // loop thru first row to get the column names
                    console.log("ColumnNames : " + columnNames[j]);
                }
                var Row = '<tr>';
                columnNames.forEach(colm => {
                    Row += '<th style="border:1px solid">' + colm + '</th>';
                });
                Row += "</tr><tr>";
                for (var k = 0; k < response[tblNames[i]].length; k++) //loop thru all the rows of data
                {
                    const oneRow = response[tblNames[i]][k];
                    for (var l = 0; l < columnNames.length; l++) // loop thru each column in the row
                    {
                        Row += '<td style="border:1px solid">' + oneRow[columnNames[l]] + '</td>';
                    };
                    Row += "</tr><tr>";
                };
                html += Row + '</table>';
                finalhtml += html;
            }
            document.getElementById("dpResults").innerHTML = finalhtml;
        },
        error: function (error) {
            alert("ERROR");
            console.log(error);
        }
    });
};
'''




