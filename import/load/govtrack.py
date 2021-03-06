"""
load data from govtrack.us

from: data/crawl/govtrack/people.xml
  to: data/parse/politicians/govtrack.json
"""

import simplejson
from parse import govtrack

reps = simplejson.load(file('../data/parse/politicians/index.json'))
dist2rep = {}
for repid, rep in reps.iteritems():
    dist2rep[rep['district']] = repid

mapping = {
  'bioguideid': 'bioguideid',
  'birthday': 'birthday',
  'firstname': 'firstname',
  'gender': 'gender',
  'id': 'govtrackid',
  'lastname': 'lastname',
  'middlename': 'middlename',
  'osid': 'opensecretsid',
  'party': 'party',
  'religion': 'religion',
  'represents': 'district',
  'url': 'officeurl'
}

out = {}
def callback(pol):
    newpol = {}
    for k, v in mapping.iteritems():
        if k in pol: newpol[v] = pol[k]
    
    if pol.get('represents') and pol.represents in dist2rep: 
        rep = dist2rep[pol.represents]
        if pol.lastname.lower().replace(' ', '_') in rep:
            out[rep] = newpol

if __name__ == "__main__":
    govtrack.main(callback)
    print simplejson.dumps(out, indent=2, sort_keys=True)
