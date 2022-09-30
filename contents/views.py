from turtle import title
from types import NoneType
from rest_framework.views import APIView, Request, Response, status
from .models import Content
from django.forms.models import model_to_dict

class ContentView(APIView):
    valid_keys = ["title", "module", "students", "description", "is_active"]
    valid_keys_type = {
    "title": str,
    "module": str,
    "description": str,
    "students": int,
    "is_active": bool
}
    err = {}
    type_err = {}

    def get(self, request: Request) -> Response:
        contents = Content.objects.all()
        content_list = [model_to_dict(content) for content in contents]
        return Response(content_list, status.HTTP_200_OK)
    
    def post(self, request: Request) -> Response:
        self.clean_data(dict(**request.data))
        self.is_valid(dict(**request.data))

        if len(self.err) > 0:
            return Response(self.err, status.HTTP_400_BAD_REQUEST)
        
        self.is_valid_type(dict(**request.data))

        if len(self.type_err) > 0:
            return Response(self.type_err, status.HTTP_400_BAD_REQUEST)

        content = Content.objects.create(**request.data)
        new_content = model_to_dict(content)

        return Response(new_content, status.HTTP_201_CREATED)
    

    def is_valid(self, data: dict) -> None:
        for valid_key in self.valid_keys:
            if valid_key not in data.keys():
                self.err.update({valid_key: 'Missing'})


    def is_valid_type(self, data: dict) -> None:
        for key, value in data.items():
            if type(value) != self.valid_keys_type[key]:
                self.type_err.update({key: f'Must be a {self.valid_keys_type[key]}'})


    def clean_data(self, data: dict) -> None:
        data_keys = list(data.keys())
        for key_name in data_keys:
            if key_name not in self.valid_keys:
                data.pop(key_name)


class OneContentView(APIView):
    def get(self, request: Request, content_id: int) -> Response:

        try:
            content = Content.objects.get(id = content_id)
        except Content.DoesNotExist:
            return Response({'message': 'Content not found'}, status.HTTP_404_NOT_FOUND)

        contents = model_to_dict(content)
        return Response(contents, status.HTTP_200_OK)

    def patch(self, request: Request, content_id: int) -> Response:
        try:
            content = Content.objects.get(id = content_id)
        except Content.DoesNotExist:
            return Response({'message': 'Content not found'}, status.HTTP_404_NOT_FOUND)

        for key, value in request.data.items():
            setattr(content, key, value)
        
        content.save()

        response = model_to_dict(content)

        return Response(response, status.HTTP_200_OK)


    def delete(self, request: Request, content_id: int) -> Response:
        try:
            content = Content.objects.get(id = content_id)
        except Content.DoesNotExist:
            return Response({'message': 'Content not found'}, status.HTTP_404_NOT_FOUND)

        for key, value in request.data.items():
            setattr(content, key, value)
        
        content.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

class FilterContentView(APIView):
    def get(self, request: Request) -> Response:
        filter = request.query_params.get('title')
        contents = Content.objects.filter(title__icontains = filter).all()
        contents_founded = [
            model_to_dict(content) for content in contents
            ]
        if len(contents_founded) == 0:
            return Response({'message': "Can't find any content with this word or letters"}, status.HTTP_404_NOT_FOUND)
        return Response(contents_founded, status.HTTP_200_OK)