'''
Dictionary that contains file signatures and the programs that open them 

Taken from http://extension.nirsoft.net/txt
'''
#!/usr/bin/env python

def returnPrograms(fileSignature):
    
    programsDict = {'txt' : ['wordpad', 'notepad', 'notepad++', 'dreamweaver', 'editpad', 'pdfcreator', 'uedit32', 'swriter'], 
                    'rtf' : ['wordpad', 'notepad', 'notepad++', 'winword', 'pdfcreator', 'wps', 'swriter'], 
                    'xps' : ['notepad', 'iexplore', 'dreamweaver', 'pdfcreator', 'winfxdocobj', 'xpsrchvw', 'xpsviewer'], 
                    'jpg' : ['explorer', 'fsviewer', 'gimp', 'photoviewer', 'picasaphotoviewer', 'rundll32', 'snippingtool'], 
                    'png' : ['explorer', 'fsviewer', 'gimp', 'i_view32', 'mediainfo', 'paintdotnet', 'snippingtool', 'rundll32', 'shimgvw', 'wlxphotogallery', 'photoshop', 'photoviewer', 'picasaphotoviewer'], 
                    'zip' : ['7zfm', '7z', 'zip', 'winzip', 'explorer', 'pdfcreator', 'uniextract', 'winarchiver', 'winrar', 'winzip32', 'winzip64'], 
                    'mht' : ['firefox', 'iexplore', 'msohtmed', 'opera', 'pdfcreator', 'uniextract', 'rundll32'], 
                    'html' : ['chrome', 'dreamweaver', 'excel', 'explorer', 'firefox', 'iexplore', 'mshtml', 'msohtmed', 'notepad++', 'notepad', 'opera', 'pdfcreator', 'rundll32', 'sbrowser'], 
                    'htm' : ['chrome', 'dreamweaver', 'excel', 'explorer', 'firefox', 'iexplore', 'mshtml', 'msohtmed', 'notepad++', 'notepad', 'opera', 'pdfcreator', 'rundll32', 'sbrowser'], 
                    'pdf' : ['acrobat', 'acrord32', 'firefox', 'foxitreader', 'foxitr~1', 'pdfcreator', 'pdfxcview', 'sumatrapdf', 'winword'], 
                    'doc' : ['moc', 'pdfcreator', 'swriter', 'winword', 'wordpad', 'wps'], 
                    'xls' : ['excel', 'moc', 'pdfcreator', 'scalc', 'soffice', 'xlview']}
    
    for key in programsDict.keys():
        if key == fileSignature:
            return programsDict[key]