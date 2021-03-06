import os, glob
import simplejson
import web

DATA_DIR = '../data/parse'
db = web.database(dbn=os.environ.get('DATABASE_ENGINE', 'postgres'), db='watchdog_dev')

def unidecode(d):
    newd = {}
    for k, v in d.iteritems():
        newd[k.encode('utf8')] = v
    return newd

def load():
    states = simplejson.load(file(DATA_DIR + '/states/index.json'))
    for code, state in states.iteritems():
        if 'aka' in state: state.pop('aka')
        db.insert('state', seqname=False, code=code, **unidecode(state))
    
    districts = simplejson.load(file(DATA_DIR + '/districts/index.json'))
    
    for name, district in districts.iteritems():
        db.insert('district', seqname=False, name=name, **unidecode(district))
    
    for fn in ['almanac', 'shapes', 'centers']:
        print 'loading', fn
        districts = simplejson.load(file(DATA_DIR + '/districts/%s.json' % fn))
        for name, district in districts.iteritems():
            db.update('district', where='name = $name', vars=locals(), **unidecode(district))
    
    politicians = simplejson.load(file(DATA_DIR + '/politicians/index.json'))
    for polid, pol in politicians.iteritems():
        db.insert('politician', seqname=False, id=polid, **unidecode(pol))
    
    for fn in ['govtrack', 'photos']:
        print 'loading', fn
        politicians = simplejson.load(file(DATA_DIR + '/politicians/%s.json' % fn))
        for polid, pol in politicians.iteritems():
            db.update('politician', where='id = $polid', vars=locals(), **unidecode(pol))
    

if __name__ == "__main__": load()
