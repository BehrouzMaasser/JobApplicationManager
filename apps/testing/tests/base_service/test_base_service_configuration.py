import pytest

from apps.core.common.services.base_service import BaseService

from apps.testing.models import DummyItem
from apps.testing.selectors import DummyItemSelector


# ---------------------------------------------------------------------
# Missing required configuration
# ---------------------------------------------------------------------

def test_missing_model_configuration_raises_type_error():

    with pytest.raises(TypeError, match="MODEL"):

        class MissingModelService(BaseService):

            SELECTOR = DummyItemSelector

            CREATE_FIELDS = ()
            SCALAR_UPDATABLE_FIELDS = ()
            M2M_UPDATABLE_FIELDS = ()
            REQUIRED_M2M_FIELDS = ()
            NON_EMPTY_M2M_FIELDS = ()
            M2M_OWNER_FIELD_MAP = {}

            @classmethod
            def _validate_resolved_instance(cls, **kwargs):
                pass


def test_missing_selector_configuration_raises_type_error():

    with pytest.raises(TypeError, match="SELECTOR"):

        class MissingSelectorService(BaseService):

            MODEL = DummyItem

            CREATE_FIELDS = ()
            SCALAR_UPDATABLE_FIELDS = ()
            M2M_UPDATABLE_FIELDS = ()
            REQUIRED_M2M_FIELDS = ()
            NON_EMPTY_M2M_FIELDS = ()
            M2M_OWNER_FIELD_MAP = {}

            @classmethod
            def _validate_resolved_instance(cls, **kwargs):
                pass


@pytest.mark.parametrize(
    "attribute",
    (
        "CREATE_FIELDS",
        "SCALAR_UPDATABLE_FIELDS",
        "M2M_UPDATABLE_FIELDS",
        "REQUIRED_M2M_FIELDS",
        "NON_EMPTY_M2M_FIELDS",
        "M2M_OWNER_FIELD_MAP",
    ),
)
def test_missing_required_configuration(attribute):

    namespace = {
        "MODEL": DummyItem,
        "SELECTOR": DummyItemSelector,
        "CREATE_FIELDS": (),
        "SCALAR_UPDATABLE_FIELDS": (),
        "M2M_UPDATABLE_FIELDS": (),
        "REQUIRED_M2M_FIELDS": (),
        "NON_EMPTY_M2M_FIELDS": (),
        "M2M_OWNER_FIELD_MAP": {},
        "_validate_resolved_instance": classmethod(lambda cls, **kwargs: None),
    }

    namespace.pop(attribute)

    with pytest.raises(TypeError, match=attribute):
        type("InvalidService", (BaseService,), namespace)


# ---------------------------------------------------------------------
# Invalid MODEL
# ---------------------------------------------------------------------

def test_model_must_inherit_from_django_model():

    class InvalidModel:
        pass

    with pytest.raises(TypeError, match="MODEL"):

        class InvalidService(BaseService):

            MODEL = InvalidModel
            SELECTOR = DummyItemSelector

            CREATE_FIELDS = ()
            SCALAR_UPDATABLE_FIELDS = ()
            M2M_UPDATABLE_FIELDS = ()
            REQUIRED_M2M_FIELDS = ()
            NON_EMPTY_M2M_FIELDS = ()
            M2M_OWNER_FIELD_MAP = {}

            @classmethod
            def _validate_resolved_instance(cls, **kwargs):
                pass


# ---------------------------------------------------------------------
# Invalid SELECTOR
# ---------------------------------------------------------------------

def test_selector_must_inherit_from_base_selector():

    class InvalidSelector:
        pass

    with pytest.raises(TypeError, match="SELECTOR"):

        class InvalidService(BaseService):

            MODEL = DummyItem
            SELECTOR = InvalidSelector

            CREATE_FIELDS = ()
            SCALAR_UPDATABLE_FIELDS = ()
            M2M_UPDATABLE_FIELDS = ()
            REQUIRED_M2M_FIELDS = ()
            NON_EMPTY_M2M_FIELDS = ()
            M2M_OWNER_FIELD_MAP = {}

            @classmethod
            def _validate_resolved_instance(cls, **kwargs):
                pass


# ---------------------------------------------------------------------
# Invalid configuration types
# ---------------------------------------------------------------------

@pytest.mark.parametrize(
    "attribute,value",
    (
        ("CREATE_FIELDS", []),
        ("SCALAR_UPDATABLE_FIELDS", []),
        ("M2M_UPDATABLE_FIELDS", []),
        ("REQUIRED_M2M_FIELDS", []),
        ("NON_EMPTY_M2M_FIELDS", []),
        ("M2M_OWNER_FIELD_MAP", ()),
    ),
)
def test_configuration_has_expected_type(attribute, value):

    namespace = {
        "MODEL": DummyItem,
        "SELECTOR": DummyItemSelector,
        "CREATE_FIELDS": (),
        "SCALAR_UPDATABLE_FIELDS": (),
        "M2M_UPDATABLE_FIELDS": (),
        "REQUIRED_M2M_FIELDS": (),
        "NON_EMPTY_M2M_FIELDS": (),
        "M2M_OWNER_FIELD_MAP": {},
        "_validate_resolved_instance": classmethod(lambda cls, **kwargs: None),
    }

    namespace[attribute] = value

    with pytest.raises(TypeError):
        type("InvalidService", (BaseService,), namespace)


