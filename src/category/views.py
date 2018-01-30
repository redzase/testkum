from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.exceptions import APIException

from src.helper.response import response
from src.category.models import Category, Tag
from src.category.serializers import CategoryListSerializers, CategorySerializers


class CategoryList(APIView):
    message = 'data not found'
    meta = None

    def get(self, request, format=None):
        try:
            page = int(request.GET.get('page', 1))
            per_page = int(request.GET.get('per_page', 10))
            search = request.GET.get('search', '')
            filter_by = request.GET.get('filter_by', '').lower()
            sort_by = request.GET.get('sort_by', 'id')
            sort_order = request.GET.get('sort_dir', 'asc')
            status = request.GET.get('status', '')
            sorting = ''

            if sort_order == 'asc':
                sorting = sort_by
            elif sort_order == 'desc':
                sorting = '-' + sort_by

            if filter_by == 'status':
                all_data = Category.objects.filter(Q(status=search)).order_by(sorting)
            elif filter_by == 'tag':
                all_data = Category.objects.filter(pk__in=Tag.objects.filter(name__icontains=search).values('category_id')).order_by(sorting)
            else:
                all_data = Category.objects.filter(Q(name__icontains=search)).order_by(sorting)

            if status != '':
                all_data = all_data.filter(status=status)

            paginator = Paginator(all_data, per_page)
            serialized = CategoryListSerializers(paginator.page(page), many=True)
            meta = {
                'total': paginator.count,
                'per_page': per_page,
                'current_page': page,
                'last_page': paginator.num_pages,
            }
            data = serialized.data
            if data:
                message = 'get Category list'
                status = True
                return response(200, data, message, status, meta)

            return response(200, message=self.message)
        except Exception as e:
            return response(400, message=str(e))

    def post(self, request, format=None):
        serialized = CategorySerializers(data=request.data)
        if serialized.is_valid():
            serialized.save()
            message = 'create Category'
            status = True
            return response(200, serialized.data, message, status)
        else:
            return response(400, serialized.errors)

class CategoryDetail(APIView):
    message = 'data not found'
    meta = None

    def get(self, request, id, format=None):
        try:
            try:
                detail_data = Category.objects.get(pk=id)
            except Category.DoesNotExist:
                detail_data = None
                return response(404, message="Category doesn't exist")

            serialized = CategorySerializers(detail_data)
            if serialized.data:
                message = 'Category detail'
                status = True
                return response(200, serialized.data, message, status, self.meta)

            return response(200, message=self.message)
        except Exception as e:
            return response(400, message=str(e))

    def put(self, request, id, format=None):
        category = get_object_or_404(Category, pk=id)
        serialized = CategorySerializers(category, data=request.data)
        if serialized.is_valid():
            serialized.save()
            message = 'update Category'
            status = True
            return response(200, serialized.data, message, status)

        return response(400, serialized.errors, message="failed to update data")

    def delete(self, request, id, format=None):
        category = get_object_or_404(Category, pk=id)
        try:
            data = CategorySerializers(category).data
            category.delete()
            message = 'delete Category'
            status = True
            return response(200, data, message, status)
        except Exception as e:
            return response(400, message="failed to delete data")
