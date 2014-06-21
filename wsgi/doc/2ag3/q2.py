class Example(object):
_cp_config = {
# if there is no utf-8 encoding, no Chinese input available
'tools.encode.encoding': 'utf-8',
'tools.sessions.on' : True,
'tools.sessions.storage_type' : 'file',
'tools.sessions.locking' : 'explicit',
'tools.sessions.storage_path' : data_dir+'/tmp',
# session timeout is 60 minutes
'tools.sessions.timeout' : 60
}

@cherrypy.expose
def index(self):
    output = ''

    form = '''
    <form action='action'>
    num1:<INPUT type='text' name='num1'>
    num2:<INPUT type='text'  name='num2'>
    <input type=submit>
    <input type=reset>
    </form>
    '''
    output += form
    return output
@cherrypy.expose
def action(self, num1=9, num2=9):
    num1 = int(num1)
    num2 = int(num2)
    output = ''
    for i in range(num1):
        for j in range(num2):
            output += str(i) + '*' + str(j) + '=' + str(i*j) + '<br />'
    return output
