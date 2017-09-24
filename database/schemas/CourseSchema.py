SCHEMA = {
    "$schema": "http://json-schema.org/schema#",
    "type": "object",
    "description": "a schema for a course data",
    "properties": {

        "cid": {
            "type": "string",
        },
        "dept": {
            "type": "string"
        },
        "name": {
            "type": "string"
        },
        "prereqs": {
            "type": "array",
            "items": {
                "type": "array",
                "items": {
                    "type": "string"
                }
            }
        },
        "quarters": {
            "type": "array",
            "items": {
                "type": "integer",
                "minimum": 0
            }
        },
        "units": {
            "type": "number",
            "minimum": 0
        },
        "upperOnly": {
            "type": "boolean"
        }
    },
    "required": ["cid", "dept", "name", "prereqs", "units", "upperOnly"]

}
