def to_json(name, id, version_protocol, ack , error_message):

    answer_dict = {
        "answer": {
            "protocol-version": version_protocol,
            "name": name,
            "fields": {
                "acknowledge": ack,

            }
        }
    }

    if id is not None:
        answer_dict["answer"]["fields"]["new-test-id"] = id

    if error_message is not None:
        answer_dict["answer"]["fields"]["error-message"] = error_message

    return answer_dict
