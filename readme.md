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
 <h4>Details zum Künstler/Interpreten</h4>
 
    <content>plugin://script.helper.bumblebox?module=audiodb_info&amp;request=getArtistDetails&amp;artistname='Adele'</content>

Der Aufruf per Content-Methode befüllt ein ListItem, das per Plugin-Handle von Kodi bereitgestellt wird. Folgende Items werden befüllt:

    ListItem.Label:                             strArtist (Künstlername)
    ListItem.Label2:                            idArtist (ID des Künstlers)
    ListItem.IconImage:                         strArtistThumb (Thumbnail)
    ListItem.Art(banner)                        strArtistBanner
    ListItem.Art(icon)                          strArtistThumb
    ListItem.Property(Artist_strStyle):         strStyle (Genre)
    ListItem.Property(Artist_strCountry):       strCountry (Herkunftsland/-ort)
    ListItem.Property(Artist_strArtistBanner):  strArtistBanner oder strArtistLogo (Banner zuerst)
    ListItem.Property(Artist_intBornYear):      intBornYear (Geburtsjahr)
    ListItem.Property(Artist_intFormedYear):    intFormedYear (bekannt seit)
    ListItem.Property(Artist_strBiography):     strBiography[eingestellte Sprache] oder strBiographyEN oder 'not found'

<h4>Details zum Album</h4>

    <content>plugin://script.helper.bumblebox?module=audiodb_info&amp;request=getAlbumDetails&amp;artistname='A-ha'&amp;albumname='Lifelines'</content>

Der Aufruf per Content-Methode befüllt ein ListItem, das per Plugin-Handle von Kodi bereitgestellt wird. Folgende Items werden befüllt:

    ListItem.Label:                                 strAlbum (Album)
    ListItem.Label2:                                idArtist
    ListItem.IconImage:                             strAlbumThumb

    ListItem.Property('intYearReleased'):           intYearReleased (Erscheinungsjahr)
    ListItem.Property('strAlbumCDart'):
    ListItem.Property('strAlbumSpine'):
    ListItem.Property('strAlbumThumbBack'):
    ListItem.Property('strDescriptionDE'):          Beschreibung deutsch oder
    ListItem.Property('strDescriptionEN'):          Beschreibung Englisch
    ListItem.Property('strGenre'):
    ListItem.Property('strLabel'):
    ListItem.Property('strLocation'):
    ListItem.Property('strMood'):
    ListItem.Property('strReleaseFormat'):
    ListItem.Property('strSpeed'):
    ListItem.Property('strStyle'):


<h3>Implementierte Module:</h3>

Ermittelt die WAN-IP (vom Provider zugewiesene IP) und schreibt diese in das Control(10) der SystemSettingsInfo.xml. Dazu muss der Button mit der ID=96 mit dem Scriptaufruf im `<onclick>` (wie folgt) komplettiert werden. Schlägt der Aufruf fehl, wird die WAN per Notification ausgegeben.

    module=wanip        ermittelt WAN per 'http://ident.me' und gibt diese aus

    # Button #96
    <onclick>RunScript(script.helper.bumblebox, module=wanip)</onclick>
 