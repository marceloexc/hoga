# HOGA

![](https://dont-look-back.marceloexc.com/junk/hoga_banner_full.jpg)
###### HOGA stands for ***Ho**arders **Ga***llery 
HOGA is a self-hosted media gallery viewer with support for several social media and image hosting sites. It is intended to serve data that
was initially downloaded using tools such as _[gallery-dl](https://github.com/mikf/gallery-dl)_, 
_[instaloader](https://github.com/instaloader/instaloader)_, and _[yt-dlp](https://github.com/yt-dlp/yt-dlp)_.

### HOGA is in pre-alpha

The current architecture for HOGA is still being experimented with. As of now, the main design decisions have been:
* Backend should be written in Python for greater interoperability with scraper-tools, which are also
mostly Python-based (opening up potential for scripting?)
* Frontend will be web-based, should be lightweight and have minimal JavaScript
* Easy to deploy on both baremetal and as a Docker container
* Easy to expose to the internet to share your galleries with others
* Lightweight on resources (I feel like this one will be the hardest!)

### Why?
I've been active on [r/Datahoarder](https://old.reddit.com/r/DataHoarder/) for a while now, but it is only because of
[recent events](https://en.wikipedia.org/wiki/Enshittification) within the past year or so that the concept of archiving
entire social media accounts has gotten even more popular. There are many wikiposts now that go into great detail for
configuring these scraping tools to get around API timeouts, download all metadata, etc. Which is great! But, I don't see
many people sharing the data that they download to the wider internet.

I don't think that uploading everything that you've downloaded with these toosl to a place like the [Internet Archive](https://archive.org) is a good idea.
If you were to upload an entire Twitter profile to archive.org, how would you set its metadata to be easily searchable?


### The obligatory and necessary
Some people would like to be forgotten! Ask yourself if the information you are hosting on HOGA respects the privacies 
of others if you choose to expose your galleries to the internet.