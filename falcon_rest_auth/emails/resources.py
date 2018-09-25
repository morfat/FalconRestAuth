
import falcon

from .models import EmailProvider,EmailTemplate
from .serializers import EmailProviderSerializer,EmailTemplateSerializer

from falchemy_rest.resources import ListCreateResource ,RetrieveUpdateResource

class ListCreateEmailProviders(ListCreateResource):

    model = EmailProvider

    filterable_fields = ('activated',)
    searchable_fields = ('name',)

    serializer_class = EmailProviderSerializer


class RetrieveUpdateEmailProvider(RetrieveUpdateResource):
   
    model = EmailProvider

    serializer_class = EmailProviderSerializer



class ListCreateEmailTemplates(ListCreateResource):

   
    model = EmailTemplate

    filterable_fields = ('activated',)
    searchable_fields = ('name',)

    serializer_class = EmailTemplateSerializer


class RetrieveUpdateEmailTemplate(RetrieveUpdateResource):
 
    model = EmailTemplate

    serializer_class = EmailTemplateSerializer

    


    
   

        



