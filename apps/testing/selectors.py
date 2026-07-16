from apps.core.common.selectors.base_selector import BaseSelector

from .models import DummyItem


class DummyItemSelector(BaseSelector):

    MODEL = DummyItem
    RESOURCE_NAME = "DummyItem"
    LOOKUP_FIELD = "id"
    OWNER_PATH = "owner"
