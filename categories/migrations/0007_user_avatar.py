# Generated by Django 3.0.8 on 2020-07-21 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0006_auto_20200720_1615'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.ImageField(default='https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.pinterest.com%2Fpin%2F551761391822118649%2F&psig=AOvVaw3WUzHXrM9DPYgmewZv9hc2&ust=1595418598608000&source=images&cd=vfe&ved=0CAIQjRxqFwoTCMjf5suj3uoCFQAAAAAdAAAAABAF', upload_to='categories/images/'),
        ),
    ]
