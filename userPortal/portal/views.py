#  from django.shortcuts import render
#  from models import *

from django.http import HttpResponse, StreamingHttpResponse
from django.views.generic import View

from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework import filters

from serializers import *
from filters import *

import pygraphviz


# Create your views here.

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    lookup_field = 'company_id'
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter)
    filter_class = CompanyFilterSet


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializerReadonly
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = ProjectFilterSet
    lookup_field = 'project_openstack_id'

    def create(self, request, *args, **kwargs):
        company_id = request.data.get('project_company_id', None)
        project_company = request.data.get('project_company', None)
        serializer = None

        if company_id is not None:
            request.data.pop('project_company_id')
            request.data['project_company'] = company_id
            serializer = ProjectSerializerWritableWithExistsCompany(data=request.data)
        elif project_company is not None:
            serializer = ProjectSerializerWritableWithNewCompany(data=request.data)

        if serializer is not None:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response('', status=status.HTTP_400_BAD_REQUEST)


class PortalUserViewSet(viewsets.ModelViewSet):
    queryset = PortalUser.objects.all()
    serializer_class = PortalUserSerializerReadonly
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = PortalUserFilter

    def create(self, request, *args, **kwargs):
        with transaction.atomic():
            serializer = PortalUserSerializerWritable(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WorkOrderViewSet(viewsets.ModelViewSet):
    queryset = WorkOrder.objects.all()


class WorkOrderDetailViewSet(viewsets.ModelViewSet):
    queryset = WorkOrderDetail.objects.all()


class ResourceViewSet(viewsets.ModelViewSet):
    queryset = ResourceOrder.objects.all()


class ResourceViewSet(viewsets.ModelViewSet):
    queryset = ResourceOrderDetail.objects.all()


class PortalView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'home.html')


class ImageView(View):

    def get(self, request, *args, **kwargs):
        A = pygraphviz.AGraph(directed=True, strict=True)
        A.add_edge(1, 2)
        A.add_edge(1, 3)
        A.add_node('a', style='invis')
        A.add_edge(1, 'a', style='invis')
        B = A.add_subgraph([2, 3, 'a'], rank='same')
        B.add_edge(2, 'a', style='invis')
        B.add_edge('a', 3, style='invis')

        A.add_edge(2, 4)
        A.add_edge(2, 5)
        A.add_node('b', style='invis')
        A.add_edge(2, 'b', style='invis')
        C = A.add_subgraph([4, 5, 'b'], rank='same')
        C.add_edge(4, 'b', style='invis')
        C.add_edge('b', 5, style='invis')

        A.add_edge(5, 6)
        A.add_edge(5, 7)
        A.add_node('c', style='invis')
        A.add_edge(5, 'c', style='invis')
        D = A.add_subgraph([6, 7, 'c'], rank='same')
        D.add_edge(6, 'c', style='invis')
        D.add_edge('c', 7, style='invis')

        A.add_edge(3, 8)
        A.add_edge(3, 9)
        A.add_node('d', style='invis')
        A.add_edge(3, 'd', style='invis')
        E = A.add_subgraph([8, 9, 'd'], rank='same')
        E.add_edge(8, 'd', style='invis')
        E.add_edge('d', 9, style='invis')

        A.add_edge(8, 10)
        A.add_edge(8, 11)
        A.add_node('e', style='invis')
        A.add_edge(8, 'e', style='invis')
        F = A.add_subgraph([10, 11, 'e'], rank='same')
        F.add_edge(10, 'e', style='invis')
        F.add_edge('e', 11, style='invis')

        A.graph_attr['epsilon'] = '0.001'
        print A.string()  # print dot file to standard output
        A.write('foo.dot')
        A.layout('dot')  # layout with dot
        A.draw('foo.svg')

        def file_iterator(file_name, chunk_size=512):
            with open(file_name) as f:
                while True:
                    c = f.read(chunk_size)
                    if c:
                        yield c
                    else:
                        break

        response = StreamingHttpResponse(file_iterator('foo.svg'), content_type='image/svg+xml')
        return response
