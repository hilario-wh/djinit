import os
import uuid

from django.core.validators import RegexValidator
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField

# Create your models here.
from django.contrib.auth.models import AbstractUser
phone_regex = RegexValidator(regex=r'^\d+$', message=_('Ingrese solo números.'))

# Create your models here.
class User(AbstractUser):
    ADMIN = 'Admin'
    TECNICO = 'Tecnico'
    SOPORTE = 'Soporte'
    VENTAS = 'Ventas'
    CLIENTE = 'Cliente'
    PROSPECTO = 'Prospecto'
    TYPE = (
        (ADMIN, _('Administrador')),
        (TECNICO, _('Técnico')),
        (SOPORTE, _('Soporte')),
        (VENTAS, _('Ventas')),
        (CLIENTE, _('Cliente')),
        (PROSPECTO, _('Prospecto')),
    )

    MORAL = 'Moral/Juridica'
    FISICA = 'Fisica/Natural'
    TIPO_PERSONA = (
        (FISICA, _('Fisica/Natural')),
        (MORAL, _('Moral/Juridica'))
    )

    def avatar_path(self, filename):
        extension = os.path.splitext(filename)[1][1:]
        file_name = os.path.splitext(filename)[0]
        url = "usuarios/{}/avatar/{}.{}".format(
            self.legal_name, slugify(str(file_name)), extension
        )
        return url

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, db_index=True, unique=True)
    avatar = models.ImageField(upload_to='usuarios/%Y/%m/', default='usuarios/avatar.png')

    address = models.TextField(_("Dirección"), blank=True)
    phone_number = models.CharField(_("Teléfono Celular"), max_length=250, blank=True,
                                    validators=[phone_regex])
    rfc = models.CharField('RFC/RUC/NIT', max_length=30, blank=True)
    legal_name = models.CharField(_('Nombre facturación'), max_length=255, blank=True)
    tax_id = models.CharField('RFC/RUC', max_length=30, blank=True)
    tax_system = models.CharField(_('Regimen fiscal'), max_length=10, blank=True, null=True)
    postal_code = models.CharField(_('Código postal'), max_length=50, blank=True)
    billing_address = models.TextField(_('Dirección de facturación'), max_length=100, blank=True)
    billing_email = models.EmailField(_('Email de facturación'), blank=True)
    district = models.CharField(_('Localidad/Barrio/Departamento'), max_length=50, blank=True)
    city = models.CharField(_('Ciudad/Municipio'), max_length=50, blank=True)
    license = models.CharField(_('Licencia DNI/C.I./C.C.'), max_length=35, blank=True)

    # relations
    user_type = models.ForeignKey('users.TipoUsuario', verbose_name=_('Tipo de usuario'), null=True,
                                  related_name='user_type_user', on_delete=models.SET_NULL)
    person_type = models.ForeignKey('users.TipoPersona', verbose_name=_('Tipo de persona'), blank=True, null=True,
                                    related_name='person_type_user', on_delete=models.SET_NULL)

    status = models.ForeignKey("users.ClientStatus", related_name="client_status", verbose_name=_("Estatus"),
                               on_delete=models.SET_NULL, null=True, blank=True)

    company = models.ForeignKey('Empresa', verbose_name=_('Empresa'), null=True, related_name='company_user',
                                on_delete=models.CASCADE)

    def __str__(self):
        return self.username + '-' + self.get_full_name()

    class Meta:
        ordering = ('-id',)


class TipoUsuario(models.Model):
    name = models.CharField(_('Nombre'), max_length=20)

    def __str__(self):
        return self.name


class TipoPersona(models.Model):
    name = models.CharField(_('Nombre'), max_length=20)

    def __str__(self):
        return self.name


class ClientStatus(models.Model):
    name = models.CharField(max_length=70, verbose_name=_('Nombre'))
    class_css = models.CharField(max_length=40, verbose_name=_("Class ccs color"))
    created = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        ordering = ('-created',)
        verbose_name = _("Estado Clientes")
        verbose_name_plural = _("Estado Clientes")

    def __str__(self):
        return self.name


class Empresa(models.Model):

    def logo_path(self, filename):
        extension = os.path.splitext(filename)[1][1:]
        file_name = os.path.splitext(filename)[0]
        url = "empresas/{}/logo/{}.{}".format(
            self.nombre, slugify(str(file_name)), extension
        )
        return url

    ACTIVO = 1
    SUSPENDIDO = 2
    CANCELADO = 3
    ESTADO_EMPRESA = (
        (ACTIVO, 'Activo'),
        (SUSPENDIDO, 'Suspendido'),
        (CANCELADO, 'Cancelado'),
    )
    uuid = models.UUIDField(verbose_name=_('Identificador de empresa'), editable=False, default=uuid.uuid4,
                            db_index=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Registro')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Última Actualización')

    nombre = models.CharField(max_length=80, unique=True)
    email = models.EmailField(blank=True)
    direccion = models.TextField(max_length=100, blank=True)
    telefono = models.CharField(validators=[phone_regex], max_length=15, blank=True)
    pais = CountryField()
    detalles = models.TextField(verbose_name="Detalles", blank=True)

    logo = models.ImageField(upload_to=logo_path)

    estado = models.PositiveSmallIntegerField(choices=ESTADO_EMPRESA, default=ACTIVO, blank=True)
    is_active = models.BooleanField(default=True)

    fecha_contratacion = models.DateTimeField(blank=True, null=True)
    fecha_suspension = models.DateTimeField(blank=True, null=True, verbose_name="Fecha de Suspension")

    nombre_facturacion = models.CharField(max_length=255, blank=True)
    rfc = models.CharField(max_length=30, blank=True, verbose_name="RFC/RUC")
    regimen_fiscal = models.CharField(max_length=10, blank=True, null=True)
    codigo_postal = models.CharField(max_length=50, blank=True)
    direccion_facturacion = models.TextField(max_length=100, blank=True)
    email_facturacion = models.EmailField(blank=True)

    timezone = models.CharField(max_length=190, blank=False, null=False, default="Etc/UTC")
    # Grupos de Servidores y Subdominios
    external_id = models.PositiveIntegerField(_('Id externo del lote al que pertenece'), db_index=True, blank=True,
                                              null=True)
    plan = models.ForeignKey('PlanEmpresa', related_name="empresa_plan_empresa", on_delete=models.SET_NULL,
                             null=True, blank=True, )

    class Meta:
        verbose_name = _("Empresa")
        verbose_name_plural = _("Empresas")
        permissions = {
            ('lista_empresas', _('Lista de empresas')),
            ('acciones_lista_empresas', _('Acciones lista de empresas')),
            ('crear_superusuarios', _('Crear super usuarios')),
            ('eliminar_superusuarios', _('Eliminar super usuarios')),
            ('ver_perfil_financiero', _('Ver perfil financiero')),
        }

    def __str__(self):
        return F"{self.nombre}"


class PlanEmpresa(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, db_index=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    precio_sin_iva = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    mostrar = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Última Actualización')

    class Meta:
        ordering = ('-created',)
        verbose_name = "Plan"
        verbose_name_plural = "Planes"

    def __str__(self):
        return '{}'.format(self.nombre)
