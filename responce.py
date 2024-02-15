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

    #aggiungere al dizionario valore id solo se non è null
    if id is not None:
        answer_dict["answer"]["fields"]["new-test-id"] = id

    #quando c'è stato un errore cioè è presente un messaggio di errore
    if error_message is not None:
        answer_dict["answer"]["fields"]["error-message"] = error_message

    return answer_dict
