def to_jason(name, id, version_protocol, ack , error_message):

    answer_dict = {
        "answer": {
            "protocol-version": "00.01",
            "name": "update-test-in-progress",
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


