SCHEMA = {
    "$schema": "http://json-schema.org/schema#",
    "type": "object",
    "description": "a schema for major requirements data",
    "properties": {
        "major": {"type": "string"},
        "requirements": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "sub_reqs": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "req_num": {
                                    "type": "integer",
                                    "minimum": 1
                                },
                                "req_list": {
                                    "type": "array",
                                    "items": {"type": "string"}
                                }
                            },
                            "required": ["req_num", "req_list"]
                        }
                    }
                },
                "required": ["name", "sub_reqs"]
            }
        },
        "specs": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "sub_reqs": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "req_num": {
                                    "type": "integer",
                                    "minimum": 1
                                },
                                "req_list": {
                                    "type": "array",
                                    "items": {"type": "string"}
                                }
                            },
                            "required": ["req_num", "req_list"]
                        }
                    }
                },
                "required": ["name", "sub_reqs"]
            }
        }
    },
    "required": ["major", "requirements"]
}
