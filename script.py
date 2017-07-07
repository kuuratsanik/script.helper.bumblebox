# -*- encoding utf-8 -*-

import sys
import urllib
import urlparse

import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin

import json

addon = xbmcaddon.Addon()
addon_path = addon.getAddonInfo('path').decode('utf-8')
addon_id = addon.getAddonInfo('id')
LS = addon.getLocalizedString

AUDIO_DB = 'http://www.theaudiodb.com/api/v1/json/'
API_Key = 1
WINDOW_ID = 10135

def log(msg, level=xbmc.LOGDEBUG):
    xbmc.log('[%s] %s' % (addon_id, msg.encode('utf-8')), level)


def getParams(call):
    log('script parameters: %s' % (str(call)))
    params = {}
    scheme = urlparse.urlsplit(call[0]).scheme
    if scheme == '' or scheme == 'script':
        params.update(dict(urlparse.parse_qsl(urlparse.urlsplit('%s?%s' % (call[0], call[1])).query)))
    elif scheme == 'plugin':
        params.update(dict(urlparse.parse_qsl(urlparse.urlsplit('%s%s' % (call[0], call[2])).query)))
        params.update({'pluginHandle': call[1]})
    else:
        log('unknown scheme', level=xbmc.LOGFATAL)
    return params


def NoneToStr(str):
    return '' if str == None else str


def GetJSONfromUrl(URL):

    v = 1
    while True:
        data = urllib.urlopen(URL)
        try:
            return json.loads(data.read())
        except ValueError, e:
            v += 1
            if v > 5:
                log('no data received: %s' % (e.message), xbmc.LOGERROR)
                return None
            log('no data received, wait 500 msec for %s. try' % (v))
            xbmc.sleep(500)


def setWindowProperties(property_name, property):

    for k, v in property[0].iteritems():
        log('set Property %s to %s' % (property_name + k, NoneToStr(v)))
        xbmcgui.Window(WINDOW_ID).setProperty(property_name + k, NoneToStr(v))
    return True

def getArtistDetails(data, handle):
    pref_lang = 'strBiography%s' % (language)
    li = xbmcgui.ListItem(label=data[0].get('strArtist', ''), label2=data[0].get('idArtist', ''),
                          iconImage=data[0].get('strArtistThumb', ''))

    li.setArt({'icon': data[0].get('strArtistThumb', ''), 'banner': data[0].get('strArtistBanner', '')})
    li.setProperty('Artist_strCountry', data[0].get('strCountry', ''))
    li.setProperty('Artist_strArtistBanner', data[0].get('strArtistBanner', data[0].get('strArtistLogo', '')))
    li.setProperty('Artist_strStyle', data[0].get('strStyle', ''))
    li.setProperty('Artist_strCountry', data[0].get('strCountry', ''))
    li.setProperty('Artist_intBornYear', data[0].get('intBornYear', ''))
    li.setProperty('Artist_intFormedYear', data[0].get('intFormedYear', ''))
    li.setProperty('Artist_strBiography', data[0].get(pref_lang, data[0].get('strBiographyEN', LS(32100))))
    if handle is not None:
        xbmcplugin.addDirectoryItem(handle=int(handle), url='', listitem=li)
        xbmcplugin.endOfDirectory(int(handle), updateListing=True)

def getAlbumDetails(data):
    if setWindowProperties('Album_', data['album']):
        pref_lang = 'strDescription%s' % (language)
        if (pref_lang or 'strDescriptionEN') in data['album'][0]:
            xbmcgui.Window(WINDOW_ID).setProperty('Album_Info', 'yes')
            try:
                if NoneToStr(data['album'][0][pref_lang]) != '':
                    xbmcgui.Window(WINDOW_ID).setProperty('Album_strDescription', data['album'][0][pref_lang])
                    log('found album description in preferred language')
            except IndexError:
                xbmcgui.Window(WINDOW_ID).setProperty('Album_strDescription', NoneToStr(data['album'][0]['strDescriptionEN']))
                log('found album description in EN only')
        else:
            xbmcgui.Window(WINDOW_ID).setProperty('Album_strDescription', LS(32101))
            log('no album description available')
    else:
        xbmcgui.Window(WINDOW_ID).setProperty('Album_Info', 'no')
        log('no album description available')

if __name__ == '__main__':

    log('script started')
    language = xbmc.getLanguage(xbmc.ISO_639_1).upper()
    log('language is %s' % (language))
    xbmcgui.Window(WINDOW_ID).clearProperties()

    _query = ''
    _addonHandle = None
    param = getParams(sys.argv)

    if param.get('module', '') == 'audiodb_info':
        log('processing module audioDB')
        if param['request'] == 'getArtistDetails':
            if 'artistname' in param:
                _query = '/search.php?s=%s' % (param['artistname'])
            elif 'artistid' in param:
                _query = '/artist.php?i=%s' % (param['artistid'])
            elif 'artistmbid' in param:
                _query = '/artist-mb.php?i=%s' % (param['artistmbid'])
            data = GetJSONfromUrl('%s/%s%s' % (AUDIO_DB, API_Key, _query))
            if data.get('artists', None) is not None:
                getArtistDetails(data['artists'], param.get('pluginHandle', None))
            else:
                log('no artist info found', xbmc.LOGFATAL)
            '''
            
        elif param['request'] == 'getAlbumDetails':
            if 'artistname' in param and 'albumname' in param:
                _query = '/searchalbum.php?s=%s&a=%s' % (param['artistname'], param['albumname'])
            elif 'albumid' in param:
                _query = '/album.php?m=%s' % (param['albumid'])
            elif 'albummbid' in param:
                _query = '/album-mb.php?i=%s' % (param['albummbid'])
            data = GetJSONfromUrl('%s/%s%s' % (AUDIO_DB, API_Key, _query))
            if data is not None: getAlbumDetails(data)
        elif param['request'] == 'getTrackDetails':
            if 'artistname' in param and 'trackname' in param:
                _query = '/searchtrack.php?s=%s&t=%s' % (param['artistname'], param['trackname'])
            if 'trackid' in param:
                _query = '/track.php?h=%s' % (param['trackid'])
            elif 'trackmbid' in param:
                _query = '/track-mb.php?i=%s' % (param['trackmbid'])
            data = GetJSONfromUrl('%s/%s%s' % (AUDIO_DB, API_Key, _query))
            if data is not None: setWindowProperties('Track_', data['track'])
            
            '''
        else:
            log('no API entry found for %s' % (param['request']))

    elif param.get('module', '') == 'wanip':
        """
        Complete  button with id 96 in SystemSettingsInfo.xml (near line 288) with 
        <onfocus>RunScript(script.helper.bumblebox, module=wanip)</onfocus>
        """
        log('processing module wanip')
        ext_ip = urllib.urlopen('http://ident.me').read().decode('utf-8')
        wid = xbmcgui.Window(xbmcgui.getCurrentWindowId())
        try:
            wid.getControl(10).setLabel(LS(32110) + ': %s' % (ext_ip))
        except AttributeError:
            xbmcgui.Dialog().notification(LS(32110), ext_ip)
        except RuntimeError:
            xbmcgui.Dialog().notification(LS(32110), ext_ip)
    else:
        log('no or incorrect module parameter provided', level=xbmc.LOGFATAL)
    log('script finished')
