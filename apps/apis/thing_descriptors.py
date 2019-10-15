PID = ['smart_hotel_dummy_iot_service']


HOTEL_INFO = {
    "pid": "hotel_info",
    "monitors": "adapters:Start",
    "write_link": {
        "href": "/reservations/property/{pid}",
        "input": {
            "type": "object",
            "field": [
                {
                    "name": "name",
                    "schema": {
                        "type": "string"
                    }
                }
            ]
        },
        "output": {
            "type": "object",
            "field": [
                {
                    "name": "name",
                    "schema": {
                        "type": "string"
                    }
                },
                {
                    "name": "address",
                    "schema": {
                        "type": "string"
                    }
                },
                {
                    "name": "state",
                    "schema": {
                        "type": "double"
                    }
                },
                {
                    "name": "city",
                    "schema": {
                        "type": "double"
                    }
                }
            ]
        }
    }
}


SMART_GARAGE_EID = "reservations"

RESERVE_PARKING_EVENT = {
    "eid": SMART_GARAGE_EID,
    "monitors": "adapters:Start",
    "output": {
        "type": "object",
        "field": [
            {
                "name": "payment_id",
                "schema": {
                    "type": "string"
                }
            },
            {
                "name": "payment_address",
                "schema": {
                    "type": "string"
                }
            },
            {
                "name": "status",
                "schema": {
                    "type": "string"
                }
            }
        ]}
}
