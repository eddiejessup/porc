import util
import os

ORDER = [
    'Resource',
    'Client',
    'Collection',
    'Page',
    'Key',
    'Ref',
    'Event',
    'Relation'
]

dirname, filename = os.path.split(os.path.abspath(__file__))
maindir = os.path.normpath(os.path.join(dirname, '..'))

OUTPUT = os.path.join('source', 'index.md')
TEMPLATE = os.path.join(dirname, 'template.md')

util.generate_docs(ORDER, TEMPLATE, OUTPUT)