from __future__ import unicode_literals

import os
import random

from datetime import (datetime, date)
from django.contrib.auth.models import (User)
from django.db import (models)
from django.db.models.signals import (post_save, pre_save)
from django.dispatch import (receiver)
from django.utils.translation import gettext_lazy as _

from ckeditor.fields import (RichTextField)
# from src.users.tokens import AccountActivationTokenGenerator


def get_upload_path(instance, filename):
    _filename = filename.split('.')
    _filename_ext = _filename[-1]
    _filename_name = ''.join(random.choice(_filename[0]) for _ in range(5))
    filename = '%s.%s' % (_filename_name,_filename_ext)
    try:
        uuii = User.objects.get(id=instance.user_id)
        a = uuii.username.lower()
        # print('---',instance.__dict__)
        # print(uuii.first_name)
    except:
        a = 'profile'
    return os.path.join('profile/%s/'%(a.lower()), datetime.now().date().strftime("%Y/%m/%d"), filename)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
    # print(sender.profile)
    # sender.profile.save()


class Newsletter(models.Model):
    """
    Newsletter module
    """
    name = models.CharField(max_length=140, verbose_name=_('Nombre de contacto'), blank=True)
    subject = RichTextField(verbose_name=_('Asunto'), blank=True)
    email = models.CharField(max_length=144, verbose_name=_('Direción email'), blank=True)
    message = RichTextField(blank=True, verbose_name=_('Mensaje'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('Usuario'), blank=True, null=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name=_('Ultima actualización'))

    def __str__(self):
        return self.name


class Profile(models.Model):
    """
    Extends defoult user model
    """
    ADMIN = 1
    SUPERVISOR = 2
    OFFICE = 3
    SELLER = 4
    BUYER = 5
    PROVIDER = 6
    ROLE_CHOICES = (
        ('ADMIN', 'admin'),
        ('SUPERVISOR', 'supervisor'),
        ('OFFICE', 'oficina'),
        ('SELLER', 'vendedor'),
        ('BUYER', 'comprador'),
        ('PROVIDER', 'proveedor'),
    )
    ACTIVE = 1
    INACTIVE = 2
    BLOCKED = 3
    STATUS_CHOICES = (
        ('ACTIVE',"activo"),
        ('INACTIVE',"inactivo"),
        ('BLOCKED',"bloqueado"),
    )
    COUNTRY_CHOICES = (
        ('AFG','Afganistán'),
        ('ALA','Islas de Åland'),
        ('ALB','Albania'),
        ('DZA','Argelia'),
        ('ASM','Samoa Americana'),
        ('AND','Andorra'),
        ('AGO','Angola'),
        ('AIA','Anguila'),
        ('ATA','Antártida'),
        ('ATG','Antigua y Barbuda'),
        ('ARG','Argentina'),
        ('ARM','Armenia'),
        ('ABW','Aruba'),
        ('AUS','Australia'),
        ('AUT','Austria'),
        ('AZE','Azerbaiyán'),
        ('BHS','Bahamas'),
        ('BHR','Baréin'),
        ('BGD','Bangladesh'),
        ('BRB','Barbados'),
        ('BLR','Bielorrusia'),
        ('BEL','Bélgica'),
        ('BLZ','Belice'),
        ('BEN','Benín'),
        ('BMU','Bermuda'),
        ('BTN','Bután'),
        ('BOL','Bolivia'),
        ('BES','Bonaire, San Eustaquio y Saba'),
        ('BIH','Bosnia y Herzegovina'),
        ('BWA','Botsuana'),
        ('BVT','Isla Bouvet'),
        ('BRA','Brasil'),
        ('IOT','Territorio Británico del Océano Índico'),
        ('VGB','Islas Vírgenes Británicas'),
        ('BRN','Brunei'),
        ('BGR','Bulgaria'),
        ('BFA','Burkina Faso'),
        ('BDI','Burundi'),
        ('KHM','Camboya'),
        ('CMR','Camerún'),
        ('CAN','Canadá'),
        ('CPV','Cabo Verde'),
        ('CYM','Islas Caimán'),
        ('CAF','República de África Central'),
        ('TCD','Chad'),
        ('CHL','Chile'),
        ('CHN','China'),
        ('CXR','Isla de Pascua'),
        ('CCK','Islas Cocos'),
        ('COL','Colombia'),
        ('COM','Comoras'),
        ('COK','Islas Cook'),
        ('CRI','Costa Rica'),
        ('HRV','Croacia'),
        ('CUB','Cuba'),
        ('CUW','Curazao'),
        ('CYP','Chipre'),
        ('CZE','República Checa'),
        ('COD','República Democrática del Congo'),
        ('DNK','Dinamarca'),
        ('DJI','Yibuti'),
        ('DMA','Dominica'),
        ('DOM','República Dominicana'),
        ('TLS','Timor Oriental'),
        ('ECU','Ecuador'),
        ('EGY','Egipto'),
        ('SLV','El Salvador'),
        ('GNQ','Guinea Ecuatorial'),
        ('ERI','Eritrea'),
        ('EST','Estonia'),
        ('ETH','Etiopía'),
        ('FLK','Islas Malvinas'),
        ('FRO','Islas Faroe'),
        ('FJI','Fiji'),
        ('FIN','Finlandia'),
        ('FRA','Francia'),
        ('GUF','Guayana Francesa'),
        ('PYF','Polinesia Francesa'),
        ('ATF','Territorios del sur Franceses'),
        ('GAB','Gabón'),
        ('GMB','Gambia'),
        ('GEO','Georgia'),
        ('DEU','Alemania'),
        ('GHA','Ghana'),
        ('GIB','Gibraltar'),
        ('GRC','Grecia'),
        ('GRL','Groenlandia'),
        ('GRD','Granada'),
        ('GLP','Guadalupe'),
        ('GUM','Guam'),
        ('GTM','Guatemala'),
        ('GGY','Guernsey'),
        ('GIN','Guinea'),
        ('GNB','Guinea Bissau'),
        ('GUY','Guyana'),
        ('HTI','Haití'),
        ('HMD','Islas Heard y McDonald'),
        ('HND','Honduras'),
        ('HKG','Hong Kong'),
        ('HUN','Hungría'),
        ('ISL','Islandia'),
        ('IND','India'),
        ('IDN','Indonesia'),
        ('IRN','Irán'),
        ('IRQ','Irak'),
        ('IRL','Irlanda'),
        ('IMN','Isla de Man'),
        ('ISR','Israel'),
        ('ITA','Italia'),
        ('CIV','Costa de Marfil'),
        ('JAM','Jamaica'),
        ('JPN','Japón'),
        ('JEY','Jersey'),
        ('JOR','Jordania'),
        ('KAZ','Kazajistán'),
        ('KEN','Kenia'),
        ('KIR','Kiribati'),
        ('XKX','Kosovo'),
        ('KWT','Kuwait'),
        ('KGZ','Kirguistán'),
        ('LAO','Laos'),
        ('LVA','Letonia'),
        ('LBN','Líbano'),
        ('LSO','Lesoto'),
        ('LBR','Liberia'),
        ('LBY','Libia'),
        ('LIE','Liechtenstein'),
        ('LTU','Lituania'),
        ('LUX','Luxemburgo'),
        ('MAC','Macao'),
        ('MKD','Macedonia'),
        ('MDG','Madagascar'),
        ('MWI','Malaui'),
        ('MYS','Malasia'),
        ('MDV','Maldivas'),
        ('MLI','Malí'),
        ('MLT','Malta'),
        ('MHL','Islas Marshall'),
        ('MTQ','Martinica'),
        ('MRT','Mauritania'),
        ('MUS','Mauricio'),
        ('MYT','Mayotte'),
        ('MEX','México'),
        ('FSM','Micronesia'),
        ('MDA','Moldavia'),
        ('MCO','Mónaco'),
        ('MNG','Mongolia'),
        ('MNE','Montenegro'),
        ('MSR','Montserrat'),
        ('MAR','Marruecos'),
        ('MOZ','Mozambique'),
        ('MMR','Myanmar'),
        ('NAM','Namibia'),
        ('NRU','Nauru'),
        ('NPL','Nepal'),
        ('NLD','Países Bajos'),
        ('ANT','Antillas Holandesas'),
        ('NCL','Nueva Caledonia'),
        ('NZL','Nueva Zelanda'),
        ('NIC','Nicaragua'),
        ('NER','Níger'),
        ('NGA','Nigeria'),
        ('NIU','Niue'),
        ('NFK','Isla Norfolk'),
        ('PRK','Corea del Norte'),
        ('MNP','Islas Marianas del Norte'),
        ('NOR','Noruega'),
        ('OMN','Omán'),
        ('PAK','Pakistán'),
        ('PLW','Palaos'),
        ('PSE','Territorios Palestinos'),
        ('PAN','Panamá'),
        ('PNG','Papúa Nueva Guinea'),
        ('PRY','Paraguay'),
        ('PER','Perú'),
        ('PHL','Filipinas'),
        ('PCN','Islas Pitcairn'),
        ('POL','Polonia'),
        ('PRT','Portugal'),
        ('PRI','Puerto Rico'),
        ('QAT','Catar'),
        ('COG','República del Congo'),
        ('REU','Reunión'),
        ('ROU','Rumanía'),
        ('RUS','Rusia'),
        ('RWA','Ruanda'),
        ('BLM','San Bartolomé'),
        ('SHN','Santa Elena'),
        ('KNA','San Cristóbal y Nieves'),
        ('LCA','Santa Lucía'),
        ('MAF','San Martín'),
        ('SPM','San Pedro y Miguelón'),
        ('VCT','San Vicente y las Granadinas'),
        ('WSM','Samoa Occidental'),
        ('SMR','San Marino'),
        ('STP','Santo Tomé y Príncipe'),
        ('SAU','Arabia Saudita'),
        ('SEN','Senegal'),
        ('SRB','Serbia'),
        ('SCG','Serbia y Montenegro'),
        ('SYC','Seychelles'),
        ('SLE','Sierra Leona'),
        ('SGP','Singapur'),
        ('SXM','San Martín'),
        ('SVK','Eslovaquia'),
        ('SVN','Eslovenia'),
        ('SLB','Islas Salomón'),
        ('SOM','Somalia'),
        ('ZAF','Sudáfrica'),
        ('SGS','Islas Georgia del Sur y Sandwich del Sur'),
        ('KOR','Corea del Sur'),
        ('SSD','Sudán del Sur'),
        ('ESP','España'),
        ('LKA','Sri Lanka'),
        ('SDN','Sudán'),
        ('SUR','Surinam'),
        ('SJM','Islas Svalbard y Jan Mayen'),
        ('SWZ','Suazilandia'),
        ('SWE','Suecia'),
        ('CHE','Suiza'),
        ('SYR','Siria'),
        ('TWN','Taiwán'),
        ('TJK','Tayikistán'),
        ('TZA','Tanzania'),
        ('THA','Tailandia'),
        ('TGO','República Togolesa'),
        ('TKL','Islas Tokelau'),
        ('TON','Tonga'),
        ('TTO','Trinidad y Tobago'),
        ('TUN','Túnez'),
        ('TUR','Turquía'),
        ('TKM','Turkmenistán'),
        ('TCA','Islas Turcos y Caicos'),
        ('TUV','Tuvalu'),
        ('VIR','Islas Vírgenes de los EE.UU.'),
        ('UGA','Uganda'),
        ('UKR','Ucrania'),
        ('ARE','Emiratos Árabes Unidos'),
        ('GBR','Reino Unido'),
        ('USA','Estados Unidos (USA)'),
        ('UMI','Islas menores alejadas de los Estados Unidos'),
        ('URY','Uruguay'),
        ('UZB','Uzbekistán'),
        ('VUT','Vanuatu'),
        ('VAT','Vaticano'),
        ('VEN','Venezuela'),
        ('VNM','Vietnam'),
        ('WLF','Wallis y Futuna'),
        ('ESH','Sahara Occidental'),
        ('YEM','Yemen'),
        ('ZMB','Zambia'),
        ('ZWE','Zimbabue'),
    )

    SCORE_CHOICES = (
        ('I','1'),
        ('II','2'),
        ('III','3'),
        ('IV','4'),
        ('V','5'),
        ('VI','6'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_('Usuario'))
    # code = models.CharField(max_length=144, blank=True, verbose_name=_('Codigo de usuario'))
    avatar = models.ImageField(
        verbose_name=_('Avatar de usuario'),
        upload_to=get_upload_path,
        null=True,
        blank=True,
        default='/profile/avatar.png',
    )
    bio = RichTextField( blank=True, verbose_name=_('Biografia'))
    birth_date = models.DateField(null=True, blank=True, verbose_name=_('Fecha de nacimiento'))
    description = RichTextField( blank=True, verbose_name=_('Descripción'))
    phone = models.CharField(max_length=144, blank=True, verbose_name=_('Numero de teléfono'))
    country = models.CharField(choices=COUNTRY_CHOICES, default='PAN', max_length=3, verbose_name=_('Pais'))
    city = models.CharField(max_length=144, blank=True, verbose_name=_('Ciudad'))
    direction1 = RichTextField( blank=True, verbose_name=_('Dirección 1'))
    direction2 = RichTextField( blank=True, verbose_name=_('Dirección 2'))
    zip_code = models.CharField(max_length=144, blank=True, verbose_name=_('Codigo zip'))
    location = models.CharField(max_length=30, blank=True, verbose_name=_('Miembro desde'))
    saldo = models.CharField(max_length=144, blank=True, verbose_name=_('Saldo disponible'))
    max_credit = models.CharField(max_length=144, blank=True, verbose_name=_('Credito maximo'))
    payment_lapse = models.CharField(max_length=144, blank=True, verbose_name=_('Lapso de pago'))
    respons = models.CharField(max_length=144, blank=True)#, verbose_name=_(''))
    status = models.CharField(choices=STATUS_CHOICES, default='INACTIVE', max_length=15, verbose_name=_('Estado de la cuenta'))
    score = models.CharField(choices=SCORE_CHOICES, default='IV', max_length=15, verbose_name=_('Puntuación'))
    role = models.CharField(choices=ROLE_CHOICES, default='BUYER', max_length=15, verbose_name=_('Roles'))
    member_since = models.DateTimeField(auto_now_add=True, verbose_name=_('Miembro desde'))
    email_confirmed = models.BooleanField(default=False, verbose_name=_('Correo confirmado'))

    def __str__(self):
        return self.get_fullname()

    
    class Meta:
        verbose_name = _('Perfil de Usuario')
        verbose_name_plural = _('Perfiles de Usuarios')

    def get_fullname(self):
        """
        Method to get the fullname of user
        """
        if self.user.last_name and self.user.first_name:
            fullname = '%s %s' % (self.user.first_name, self.user.last_name)
        else:
            fullname = self.user.email
        return fullname

    def get_avatar(self):
        """
        Easy method to get user avatar
        """
        avatar = self.user.profile.avatar
        img = 'staticfiles/base/img/avatar.png'
        if avatar.url:
            img = avatar.url
        return img

    def get_age(self):
        """
        This method calculate the age of user
        """
        if self.user.profile.birth_date:
            today = datetime.today()
            user_date = self.user.profile.birth_date
        return today.year - user_date - ((today.month, today.day) < (user_date.month, user_date.day))

    def get_user_status(self):
        """
        Easy method to get user status
        """
        status = '%s' % (self.user.profile.status)
        return status

    def exists(self):
        """
        Method to verify if user has profile
        """
        user = Profile.objects.get(user=self.user.pk)
        if user:
            return True
        else:
            return False
            

    # def save(self, *args, **kwargs):
    #     if self.request.user.profile.email_confirmed and self.user.profile.status == 'INACTIVE':
            
    #     super(Profile, self).save(*args, **kwargs)


class Frecuency(models.Model):
    """
    User frecuency
    """
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE,)
    average = models.CharField(max_length=144, blank=True)
    monday = models.CharField(max_length=144, blank=True)
    tuesday = models.CharField(max_length=144, blank=True)
    wednesday = models.CharField(max_length=144, blank=True)
    thursday = models.CharField(max_length=144, blank=True)
    friday = models.CharField(max_length=144, blank=True)
    saturday = models.CharField(max_length=144, blank=True)
    sunday = models.CharField(max_length=144, blank=True)

    def __str__(self):
        return self.user

    class Meta:
        verbose_name = 'Frecuencia de visita'
        verbose_name_plural = 'Frecuencia de visitas'

