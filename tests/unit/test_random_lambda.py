# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved. 2021
# SPDX-License-Identifier: Apache-2.0

import pytest
from os import path
import sys

# Add path to udq_utils module
dir_path = path.dirname(path.realpath(__file__))
sys.path.insert(0, "wind_farm/random_component/udq_helper_utils")

from wind_farm.random_component.lambda_.handler import lambda_handler  # noqa: E402


@pytest.fixture()
def twinmaker_event():
    """Generates TwinMaker Reader Event"""

    return {
        "workspaceId": "windfarm-sample",
        "selectedProperties": ["speed"],
        "startTime": "2022-11-15T14:33:02Z",
        "endTime": "2022-11-15T14:33:02Z",
        "startDateTime": 1668522782,
        "endDateTime": 1668522782,
        "properties": {
            "speed": {
                "definition": {
                    "dataType": {
                        "type": "DOUBLE",
                    },
                    "isTimeSeries": True,
                    "isRequiredInEntity": False,
                    "isExternalId": False,
                    "isStoredExternally": True,
                    "isImported": False,
                    "isFinal": False,
                    "isInherited": True,
                    "imported": False,
                    "requiredInEntity": False,
                    "inherited": True,
                    "final": False,
                    "storedExternally": True,
                    "externalId": False,
                    "timeSeries": True,
                }
            },
            "min": {
                "definition": {
                    "dataType": {"type": "DOUBLE"},
                    "isTimeSeries": False,
                    "isRequiredInEntity": True,
                    "isExternalId": False,
                    "isStoredExternally": False,
                    "isImported": False,
                    "isFinal": False,
                    "isInherited": True,
                    "imported": False,
                    "requiredInEntity": True,
                    "inherited": True,
                    "final": False,
                    "storedExternally": False,
                    "externalId": False,
                    "timeSeries": False,
                },
                "value": {"doubleValue": "50"},
            },
            "max": {
                "definition": {
                    "dataType": {"type": "DOUBLE"},
                    "isTimeSeries": False,
                    "isRequiredInEntity": True,
                    "isExternalId": False,
                    "isStoredExternally": False,
                    "isImported": False,
                    "isFinal": False,
                    "isInherited": True,
                    "imported": False,
                    "requiredInEntity": True,
                    "inherited": True,
                    "final": False,
                    "storedExternally": False,
                    "externalId": False,
                    "timeSeries": False,
                },
                "value": {"doubleValue": "150"},
            },
        },
        "entityId": "urn:ngsi-ld:Turbine:turbine_rect_1",
        "componentName": "TurbineFan",
        "maxResults": 100,
        "orderByTime": "ASCENDING",
    }


def test_lambda_handler(twinmaker_event):

    data = lambda_handler(twinmaker_event, "")

    # {
    #     "propertyValues": [
    #         {
    #         "entityPropertyReference": {
    #             "entityId": "urn:ngsi-ld:Turbine:turbine_rect_1",
    #             "componentName": "TurbineFan",
    #             "propertyName": "speed"
    #         },
    #         "values": [
    #             {
    #               "timestamp": 1646426606,
    #               "value": {
    #                   "stringValue": "NORMAL"
    #               }
    #             }
    #         ]
    #         }
    #     ],
    #     "nextToken": null
    #     }

    assert len(data["propertyValues"]) == 1
    value = data["propertyValues"][0]
    assert (
        value["entityPropertyReference"]["entityId"]
        == "urn:ngsi-ld:Turbine:turbine_rect_1"
    )
    assert value["entityPropertyReference"]["componentName"] == "TurbineFan"
    assert value["entityPropertyReference"]["propertyName"] == "speed"

    assert len(value["values"]) == 1
    val = value["values"][0]
    # The value is random but constant for the same input event
    assert float(val["value"]["doubleValue"]) == 53.0