@pytest.mark.parametrize(
    "attribute",
    (
        "CREATE_FIELDS",
        "SCALAR_UPDATABLE_FIELDS",
        "M2M_UPDATABLE_FIELDS",
        "REQUIRED_M2M_FIELDS",
        "NON_EMPTY_M2M_FIELDS",
    ),
)
def test_tuple_configuration_must_contain_only_strings(attribute):

    namespace = {
        "MODEL": DummyItem,
        "SELECTOR": DummyItemSelector,
        "CREATE_FIELDS": (),
        "SCALAR_UPDATABLE_FIELDS": (),
        "M2M_UPDATABLE_FIELDS": (),
        "REQUIRED_M2M_FIELDS": (),
        "NON_EMPTY_M2M_FIELDS": (),
        "M2M_OWNER_FIELD_MAP": {},
        "_validate_resolved_instance": classmethod(lambda cls, **kwargs: None),
    }

    namespace[attribute] = ("valid", 123)

    with pytest.raises(TypeError):
        type("InvalidService", (BaseService,), namespace)


@pytest.mark.parametrize(
    "attribute",
    (
        "CREATE_FIELDS",
        "SCALAR_UPDATABLE_FIELDS",
        "M2M_UPDATABLE_FIELDS",
        "REQUIRED_M2M_FIELDS",
        "NON_EMPTY_M2M_FIELDS",
    ),
)
def test_tuple_configuration_must_not_contain_duplicates(attribute):

    namespace = {
        "MODEL": DummyItem,
        "SELECTOR": DummyItemSelector,
        "CREATE_FIELDS": (),
        "SCALAR_UPDATABLE_FIELDS": (),
        "M2M_UPDATABLE_FIELDS": (),
        "REQUIRED_M2M_FIELDS": (),
        "NON_EMPTY_M2M_FIELDS": (),
        "M2M_OWNER_FIELD_MAP": {},
        "_validate_resolved_instance": classmethod(lambda cls, **kwargs: None),
    }

    namespace[attribute] = (
        "name",
        "name",
    )

    with pytest.raises(TypeError):
        type("InvalidService", (BaseService,), namespace)


def test_owner_field_map_keys_must_be_strings():

    namespace = {
        "MODEL": DummyItem,
        "SELECTOR": DummyItemSelector,
        "CREATE_FIELDS": (),
        "SCALAR_UPDATABLE_FIELDS": (),
        "M2M_UPDATABLE_FIELDS": (),
        "REQUIRED_M2M_FIELDS": (),
        "NON_EMPTY_M2M_FIELDS": (),
        "M2M_OWNER_FIELD_MAP": {
            123: "owner",
        },
        "_validate_resolved_instance": classmethod(lambda cls, **kwargs: None),
    }

    with pytest.raises(TypeError):
        type("InvalidService", (BaseService,), namespace)


def test_owner_field_map_values_must_be_strings():

    namespace = {
        "MODEL": DummyItem,
        "SELECTOR": DummyItemSelector,
        "CREATE_FIELDS": (),
        "SCALAR_UPDATABLE_FIELDS": (),
        "M2M_UPDATABLE_FIELDS": (),
        "REQUIRED_M2M_FIELDS": (),
        "NON_EMPTY_M2M_FIELDS": (),
        "M2M_OWNER_FIELD_MAP": {
            "tags": object(),
        },
        "_validate_resolved_instance": classmethod(lambda cls, **kwargs: None),
    }

    with pytest.raises(TypeError):
        type("InvalidService", (BaseService,), namespace)


def test_scalar_and_m2m_updatable_fields_must_not_overlap():

    namespace = {
        "MODEL": DummyItem,
        "SELECTOR": DummyItemSelector,
        "CREATE_FIELDS": (),
        "SCALAR_UPDATABLE_FIELDS": (
            "name",
        ),
        "M2M_UPDATABLE_FIELDS": (
            "name",
        ),
        "REQUIRED_M2M_FIELDS": (),
        "NON_EMPTY_M2M_FIELDS": (),
        "M2M_OWNER_FIELD_MAP": {},
        "_validate_resolved_instance": classmethod(lambda cls, **kwargs: None),
    }

    with pytest.raises(TypeError):
        type("InvalidService", (BaseService,), namespace)


def test_configuration_fields_must_exist_on_model():

    namespace = {
        "MODEL": DummyItem,
        "SELECTOR": DummyItemSelector,
        "CREATE_FIELDS": (
            "does_not_exist",
        ),
        "SCALAR_UPDATABLE_FIELDS": (),
        "M2M_UPDATABLE_FIELDS": (),
        "REQUIRED_M2M_FIELDS": (),
        "NON_EMPTY_M2M_FIELDS": (),
        "M2M_OWNER_FIELD_MAP": {},
        "_validate_resolved_instance": classmethod(lambda cls, **kwargs: None),
    }

    with pytest.raises(TypeError):
        type("InvalidService", (BaseService,), namespace)