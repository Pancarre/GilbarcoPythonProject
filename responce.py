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

    # Add to the dictionary the value of 'id' only if it's not null.
    if id is not None:
        answer_dict["answer"]["fields"]["new-test-id"] = id

    # When there has been an error, that is, when there is an error message.
    if error_message is not None:
        answer_dict["answer"]["fields"]["error-message"] = error_message

    return answer_dict
