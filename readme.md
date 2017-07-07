<h1>script.helper.bumblebox</h1>

Die script.helper.bumblebox vereint diverse Datenbankabfragen und Skriptlets un einem Programm. Die Bubmlebox kann sowohl als Plugin als auch als Skript aus Kodi heraus gestartet werden. Das bietet die Möglichkeit, u.a. Listitems per Content-Methode dynamisch zu befüllen.
 
 
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
 