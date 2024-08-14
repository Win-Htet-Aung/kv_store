import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .services import create_items, filter_items, update_items


@csrf_exempt
def item_view(request) -> HttpResponse:
    if request.method == "GET":
        keys = request.GET.get("keys")
        response_data = filter_items(keys)
        if not response_data:
            response_data["message"] = "No items found!"
            return HttpResponse(
                content=json.dumps(response_data),
                content_type="application/json",
                status=404,
            )
        return HttpResponse(
            content=json.dumps(response_data),
            content_type="application/json",
            status=200,
        )
    elif request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        if not data:
            return HttpResponse(
                content=json.dumps({"message": "Empty body!"}),
                content_type="application/json",
                status=400,
            )
        response_data = create_items(data)
        return HttpResponse(
            content=json.dumps(response_data),
            content_type="application/json",
            status=201,
        )
    elif request.method == "PATCH":
        data = json.loads(request.body.decode("utf-8"))
        if not data:
            return HttpResponse(
                content=json.dumps({"message": "Empty body!"}),
                content_type="application/json",
                status=400,
            )
        response_data = update_items(data)
        return HttpResponse(
            content=json.dumps(response_data),
            content_type="application/json",
            status=200,
        )
