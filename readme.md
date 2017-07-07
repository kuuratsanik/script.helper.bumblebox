<h1>script.helper.bumblebox</h1>

Die script.helper.bumblebox vereint diverse Datenbankabfragen und Skriptlets in einem Programm. Die Bumblebox kann sowohl als Plugin als auch als Skript aus Kodi heraus gestartet werden. Das eröffnet die Möglichkeit, u.a. Listitems per Content-Methode dynamisch zu befüllen.
 
 
 <h2>Parameter:</h2>
 
 <h3>Implementierte Module:</h3>
 
     module=audiodb_info        Datenbankabfrage in http://www.theaudiodb.info
     request=getArtistDetails   holt Informationen zum Künstler

     artistname='Adele'         über den Namen oder
     artistid='08154711'        der Künstler-ID oder
     artistmbid='333'           der MB-ID
 
 <h4>Aufruf per Script-Methode:</h4>
 
    RunScript(script.helper.bumblebox, module=audiodb_info&amp;request=getArtistDetails&amp;artistname='Adele')
 
 <h4>Aufruf per Content-Methode (Plugin)</h4>
 
    <content>plugin://script.helper.bumblebox?module=audiodb_info&amp;request=getArtistDetails&amp;artistname='Adele'</content>

<h3>Implementierte Module:</h3>

Ermittelt die WAN-IP (vom Provider zugewiesene IP) und schreibt diese in das Control(10) der SystemSettingsInfo.xml. Dazu muss der Button mit der ID=96 mit dem Scriptaufruf im `<onclick>` (wie folgt) komplettiert werden. Schlägt der Aufruf fehl, wird die WAN per Notification ausgegeben.

    module=wanip        ermittelt WAN per 'http://ident.me' und gibt diese aus

    # Button #96
    <onclick>RunScript(script.helper.bumblebox, module=wanip)</onclick>
 