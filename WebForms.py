import json
import sys
import genhtml
import ValidateJSON
import pyServer
import GenSQL
import GenerateJS
import genDisplayHtml


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("No json file specified on Command line")
    else:
        with open(sys.argv[1], 'r') as fp:
            jObj = json.load(fp)
            err = ValidateJSON.valJSON(jObj)
            if not(err):
                html = genhtml.genhtml(jObj)
                GenerateJS.GenJS(jObj)
                pyServer.GenPyCode(jObj)
                GenSQL.GenSQL(jObj)
                dhtml = genDisplayHtml.GenDisplay(jObj)
            else:
                print('ERRORS FOUND - CANNOT CONTINUE')


