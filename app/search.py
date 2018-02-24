# Elasticsearch Abstraction:
# The idea is to keep all the Elasticsearch code in this module. The rest of the application will use the functions in this new module to access the index and will not have direct access to Elasticsearch. 
# If one day I decided I don’t like Elasticsearch anymore and want to switch to a different engine, all I need to do is rewrite the functions in this module (assuming the new model uses indexes...), and the application will continue to work as before.

# Only database Models will be included!! Plus, to include a field from the model, this should be included in the model's variable '__searchable__', as well as setting the model as derived class of 'SearchableMixin'.

# TODO Ventura: variable index may not be needed, as we can take the index based on the name of the model (under '__tablename__').

from flask import current_app


def add_to_index(index, model):
    if not current_app.elasticsearch:
        return
    payload = {}
    for field in model.__searchable__:
        payload[field] = getattr(model, field)
    current_app.elasticsearch.index(index=index,
                                    doc_type=index,
                                    id=model.id,
                                    body=payload)


def remove_from_index(index, model):
    if not current_app.elasticsearch:
        return
    current_app.elasticsearch.delete(index=index,
                                     doc_type=index,
                                     id=model.id)


def query_index(index, query, page, per_page):
    if not current_app.elasticsearch:
        return [], 0
    search = current_app.elasticsearch.search(
        index=index,
        doc_type=index,
        body={'query': {'multi_match': {'query': query, 'fields': ['*']}}, 
              'from': (page - 1) * per_page, 'size': per_page})
    ids = [int(hit['_id']) for hit in search['hits']['hits']]
    return ids, search['hits']['total']  # list of result ids, number of results