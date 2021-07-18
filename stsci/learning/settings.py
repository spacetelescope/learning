from os import getenv, environ, path

BASE = path.dirname(path.abspath(path.join(__file__, '..', '..')))


POOL = 'POOL' in environ
EXPORT_DIR = getenv('EXPORT_DIR', path.join(BASE, 'example', 'messages'))
TAG_LOOKUP = {
    'stars': 'STARS(ORG)',
    'itsd': 'ITSD(ORG)',
    'servicedesk': 'ServiceDesk(ORG)',
    'stsci': 'STScI(ORG)',
    'myst': 'MyST(PRODUCT)',
    'sso': 'SSO(PRODUCT)',
}
