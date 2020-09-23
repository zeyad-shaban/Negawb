from categories.models import Category
from django.contrib.auth.models import AbstractUser
from django.db import models
from PIL import Image


class User(AbstractUser):
    # Advance
    website = models.URLField(blank=True, null=True)

    # Admin stuff
    is_confirmed = models.BooleanField(default=False)
    # Society
    friends = models.ManyToManyField('User', blank=True)
    followers = models.ManyToManyField(
        'User', related_name='user_followers', blank=True)
    # Personal
    username = models.CharField(
        ('username'),
        max_length=30,
        unique=True,
        help_text=('30 characters or fewer.'),
        error_messages={
            'unique': ("A user with that username already exists."),
        },
    )
    bio = models.CharField(
        max_length=200, default='Hi there!', blank=True, null=True,)
    phone = models.CharField(max_length=14, null=True, blank=True, unique=True)
    avatar = models.ImageField(
        upload_to='profile_images', default='profile_images/DefaultUserImage.jpg',)
    cover = models.ImageField(
        upload_to='userpage/cover', default="userpage/cover/DefaultCover.jpg")
    birthday = models.DateField(blank=True, null=True)
    COUNTRIES_CHOICES = (
        ('AD', 'Andorra'),
        ('AE', 'United Arab Emirates'),
        ('AF', 'Afghanistan'),
        ('AG', 'Antigua & Barbuda'),
        ('AI', 'Anguilla'),
        ('AL', 'Albania'),
        ('AM', 'Armenia'),
        ('AN', 'Netherlands Antilles'),
        ('AO', 'Angola'),
        ('AQ', 'Antarctica'),
        ('AR', 'Argentina'),
        ('AS', 'American Samoa'),
        ('AT', 'Austria'),
        ('AU', 'Australia'),
        ('AW', 'Aruba'),
        ('AZ', 'Azerbaijan'),
        ('BA', 'Bosnia and Herzegovina'),
        ('BB', 'Barbados'),
        ('BD', 'Bangladesh'),
        ('BE', 'Belgium'),
        ('BF', 'Burkina Faso'),
        ('BG', 'Bulgaria'),
        ('BH', 'Bahrain'),
        ('BI', 'Burundi'),
        ('BJ', 'Benin'),
        ('BM', 'Bermuda'),
        ('BN', 'Brunei Darussalam'),
        ('BO', 'Bolivia'),
        ('BR', 'Brazil'),
        ('BS', 'Bahama'),
        ('BT', 'Bhutan'),
        ('BV', 'Bouvet Island'),
        ('BW', 'Botswana'),
        ('BY', 'Belarus'),
        ('BZ', 'Belize'),
        ('CA', 'Canada'),
        ('CC', 'Cocos (Keeling) Islands'),
        ('CF', 'Central African Republic'),
        ('CG', 'Congo'),
        ('CH', 'Switzerland'),
        ('CI', 'Ivory Coast'),
        ('CK', 'Cook Iislands'),
        ('CL', 'Chile'),
        ('CM', 'Cameroon'),
        ('CN', 'China'),
        ('CO', 'Colombia'),
        ('CR', 'Costa Rica'),
        ('CU', 'Cuba'),
        ('CV', 'Cape Verde'),
        ('CX', 'Christmas Island'),
        ('CY', 'Cyprus'),
        ('CZ', 'Czech Republic'),
        ('DE', 'Germany'),
        ('DJ', 'Djibouti'),
        ('DK', 'Denmark'),
        ('DM', 'Dominica'),
        ('DO', 'Dominican Republic'),
        ('DZ', 'Algeria'),
        ('EC', 'Ecuador'),
        ('EE', 'Estonia'),
        ('EG', 'Egypt'),
        ('EH', 'Western Sahara'),
        ('ER', 'Eritrea'),
        ('ES', 'Spain'),
        ('ET', 'Ethiopia'),
        ('FI', 'Finland'),
        ('FJ', 'Fiji'),
        ('FK', 'Falkland Islands (Malvinas)'),
        ('FM', 'Micronesia'),
        ('FO', 'Faroe Islands'),
        ('FR', 'France'),
        ('FX', 'France, Metropolitan'),
        ('GA', 'Gabon'),
        ('GB', 'United Kingdom (Great Britain)'),
        ('GD', 'Grenada'),
        ('GE', 'Georgia'),
        ('GF', 'French Guiana'),
        ('GH', 'Ghana'),
        ('GI', 'Gibraltar'),
        ('GL', 'Greenland'),
        ('GM', 'Gambia'),
        ('GN', 'Guinea'),
        ('GP', 'Guadeloupe'),
        ('GQ', 'Equatorial Guinea'),
        ('GR', 'Greece'),
        ('GS', 'South Georgia and the South Sandwich Islands'),
        ('GT', 'Guatemala'),
        ('GU', 'Guam'),
        ('GW', 'Guinea-Bissau'),
        ('GY', 'Guyana'),
        ('HK', 'Hong Kong'),
        ('HM', 'Heard & McDonald Islands'),
        ('HN', 'Honduras'),
        ('HR', 'Croatia'),
        ('HT', 'Haiti'),
        ('HU', 'Hungary'),
        ('ID', 'Indonesia'),
        ('IE', 'Ireland'),
        ('IL', 'Israel'),
        ('IN', 'India'),
        ('IO', 'British Indian Ocean Territory'),
        ('IQ', 'Iraq'),
        ('IR', 'Islamic Republic of Iran'),
        ('IS', 'Iceland'),
        ('IT', 'Italy'),
        ('JM', 'Jamaica'),
        ('JO', 'Jordan'),
        ('JP', 'Japan'),
        ('KE', 'Kenya'),
        ('KG', 'Kyrgyzstan'),
        ('KH', 'Cambodia'),
        ('KI', 'Kiribati'),
        ('KM', 'Comoros'),
        ('KN', 'St. Kitts and Nevis'),
        ('KP', 'Korea, Democratic People\'s Republic of'),
        ('KR', 'Korea, Republic of'),
        ('KW', 'Kuwait'),
        ('KY', 'Cayman Islands'),
        ('KZ', 'Kazakhstan'),
        ('LA', 'Lao People\'s Democratic Republic'),
        ('LB', 'Lebanon'),
        ('LC', 'Saint Lucia'),
        ('LI', 'Liechtenstein'),
        ('LK', 'Sri Lanka'),
        ('LR', 'Liberia'),
        ('LS', 'Lesotho'),
        ('LT', 'Lithuania'),
        ('LU', 'Luxembourg'),
        ('LV', 'Latvia'),
        ('LY', 'Libyan Arab Jamahiriya'),
        ('MA', 'Morocco'),
        ('MC', 'Monaco'),
        ('MD', 'Moldova, Republic of'),
        ('MG', 'Madagascar'),
        ('MH', 'Marshall Islands'),
        ('ML', 'Mali'),
        ('MN', 'Mongolia'),
        ('MM', 'Myanmar'),
        ('MO', 'Macau'),
        ('MP', 'Northern Mariana Islands'),
        ('MQ', 'Martinique'),
        ('MR', 'Mauritania'),
        ('MS', 'Monserrat'),
        ('MT', 'Malta'),
        ('MU', 'Mauritius'),
        ('MV', 'Maldives'),
        ('MW', 'Malawi'),
        ('MX', 'Mexico'),
        ('MY', 'Malaysia'),
        ('MZ', 'Mozambique'),
        ('NA', 'Namibia'),
        ('NC', 'New Caledonia'),
        ('NE', 'Niger'),
        ('NF', 'Norfolk Island'),
        ('NG', 'Nigeria'),
        ('NI', 'Nicaragua'),
        ('NL', 'Netherlands'),
        ('NO', 'Norway'),
        ('NP', 'Nepal'),
        ('NR', 'Nauru'),
        ('NU', 'Niue'),
        ('NZ', 'New Zealand'),
        ('OM', 'Oman'),
        ('PA', 'Panama'),
        ('PE', 'Peru'),
        ('PF', 'French Polynesia'),
        ('PG', 'Papua New Guinea'),
        ('PH', 'Philippines'),
        ('PK', 'Pakistan'),
        ('PL', 'Poland'),
        ('PM', 'St. Pierre & Miquelon'),
        ('PN', 'Pitcairn'),
        ('PR', 'Puerto Rico'),
        ('PT', 'Portugal'),
        ('PW', 'Palau'),
        ('PY', 'Paraguay'),
        ('QA', 'Qatar'),
        ('RE', 'Reunion'),
        ('RO', 'Romania'),
        ('RU', 'Russian Federation'),
        ('RW', 'Rwanda'),
        ('SA', 'Saudi Arabia'),
        ('SB', 'Solomon Islands'),
        ('SC', 'Seychelles'),
        ('SD', 'Sudan'),
        ('SE', 'Sweden'),
        ('SG', 'Singapore'),
        ('SH', 'St. Helena'),
        ('SI', 'Slovenia'),
        ('SJ', 'Svalbard & Jan Mayen Islands'),
        ('SK', 'Slovakia'),
        ('SL', 'Sierra Leone'),
        ('SM', 'San Marino'),
        ('SN', 'Senegal'),
        ('SO', 'Somalia'),
        ('SR', 'Suriname'),
        ('ST', 'Sao Tome & Principe'),
        ('SV', 'El Salvador'),
        ('SY', 'Syrian Arab Republic'),
        ('SZ', 'Swaziland'),
        ('TC', 'Turks & Caicos Islands'),
        ('TD', 'Chad'),
        ('TF', 'French Southern Territories'),
        ('TG', 'Togo'),
        ('TH', 'Thailand'),
        ('TJ', 'Tajikistan'),
        ('TK', 'Tokelau'),
        ('TM', 'Turkmenistan'),
        ('TN', 'Tunisia'),
        ('TO', 'Tonga'),
        ('TP', 'East Timor'),
        ('TR', 'Turkey'),
        ('TT', 'Trinidad & Tobago'),
        ('TV', 'Tuvalu'),
        ('TW', 'Taiwan, Province of China'),
        ('TZ', 'Tanzania, United Republic of'),
        ('UA', 'Ukraine'),
        ('UG', 'Uganda'),
        ('UM', 'United States Minor Outlying Islands'),
        ('US', 'United States of America'),
        ('UY', 'Uruguay'),
        ('UZ', 'Uzbekistan'),
        ('VA', 'Vatican City State (Holy See)'),
        ('VC', 'St. Vincent & the Grenadines'),
        ('VE', 'Venezuela'),
        ('VG', 'British Virgin Islands'),
        ('VI', 'United States Virgin Islands'),
        ('VN', 'Viet Nam'),
        ('VU', 'Vanuatu'),
        ('WF', 'Wallis & Futuna Islands'),
        ('WS', 'Samoa'),
        ('YE', 'Yemen'),
        ('YT', 'Mayotte'),
        ('YU', 'Yugoslavia'),
        ('ZA', 'South Africa'),
        ('ZM', 'Zambia'),
        ('ZR', 'Zaire'),
        ('ZW', 'Zimbabwe'),
    )
    country = models.CharField(
        max_length=2, choices=COUNTRIES_CHOICES, blank=True, null=True)
    # Confirmation
    email_code = models.IntegerField(null=True, blank=True)
    phone_code = models.IntegerField(null=True, blank=True)

    # PRIVACY
    show_email = models.BooleanField(default=True)
    who_see_avatar_choices = [
        ('none', 'No One'),
        ('friends', 'Friends only'),
        ('everyone', 'Every One'),
    ]
    who_see_avatar = models.CharField(
        max_length=30,
        choices=who_see_avatar_choices,
        default='everyone',
    )
    who_add_group_choices = [
        ('none', 'No One'),
        ('friends', 'Friends Only'),
        ('everyone', 'Every One'),
    ]
    who_add_group = models.CharField(
        max_length=30,
        choices=who_add_group_choices,
        default='everyone')
    allow_friend_request = models.BooleanField(default=True)

    # ---------DISTRACTION FREE-----------
    # Rated
    video_rate = models.IntegerField(default=33)
    image_rate = models.IntegerField(default=33)
    text_rate = models.IntegerField(default=33)
    # toggling
    hide_comments = models.BooleanField(default=False)
    hide_recommended_posts = models.BooleanField(default=False)
    blocked_topics = models.ManyToManyField(Category, blank=True)
    default_home_choices = [
        ('all_posts', 'All posts (default)'),
        ('followed_posts', 'Followed posts'),
        ('chat', 'Chat'),
    ]
    homepage = models.CharField(
        max_length=25, choices=default_home_choices, default=default_home_choices[0])
    # notifications
    allow_important_friend_messages = models.BooleanField(default=True)
    allow_important_group_message = models.BooleanField(default=True)
    allow_normal_friend_message = models.BooleanField(default=True)
    allow_normal_group_message = models.BooleanField(default=True)
    allow_comment_message = models.BooleanField(default=True)
    allow_reply_message = models.BooleanField(default=True)
    allow_invites = models.BooleanField(default=True)
    your_invites = models.BooleanField(default=True)

    # IMAGE RESIZING
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.avatar:
            img = Image.open(self.avatar.path)
            if img.width > 160 or img.height > 160:
                output_size = (160, 160)
                img.thumbnail(output_size)
                img.save(self.avatar.path)
