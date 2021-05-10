import json

def GenDisplay(jObj):
    name = jObj["name"]
    sendName = name[0:1].upper() + name[1:]

    htmlData = '<!DOCTYPE html>\n'+\
               '<html>\n' +\
               '<script src="jquery-3.4.1.min.js"></script>\n'+ \
                '<script src="' + name + '.js"></script>\n'+\
               ' <body>  <br>\n' +\
               ' <head>\n' +\
                '<h2>Display ' + sendName + ' Page</h2>\n' +\
        '''
         <br>
      </head>
      <br>
      <button type="button" id="displayData" value="Display Data" onclick='displayData()'>Display Data</button>
      <div id="dpResults">
      </div>
    </body>
    </html>
'''
    f = open(name + '_display.html', "w")
    f.write(htmlData)
    print('Display HTML file ' + jObj['name'] + '_display.html successfully generated')
    f.close()



