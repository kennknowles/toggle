from __future__ import absolute_import
from couchdbkit.ext.django.schema import *


TOGGLE_ID_PREFIX = 'hqFeatureToggle'


class Toggle(Document):
    """
    A very simple implementation of a feature toggle. Just a list of usernames
    attached to a slug.
    """
    slug = StringProperty()
    enabled_users = ListProperty()

    def save(self, **params):
        if ('_id' not in self._doc):
            self._doc['_id'] = generate_toggle_id(self.slug)
        super(Toggle, self).save(**params)

    @classmethod
    def get(cls, docid, rev=None, db=None, dynamic_properties=True):
        if not docid.startswith(TOGGLE_ID_PREFIX):
            docid = generate_toggle_id(docid)
        return super(Toggle, cls).get(docid, rev=None, db=None, dynamic_properties=True)


def generate_toggle_id(slug):
    # use the slug to build the ID to avoid needing couch views
    # and to make looking up in futon easier
    return '{prefix}-{slug}'.format(prefix=TOGGLE_ID_PREFIX, slug=slug)
