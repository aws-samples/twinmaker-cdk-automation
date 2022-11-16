# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved. 2021
# SPDX-License-Identifier: Apache-2.0

import logging
from datetime import datetime
from random import seed
from random import randint
import hashlib

from udq_utils.udq import (
    SingleEntityReader,
    IoTTwinMakerDataRow,
    IoTTwinMakerUdqResponse,
)
from udq_utils.udq_models import (
    IoTTwinMakerUDQEntityRequest,
    IoTTwinMakerReference,
    EntityComponentPropertyRef,
)

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)

# ---------------------------------------------------------------------------
#   Sample implementation of an AWS IoT TwinMaker UDQ Connector against AWS Timestream
#   consists of the EntityReader and IoTTwinMakerDataRow implementations
# ---------------------------------------------------------------------------


class RandomReader(SingleEntityReader):
    """
    The UDQ Connector implementation for our Timestream table
    It supports both single-entity queries and multi-entity queries and contains 2 utility functions to
    read from Timestream and convert the results into a IoTTwinMakerUdqResponse object
    """

    def __init__(self):
        pass

    # overrides SingleEntityReader.entity_query abstractmethod
    def entity_query(
        self, request: IoTTwinMakerUDQEntityRequest
    ) -> IoTTwinMakerUdqResponse:
        """
        This is a entityId.componentName.propertyId type query.
        The entityId and componentName is resolved into the externalId's for this component so we are getting
        telemetryAssetId and telemetryAssetType passed in. We are selecting all entries matching the passed in
        telemetryAssetType, telemetryAssetId and additional filters
        """
        LOGGER.info("RandomReader entity_query")

        selected_property = request.selected_properties[0]

        min = int(
            float(request.udq_context["properties"]["min"]["value"]["doubleValue"])
        )
        max = int(
            float(request.udq_context["properties"]["max"]["value"]["doubleValue"])
        )

        timestamp = request.start_time

        s = f"{timestamp}{request.entity_id}{request.component_name}{selected_property}"

        # This trick allows having coherent value for a given measure at a given time.
        # https://stackoverflow.com/questions/16008670/how-to-hash-a-string-into-8-digits
        seed_number = int(hashlib.sha256(s.encode("utf-8")).hexdigest(), 16) % 10**4
        seed(seed_number)

        return IoTTwinMakerUdqResponse(
            [
                RandomDataRow(
                    timestamp,
                    request.entity_id,
                    request.component_name,
                    selected_property,
                    min,
                    max,
                )
            ]
        )


class RandomDataRow(IoTTwinMakerDataRow):
    """
    The AWS IoT TwinMaker data row implementation for our Timestream data

    It supports the IoTTwinMakerDataRow interface to:
    - calculate the IoTTwinMakerReference ("entityPropertyReference") for a Timestream row
    - extract the timestamp from a Timestream row
    - extract the value from a Timestream row
    """

    def __init__(
        self,
        timestamp=None,
        entity_id=None,
        component_name=None,
        selected_property=None,
        min=0,
        max=100,
    ):
        self._timestamp = timestamp
        self._entity_id = entity_id
        self._component_name = component_name
        self._selected_property = selected_property
        self._min = min
        self._max = max

    # overrides IoTTwinMakerDataRow.get_iottwinmaker_reference abstractmethod
    def get_iottwinmaker_reference(self) -> IoTTwinMakerReference:
        """
        This function calculates the IoTTwinMakerReference ("entityPropertyReference") for a row
        """
        if self._entity_id and self._component_name:
            return IoTTwinMakerReference(
                ecp=EntityComponentPropertyRef(
                    self._entity_id, self._component_name, self._selected_property
                )
            )

    # overrides IoTTwinMakerDataRow.get_iso8601_timestamp abstractmethod
    def get_iso8601_timestamp(self) -> str:
        return self._timestamp

    # overrides IoTTwinMakerDataRow.get_value abstractmethod
    def get_value(self):
        return float(randint(self._min, self._max))


# Main Lambda invocation entry point, use the TimestreamReader to process events
# noinspection PyUnusedLocal
def lambda_handler(event, context):
    LOGGER.info("Event: %s", event)

    RANDOM_READER = RandomReader()
    result = RANDOM_READER.process_query(event)
    LOGGER.info("result:")
    LOGGER.info(result)
    return result
