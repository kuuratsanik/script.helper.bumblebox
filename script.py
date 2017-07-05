# -*- encoding utf-8 -*-

import sys
import urllib
import urlparse

import xbmc
import xbmcgui
import xbmcaddon

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


def getParams(url):
    return dict(urlparse.parse_qsl(urlparse.urlsplit(url).query))


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
                return False
            log('no data received, wait 500 msec for %s. try' % (v))
            xbmc.sleep(500)


def setWindowProperties(property_name, property):
    if property == None: return False
    for k, v in property[0].iteritems():
        xbmcgui.Window(WINDOW_ID).setProperty(property_name + k, NoneToStr(v))
    return True

def getArtistDetails(data):
    if setWindowProperties('Artist_', data['artists']):
        pref_lang = 'strBiography%s' % (language)

        if (pref_lang or 'strBiographyEN') in data['artists'][0]:
            xbmcgui.Window(WINDOW_ID).setProperty('Artist_Info', 'yes')
            try:
                if NoneToStr(data['artists'][0][pref_lang]) != '':
                    xbmcgui.Window(WINDOW_ID).setProperty('Artist_strBiography', data['artists'][0][pref_lang])
                    log('found artist biography in preferred language')
            except IndexError:
                xbmcgui.Window(WINDOW_ID).setProperty('Artist_strBiography', NoneToStr(data['artists'][0]['strBiographyEN']))
                log('found artist biography in EN only')
        else:
            xbmcgui.Window(WINDOW_ID).setProperty('Artist_strBiography', LS(32100))
            log('no artist biography available')
    else:
        xbmcgui.Window(WINDOW_ID).setProperty('Artist_Info', 'no')
        log('no artist biography available')

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

    try:
        param = getParams('script://%s?%s' % (sys.argv[0], sys.argv[1]))
    except IndexError:
        log('no additional parameters provided', level=xbmc.LOGFATAL)
        sys.exit(0)

    if param['module'] == 'audiodb_info':
        log('processing module audioDB')
        if param['request'] == 'getArtistDetails':
            if 'artistname' in param:
                _query = '/search.php?s=%s' % (param['artistname'])
            elif 'artistid' in param:
                _query = '/artist.php?i=%s' % (param['artistid'])
            elif 'artistmbid' in param:
                _query = '/artist-mb.php?i=%s' % (param['artistmbid'])
            data = GetJSONfromUrl('%s/%s%s' % (AUDIO_DB, API_Key, _query))
            if data: getArtistDetails(data)
        elif param['request'] == 'getAlbumDetails':
            if 'artistname' in param and 'albumname' in param:
                _query = '/searchalbum.php?s=%s&a=%s' % (param['artistname'], param['albumname'])
            elif 'albumid' in param:
                _query = '/album.php?m=%s' % (param['albumid'])
            elif 'albummbid' in param:
                _query = '/album-mb.php?i=%s' % (param['albummbid'])
            data = GetJSONfromUrl('%s/%s%s' % (AUDIO_DB, API_Key, _query))
            if data: getAlbumDetails(data)
        elif param['request'] == 'getTrackDetails':
            if 'artistname' in param and 'trackname' in param:
                _query = '/searchtrack.php?s=%s&t=%s' % (param['artistname'], param['trackname'])
            if 'trackid' in param:
                _query = '/track.php?h=%s' % (param['trackid'])
            elif 'trackmbid' in param:
                _query = '/track-mb.php?i=%s' % (param['trackmbid'])
            data = GetJSONfromUrl('%s/%s%s' % (AUDIO_DB, API_Key, _query))
            if data: setWindowProperties('Track_', data['tack'])
        else:
            log('no API entry found for %s' % (param['request']))

    elif param['module'] == 'wanip':
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

    log('script finished')
