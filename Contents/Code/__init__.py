# -*- coding: utf-8 -*-
from __builtin__ import enumerate
from time import mktime
from datetime import datetime


PLUGIN_TITLE = 'Forsvaret i dag'
RSS_FEED = 'http://forsvaret.no/aktuelt/publisert/forsvaret-i-dag/_layouts/listfeed.aspx?List=366E5F82-17CB-4CD0-86BA-9B4C2A750490'


def Start():
	icon = 'icon-default.png'
	art = 'art-default.jpg'
	Plugin.AddPrefixHandler('/photos/forsvaretidag', ImageViewer, PLUGIN_TITLE, icon, art)
	Plugin.AddViewGroup('Coverflow', viewMode='Coverflow', mediaType='photos')
	MediaContainer.title1 = PLUGIN_TITLE
	MediaContainer.viewGroup = 'Coverflow'
	MediaContainer.art = R(art)
	DirectoryItem.thumb = R(icon)
	HTTP.CacheTime = CACHE_1HOUR


def ImageViewer():
	dir = MediaContainer()
	items = RSS.FeedFromURL(RSS_FEED).entries
	for i, item in enumerate(items):
		try:
			img = [x.href for x in item.links if x.rel == 'enclosure'][0]
		except:
			continue
		title = item.title
		updated = datetime.fromtimestamp(mktime(item.updated_parsed))
		counter = '%s/%s' % (i + 1, len(items))
		# Escape HTML entities
		summary = HTML.ElementFromString( item.get('summary', '') ).text_content().replace('\n', ' ')
		summary = '%s\n%s\n%s   %s' % (title, summary, counter, days_ago(updated))
		dir.Append(PhotoItem(img, title=title, summary=summary))
	return dir


def days_ago(dt):
	now = datetime.now()
	delta = now - dt
	days = delta.days
	if days <= 0:
		return 'I dag'
	elif days == 1:
		return 'I går'
	else:
		return '%s dager siden' % days