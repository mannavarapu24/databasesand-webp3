import json
import sys
def valJSON(jObj):
    err = ''
    requiredFormTags = ['name','caption','backendURL','backendHost','backendPort','mysqlUserID','mysqlPWD','mysqlDB','elements']
    errFound = 0
    print('Checking for all Required json Tags in the main FORM json:')
    for key in requiredFormTags:
        if not(key in jObj.keys()):
            errFound = 1
            err += 'ERROR: Required FORM tag "' + key +'" is missing\n'
    if errFound == 0:
        print('OK: All Required FORM tags are present')
    else:
        print(err)
    print('Checking all elements for REQUIRED tags:')
    enameErr = 0
    etypeErr = 0
    datatypeErr = 0
    captionErr = 0
    enameDupErr = 0
    textboxErr = 0
    mslistErr = 0
    grpCaptionErr = 0
    grpValueErr = 0
    requiredFormTagErr = 0
    err = 0
    elements = jObj['elements']
    enames = []
    keys = []
    requiredFlds = []
    for element in elements:
        if 'required' in element.keys():
            requiredFlds.append(element['ename'])
            if element['required'] != 'true':
                err = 1
                print('ERROR: required tag of element "' + element['ename'] + '" does not have the value "true". It is "'+element['required']+'"')
        if 'key' in element.keys():
            keys.append(element['ename'])
            if element['key'] != 'key':
                err = 1
                print('ERROR: key tag of element "' + element['ename'] + '" does not have the value "key". It is "'+element['key']+'"')
        if 'ename' in element.keys():
            if element['ename'] in enames:
                enameDupErr = 1
                print('ERROR: DUPLICATE ename found "' + element['ename'] + '"')
            enames.append(element['ename'])
            if not('caption' in element.keys()):
                captionErr = 1
                print('ERROR: caption for element "'+element['ename']+'" NOT FOUND')
            if not('etype' in element.keys()):
                etypeErr = 1
                print('ERROR: etype for element "'+element['ename']+'" NOT FOUND')
            if element['etype'] not in ['submit','reset','textbox','checkbox','selectlist','multiselectlist','radiobutton']:
                err = 1
                print('ERROR: etype for element "' + element['ename'] + '" is of unknown type - "'+element['etype']+'"')
            if element['etype'] == 'textbox':
                if 'maxlength' not in element.keys():
                    txtboxErr = 1
                    print('ERROR: "maxlength" for element "' + element['ename'] + '" Not found')
                if 'size' not in element.keys():
                    txtboxErr = 1
                    print('ERROR: "size" for element "' + element['ename'] + '" Not found')
            if element['etype'] == 'multiselectlist':
                if 'size' not in element.keys():
                    mslistErr = 1
                    print('ERROR: "size" for "multislectlist" element "' + element['ename'] + '" Not found')
            if not(element['etype'] in ['submit','reset']):
                if not('datatype' in element.keys()):
                    datatypeErr = 1
                    print('ERROR: datatype for element "'+element['ename']+'" NOT FOUND')
                elif element['datatype'] not in ['string','integer']:
                    datatypeErr = 1
                    print('ERROR: datatype for element "'+element['ename']+'" is "'+ element['datatype']+'". Only "string" and "integer" are supported')
            if element['etype'] in ['checkbox', 'selectlist', 'multiselectlist', 'radiobutton']:
                if 'group' not in element.keys():
                    requiredFormTagErr = 1
                    print('ERROR: "group" tag for element "' + element['ename'] + '" of etype "' + element['etype'] + '" Not Found')
                else:
                    for gr in element['group']:
                        if 'caption' not in gr.keys():
                            grpCaptionErr = 1
                            print('ERROR: "group" tag for element "' + element['ename'] + '" of etype "' + element['etype'] + '" is Not Found')
                        if 'value' not in gr.keys():
                            grpValueErr = 1
                            print('ERROR: "value" tag for element "' + element['ename'] + '" of etype "' + element['etype'] + '" is Not Found')
        else:
            enameErr = 1
            print('ERROR: ename is MISSING for element: ' + element)
    if enames.count('submit') == 0:
        err = 1
        print('ERROR: This JSON does not have "submit" element')
    elif enames.count('submit') > 1:
        err = 1
        print('ERROR: This JSON has more than 1 "submit" element')
    else:
        print('OK: This JSON has exactly 1 "submit" element')
    if enames.count('reset') > 1:
        err = 1
        print('ERROR: this JSON has more than 1 "reset" element')
    else:
        print('OK: This JSON has 0 or 1 "reset" element')
    if len(requiredFlds)== 0:
        Err = 1
        print('ERROR: this JSON does not have any element as "required". Atleast 1  element must be "required"')
    else:
        print('OK: Atleast one "required" element found')
    if datatypeErr ==0:
        print('OK: dataypes of all elements are either "string" or "integer"')
    if len(keys)== 0:
        err = 1
        print('ERROR: this JSON does not have any element as key. Atleast 1 key element is required')
    else:
        print('OK: Atleast one "key" element found')
    if requiredFormTagErr == 0:
        print('OK: All Required element tags are present')
    if captionErr == 0:
        print('OK: All elements have "caption" tag')
    if etypeErr == 0:
        print('OK: All elements have "etype" tag')
    if enameDupErr == 0:
        print('OK: All elements have UNIQUE "ename" tags')
    if textboxErr == 0:
        print('OK: All "textbox" type elements have "size" and "maxlength" defined')
    if mslistErr == 0:
        print('OK: All "multiselectlist" type elements have "size" defined')
    if grpCaptionErr == 0:
        print('OK: All "group" sub-object have "caption" defined')
    if grpValueErr == 0:
        print('OK: All "group" sub-objects have "value" defined')
    err = err + etypeErr + enameErr + enameDupErr + errFound + captionErr + datatypeErr + textboxErr + mslistErr + requiredFormTagErr + grpCaptionErr + grpValueErr
    print(50*'-')
    return err


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("No json file specified on Command line")
    else:
        with open(sys.argv[1], 'r') as fp:
            jObj = json.load(fp)
            err = valJSON(jObj)
            if err:
                print('ERRORS FOUND - CANNOT CONTINUE')
