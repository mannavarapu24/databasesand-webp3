import json
import sys
def genhtml(jObj):
    elements = jObj["elements"]
    name = jObj["name"]
    caption = jObj["caption"]
    tb = 4
    ctb = 0
    html = ''
    html += ctb*' '+'<!DOCTYPE html>\n'
    html += ctb*' '+'<html>\n'   ; ctb += tb
    html += ctb*' '+'<script src="jquery-3.4.1.min.js"></script>\n'
    html += ctb*' '+'<script src="' + name + '.js"></script>\n'
    html += ctb*' '+'<body>\n'   ; ctb += tb
    html += ctb*' '+'<br><head>\n' ; ctb += tb
    html += ctb*' '+'<link rel="stylesheet" href="http://tinman.cs.gsu.edu/~raj/my.css">\n'
    html += ctb*' '+'<h2>'+caption+'</h2>\n'
    html += ctb*' '+'<br>\n' ; ctb -= tb
    html += ctb*' '+'</head>\n'
    html += ctb*' '+'<form id="'+name+'Form">\n'  ;ctb += tb
    for element in elements:
        ename = element["ename"]
    #    print ("processing ---",ename)
        if element['etype'] == 'textbox':       #in ['textbox','selectlist','radiobutton']:
                                                #if element['etype'] in ['selectlist', 'radiobutton']:
            html += ctb*' '+'<b><label>'+element['caption']+'</label></b>\n'
            html += ctb*' '+'<input type="text" id="'+ename+'" size="'+element['size']+'" maxlength="'+element['maxlength']+'"><br><br>\n'
        elif element['etype'] == 'checkbox':
            html += ctb * ' ' + '<b><label>' + element['caption'] + '</label></b><br>\n'
            for option in element['group']:       #loop thru the options
                checked = ''
                if 'checked' in option.keys(): checked = ' checked="checked"'
                html += ctb*' '+'<input type="checkbox" name ="'+ename+'"'+checked+' value="'+option['value']+'">'+option['caption']+'<br>\n'
            html += ctb * ' ' +'<br>\n'
        elif element['etype']  in ['selectlist','multiselectlist']:
            if element['etype'] == 'multiselectlist':
                multi = 'size="'+element['size']+'" multiple="multiple" '
            else:
                multi = ''
            html += ctb*' ' + '<b><label>' + element['caption'] + '</label></b>\n'
            html += ctb*' ' + '<select name="' + ename + '" ' + multi + 'id="' + ename + '"><br>\n';   ctb += tb
            for option in element['group']:       #loop thru the options
                html += ctb*' '+'<option value="'+option['value']+'">'+option['caption']+'</option>\n'
            ctb -= tb
            html += ctb*' '+'</select>\n'
            html += ctb*' '+'<br><br>\n'
        elif element['etype']  == 'radiobutton':
            html += ctb*' ' + '<b><label>' + element['caption'] + '</label></b><br>\n'
            for option in element['group']:       #loop thru the options
                html += ctb*' ' + '<input type="radio" name="' + ename + '" ' + 'value="' + option['value'] + '">'+option['caption']+'<br>\n';
            html += ctb*' '+'<br><br>\n'
        elif element['etype']  == 'submit':
            html += ctb*' '+'<br><br><br>\n'
            html += ctb*' ' + '<button type="button" id="submit" value="'+element['caption']+'" onclick="runQuery()">' +element['caption']+'</button>\n'
        elif element['etype']  == 'reset':
            html += ctb*' '+'<br><br><br>\n'
            html += ctb*' ' + '<button type="reset" id="reset" value="'+element['caption']+'" onclick="clearData()">' +element['caption']+'</button>\n'
    html += ctb*' '+'<h3><b>Results:</b></h3>\n'
    html += ctb*' '+'<div id="insert_result"></div>\n'
    html += ctb*' '+'<br>\n'     ; ctb -= tb
    html += ctb*' '+'</form>\n'  ;ctb -= tb
    html += ctb*' '+'</body>\n'  ; ctb -= tb
    html += ctb*' '+'</html>\n'

# write out the html file
    file1 = open(name+'.html', "w")
    file1.write(html)
    file1.close()
    print('html file '+name+'.html successfully generated')
    return (html)

if __name__ == "__main__":
    print(sys.argv)
    print(len(sys.argv))
    if len(sys.argv) == 1:
        print("No json file specified on Command line")
    else:
        with open(sys.argv[1], 'r') as fp:
            jObj = json.load(fp)
            html = genhtml(jObj)
            print(html)
