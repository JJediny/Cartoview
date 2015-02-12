# coding=utf-8

import json
import pickle
from django.http import HttpResponse, HttpResponseForbidden
from django.db.models.loading import get_model


def tree_widget(request, application, model_name):
    data = []

    if not request.is_ajax():
        return HttpResponseForbidden(u'no ajax')

    objects = get_model(application, model_name).objects

    node_id = request.GET['node_id']
    if node_id:
        objects = objects.filter(parent_id=node_id)
    else:
        objects = objects.filter(parent_id__isnull=True)

    for node in objects.iterator():
        title = unicode(node)
        data.append({"data": title, "attr": {"id": node.id, "title": title},
                     "state": "closed" if node.children.exists() else ""})

    return HttpResponse(json.dumps(data), content_type="application/json")


def autocomplete_widget(request, application, model_name):

    # if not request.is_ajax():
    #     return HttpResponseForbidden(u'no ajax')

    data = []
    expression = request.GET.get('expression')
    
    token = request.GET.get('q')
    if expression == u'pk__in':
        token = token.split(",")

    objects = get_model(application, model_name).objects
    
    where = request.GET.get('where')
    if where:
        where_params = request.GET.get('where_params')
        where_params = pickle.loads(where_params)
        objects = objects.extra(where=[where], params=where_params)

    objects = objects.filter(**{expression: token})[:20]
    
    for item in objects.iterator():
        data.append({"id": item.id, "text": unicode(item)})

    return HttpResponse(json.dumps(data), content_type="application/json;charset=utf-8")
