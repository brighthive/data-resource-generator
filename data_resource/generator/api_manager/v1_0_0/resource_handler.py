"""Generic Resource Handler."""
from data_resource.generator.api_manager.v1_0_0.crud_functions import (
    ResourceRead,
    ResourceCreate,
    ResourceUpdate,
    ResourceQuery,
)
from data_resource.generator.api_manager.v1_0_0.crud_functions.mn_functions import (
    MnRead,
    MnUpdate,
)


class ResourceHandler(
    ResourceRead, ResourceCreate, ResourceUpdate, ResourceQuery, MnRead, MnUpdate
):
    pass
