# Generated manually

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_models', '0007_comentario'),
    ]

    operations = [
        migrations.AddField(
            model_name='archivoincidencia',
            name='cloudinary_public_id',
            field=models.CharField(blank=True, help_text='Public ID del archivo en Cloudinary', max_length=500, null=True),
        ),
    ]
