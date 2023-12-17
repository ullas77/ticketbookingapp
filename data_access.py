from application.models import show
from application.models import venue
from main import cache
@cache.cached(timeout=50, key_prefix='get all venues') 
def get_all_venues():
    venues= venue.query.all()
    return venues
@cache.memoize(50)
def get_venues_by_venuename(venuename):
    venues = venue.query.filter(venue.any(venuename=venuename)) 
    return venues.all()