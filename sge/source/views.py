# -*- coding: utf-8 -*-

import json

from django import http
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views.generic import TemplateView, CreateView, UpdateView, ListView
from django.views.generic.detail import BaseDetailView
from django.views.generic.list import BaseListView
from django.forms.models import model_to_dict, inlineformset_factory

from sge.source.choices import MENU_PRINCIPAL, STATUS_ATIVO, STATUS_ENTREGA
from sge.source.models import *
from sge.source.forms import *

class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)

class JSONResponseMixin(object):
    """
    Classe 'mixin' baseada no exemplo em:
    https://docs.djangoproject.com/en/dev/topics/class-based-views/
    """
    def render_to_response(self, context):
        "Returns a JSON response containing 'context' as payload"
        return self.get_json_response(self.convert_context_to_json(context))

    def get_json_response(self, content, **httpresponse_kwargs):
        "Construct an 'HttpResponse' object."
        return http.HttpResponse(content,
                                 content_type='application/json',
                                 **httpresponse_kwargs)

    def convert_context_to_json(self, context):
        "Convert the context dictionary into a JSON object"
        return json.dumps(context)

class SgeView(LoginRequiredMixin):
    def get_context_data(self, *args, **kwargs):
        context = super(SgeView, self).get_context_data(*args, **kwargs)
        context['menu'] = MENU_PRINCIPAL
        return context

class CidadeListView(JSONResponseMixin, BaseListView):
    def get_queryset(self):
        queryset = Cidade.objects.all()
        if 'uf' in self.request.GET:
            uf = self.request.GET['uf']
            queryset = queryset.filter(uf=uf)
        return [model_to_dict(cidade) for cidade in queryset]

class ClienteDetailView(JSONResponseMixin, BaseDetailView):
    def get_object(self):
        cliente = Cliente.objects.get(pk=self.request.GET['pk'])
        return {'valor_maximo_entrega': u'%.02f' % float(cliente.valor_maximo_entrega)}

class EntregadorClienteListView(JSONResponseMixin, BaseListView):
    def get_queryset(self):
        entregador_id = int(self.request.GET['pk'])
        entregador = Entregador.objects.get(pk=entregador_id)
        clientes = [ec.cliente for ec in entregador.entregadorcliente_set.order_by('cliente__razao_social').all()]
        return [{'id': cliente.pk, 'nome': cliente.razao_social} for cliente in clientes if cliente.status]

class EntregadorClienteDetailView(JSONResponseMixin, BaseDetailView):
    def get_object(self):
        cliente_id = int(self.request.GET['cliente_id'])
        entregador_id = int(self.request.GET['pk'])
        entregador_cliente = EntregadorCliente.objects.get(cliente=cliente_id, entregador=entregador_id)
        if entregador_cliente:
            return {'valor_entrega': u'%.02f' % float(entregador_cliente.valor)}
        else:
            return None

class PainelControleView(SgeView, TemplateView):
    template_name = 'source/painel_controle.html'

    def get_context_data(self, *args, **kwargs):
        context = super(PainelControleView, self).get_context_data(*args, **kwargs)
        context['locomocoes_pendentes'] = Locomocao.objects.filter(situacao_comprovante = 'comp_pendente').count()
        context['entregas_pendentes'] = Entrega.objects.filter(status = 'enviada').count()
        context['transferencias_pendentes'] = Transferencia.objects.filter(status = 'enviada').count()
        return context

class PerfilEditarView(SgeView, UpdateView):
    model = User
    form_class = UserForm
    template_name = 'source/usuario_alteracao.html'

    def get_success_url(self):
        return reverse('source_painel_controle')

    def post(self, request, *args, **kwargs):
        r = super(PerfilEditarView, self).post(request, *args, **kwargs)
        if isinstance(r, http.HttpResponseRedirect):
            messages.success(request, _(u"Perfil atualizado com sucesso!"), fail_silently=True)
        return r

class ClienteInclusaoView(SgeView, CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'source/cliente_inclusao.html'

    def get_success_url(self):
        return reverse('source_cliente_inclusao')

    def get_context_data(self, *args, **kwargs):
        context = super(ClienteInclusaoView, self).get_context_data(*args, **kwargs)
        if self.request.POST:
            context['clienteproduto_formset'] = ClienteProdutoFormSet(self.request.POST)
        else:
            context['clienteproduto_formset'] = ClienteProdutoFormSet()
        return context

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        context = self.get_context_data()
        clienteproduto_formset = context['clienteproduto_formset']

        if clienteproduto_formset.is_valid():
            self.object = form.save()
            clienteproduto_formset.instance = self.object
            clienteproduto_formset.save()
            messages.success(self.request, _(u"Cliente cadastrado com sucesso!"), fail_silently=True)
            return http.HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

class ClienteConsultaView(SgeView, ListView):
    model = Cliente
    context_object_name = 'clientes'
    template_name = 'source/cliente_consulta.html'

class ClienteAlteracaoView(SgeView, UpdateView):
    model = Cliente
    form_class = ClienteForm
    context_object_name = 'cliente'
    template_name = 'source/cliente_alteracao.html'

    def get_success_url(self):
       return reverse('source_cliente_consulta')

    def get_context_data(self, *args, **kwargs):
        context = super(ClienteAlteracaoView, self).get_context_data(*args, **kwargs)
        if self.request.POST:
            context['clienteproduto_formset'] = ClienteProdutoFormSet(self.request.POST, instance=self.object, queryset=self.object.produto_set.order_by('descricao'))
        else:
            context['clienteproduto_formset'] = ClienteProdutoFormSet(instance=self.object, queryset=self.object.produto_set.order_by('descricao'))
        return context

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        context = self.get_context_data()
        clienteproduto_formset = context['clienteproduto_formset']

        if clienteproduto_formset.is_valid():
            self.object = form.save()
            clienteproduto_formset.save()
            messages.success(self.request, _(u"Cliente alterado com sucesso!"), fail_silently=True)
            return http.HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

class ClienteStatusChangeView(SgeView, UpdateView):
    model = Cliente

    def get_success_url(self):
        return reverse('source_cliente_consulta')

    def get(self, request, *args, **kwargs):
        r = super(ClienteStatusChangeView, self).get(request, *args, **kwargs)

        print(kwargs['status'])

        self.object.status = kwargs['status']
        self.object.save()

        if self.object.status:
            messages.success(request, _(u"Cliente reativado com sucesso!"), fail_silently=True)
        else:
            messages.success(request, _(u"Cliente desativado com sucesso!"), fail_silently=True)

        return http.HttpResponseRedirect(self.get_success_url())

class EntregadorInclusaoView(SgeView, CreateView):
    model = Entregador
    form_class = EntregadorForm
    template_name = 'source/entregador_inclusao.html'

    def get_success_url(self):
        return reverse('source_entregador_inclusao')

    def get_context_data(self, *args, **kwargs):
        context = super(EntregadorInclusaoView, self).get_context_data(*args, **kwargs)
        if self.request.POST:
           context['entregadorcliente_formset'] = EntregadorClienteFormSet(self.request.POST)
        else:
            context['entregadorcliente_formset'] = EntregadorClienteFormSet()
        return context

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        context = self.get_context_data()
        entregadorcliente_formset = context['entregadorcliente_formset']

        if entregadorcliente_formset.is_valid():
            self.object = form.save()
            entregadorcliente_formset.instance = self.object
            entregadorcliente_formset.save()
            messages.success(self.request, _(u"Entregador cadastrado com sucesso!"), fail_silently=True)
            return http.HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

class EntregadorConsultaView(SgeView, ListView):
    model = Entregador
    context_object_name = 'entregadores'
    template_name = 'source/entregador_consulta.html'

class EntregadorAlteracaoView(SgeView, UpdateView):
    model = Entregador
    form_class = EntregadorForm
    context_object_name = 'entregador'
    template_name = 'source/entregador_alteracao.html'

    def get_success_url(self):
        return reverse('source_entregador_consulta')

    def get_context_data(self, *args, **kwargs):
        context = super(EntregadorAlteracaoView, self).get_context_data(*args, **kwargs)
        if self.request.POST:
            context['entregadorcliente_formset'] = EntregadorClienteFormSet(self.request.POST, instance=self.object)
        else:
            context['entregadorcliente_formset'] = EntregadorClienteFormSet(instance=self.object)
        return context

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        context = self.get_context_data()
        entregadorcliente_formset = context['entregadorcliente_formset']

        if entregadorcliente_formset.is_valid():
            form.save()
            entregadorcliente_formset.save()
            messages.success(self.request, _(u"Entregador alterado com sucesso!"), fail_silently=True)
            return http.HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

class EntregadorStatusChangeView(SgeView, UpdateView):
    model = Entregador

    def get_success_url(self):
        return reverse('source_entregador_consulta')

    def get(self, request, *args, **kwargs):
        r = super(EntregadorStatusChangeView, self).get(request, *args, **kwargs)

        self.object.status = kwargs['status']
        self.object.save()

        if self.object.status:
            messages.success(request, _(u"Entregador reativado com sucesso!"), fail_silently=True)
        else:
            messages.success(request, _(u"Entregador desativado com sucesso!"), fail_silently=True)

        return http.HttpResponseRedirect(self.get_success_url())

class LocomocaoInclusaoView(SgeView, CreateView):
    form_class = LocomocaoForm
    template_name = 'source/locomocao_inclusao.html'

    def get_success_url(self):
        return reverse('source_locomocao_inclusao')

    def get_context_data(self, *args, **kwargs):
        context = super(LocomocaoInclusaoView, self).get_context_data(*args, **kwargs)
        return context

    def post(self, request, *args, **kwargs):
        r = super(LocomocaoInclusaoView, self).post(request, *args, **kwargs)
        if isinstance(r, http.HttpResponseRedirect):
            messages.success(request, _(u"Locomoção cadastrada com sucesso!"), fail_silently=True)
        return r

class LocomocaoConsultaView(SgeView, ListView):
    model = Locomocao
    context_object_name = 'locomocoes_pendentes'
    template_name = 'source/locomocao_consulta.html'

    def get_queryset(self):
        return Locomocao.objects.filter(situacao_comprovante = 'comp_pendente').order_by('entregador__nome')

class LocomocaoPendenteView(SgeView, UpdateView):
    model = Locomocao

    def get_success_url(self):
        return reverse('source_locomocao_consulta')

    def get(self, request, *args, **kwargs):
        r = super(LocomocaoPendenteView, self).get(request, *args, **kwargs)
        self.object.situacao_comprovante = 'comp_nao_entregue'
        self.object.save()
        messages.success(request, _(u"Locomoção atualizada com sucesso!"), fail_silently=True)
        return http.HttpResponseRedirect(self.get_success_url())

class LocomocaoAlteracaoView(SgeView, UpdateView):
    model = Locomocao
    form_class = LocomocaoForm
    context_object_name = 'locomocao'
    template_name = 'source/locomocao_alteracao.html'

    def get_success_url(self):
        return reverse('source_locomocao_consulta')

    def post(self, request, *args, **kwargs):
        r = super(LocomocaoAlteracaoView, self).post(request, *args, **kwargs)
        if isinstance(r, http.HttpResponseRedirect):
            messages.success(request, _(u"Locomoção atualizada com sucesso!"), fail_silently=True)
        return r

class EntregaInclusaoView(SgeView, CreateView):
    model = Entrega
    form_class = EntregaForm
    template_name = 'source/entrega_inclusao.html'

    def get_success_url(self):
        return reverse('source_entrega_inclusao')

    def get_context_data(self, *args, **kwargs):
        context = super(EntregaInclusaoView, self).get_context_data(*args, **kwargs)
        if self.request.POST:
            context['entregacliente_formset'] = EntregaClienteFormSet(self.request.POST)
        else:
            context['entregacliente_formset'] = EntregaClienteFormSet()
        return context

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        context = self.get_context_data()
        entregacliente_formset = context['entregacliente_formset']

        if entregacliente_formset.is_valid():
            self.object = form.save()
            entregacliente_formset.instance = self.object
            entregacliente_formset.save()
            messages.success(self.request, _(u"Entrega cadastrado com sucesso!"), fail_silently=True)
            return http.HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

class EntregaConsultaView(SgeView, ListView):
    model = Entrega
    context_object_name = 'entregas'
    template_name = 'source/entrega_consulta.html'

    def get_queryset(self):
        return Entrega.objects.filter(status=u'enviada').order_by('saida_data')

    def get_context_data(self, *args, **kwargs):
        context = super(EntregaConsultaView, self).get_context_data(*args, **kwargs)
        entrega = Entrega.objects.filter(status=u'enviada').order_by('saida_data').all()
        return context

class EntregaCancelamentoView(SgeView, UpdateView):
    model = Entrega

    def get_success_url(self):
        return reverse('source_entrega_consulta')

    def get(self, request, *args, **kwargs):
        r = super(EntregaCancelamentoView, self).get(request, *args, **kwargs)
        self.object.status = u'cancelada'
        self.object.save()
        messages.success(request, _(u"Entrega cancelada com sucesso!"), fail_silently=True)
        return http.HttpResponseRedirect(self.get_success_url())

class EntregaAlteracaoView(SgeView, UpdateView):
    model = Entrega
    form_class = EntregaFormConsulta
    context_object_name = 'entrega'
    template_name = 'source/entrega_alteracao.html'

    def get_success_url(self):
        return reverse('source_entrega_consulta')

    def get_context_data(self, *args, **kwargs):
        context = super(EntregaAlteracaoView, self).get_context_data(*args, **kwargs)
        if self.request.POST:
            context['entregacliente_formset'] = EntregaClienteFormSetConsulta(self.request.POST, instance=self.object)
        else:
            context['entregacliente_formset'] = EntregaClienteFormSetConsulta(instance=self.object)
        return context

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        context = self.get_context_data()
        entregacliente_formset = context['entregacliente_formset']

        if entregacliente_formset.is_valid():
            self.object = form.save()
            entregacliente_formset.save()
            messages.success(self.request, _(u"Entrega alterada com sucesso!"), fail_silently=True)
            return http.HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

class TransferenciaInclusaoView(SgeView, CreateView):
    model = Transferencia
    form_class = TransferenciaForm
    template_name = 'source/transferencia_inclusao.html'

    def get_success_url(self):
        return reverse('source_transferencia_inclusao')

    def get_context_data(self, *args, **kwargs):
        context = super(TransferenciaInclusaoView, self).get_context_data(*args, **kwargs)
        if self.request.POST:
            context['transferenciacliente_formset'] = TransferenciaClienteFormSet(self.request.POST)
        else:
            context['transferenciacliente_formset'] = TransferenciaClienteFormSet()
        return context

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        context = self.get_context_data()
        transferenciacliente_formset = context['transferenciacliente_formset']

        if transferenciacliente_formset.is_valid():
            self.object = form.save()
            transferenciacliente_formset.instance = self.object
            transferenciacliente_formset.save()
            messages.success(self.request, _(u"Transferência cadastrada com sucesso!"), fail_silently=True)
            return http.HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

class TransferenciaConsultaView(SgeView, ListView):
    model = Transferencia
    context_object_name = 'transferencias'
    template_name = 'source/transferencia_consulta.html'

    def get_queryset(self):
        return Transferencia.objects.filter(status=u'enviada').order_by('saida_data')

class TransferenciaAlteracaoView(SgeView, UpdateView):
    model = Transferencia
    form_class = TransferenciaFormConsulta
    context_object_name = 'transferencia'
    template_name = 'source/transferencia_alteracao.html'

    def get_success_url(self):
        return reverse('source_transferencia_consulta')

    def get_context_data(self, *args, **kwargs):
        context = super(TransferenciaAlteracaoView, self).get_context_data(*args, **kwargs)
        TransferenciaClienteFormSet = inlineformset_factory(Transferencia, TransferenciaCliente, form=TransferenciaClienteFormConsulta, extra=0, can_delete=False)
        if self.request.POST:
            context['transferenciacliente_formset'] = TransferenciaClienteFormSetConsulta(self.request.POST, instance=self.object)
        else:
            context['transferenciacliente_formset'] = TransferenciaClienteFormSetConsulta(instance=self.object)
        return context

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        context = self.get_context_data()
        transferenciacliente_formset = context['transferenciacliente_formset']

        if transferenciacliente_formset.is_valid():
            self.object = form.save()
            transferenciacliente_formset.save()
            messages.success(self.request, _(u"Transferência alterada com sucesso!"), fail_silently=True)
            return http.HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

class TransferenciaCancelamentoView(SgeView, UpdateView):
    model = Transferencia

    def get_success_url(self):
        return reverse('source_transferencia_consulta')

    def get(self, request, *args, **kwargs):
        r = super(TransferenciaCancelamentoView, self).get(request, *args, **kwargs)
        self.object.status = u'cancelada'
        self.object.save()
        messages.success(request, _(u"Transferência cancelada com sucesso!"), fail_silently=True)
        return http.HttpResponseRedirect(self.get_success_url())


