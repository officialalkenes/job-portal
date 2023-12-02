# Generated by Django 4.2.7 on 2023-12-02 16:14

from django.conf import settings
import django.contrib.gis.db.models.fields
import django.contrib.gis.geos.point
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='JobListing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Job Title')),
                ('description', models.TextField(null=True)),
                ('company', models.CharField(max_length=100)),
                ('company_email', models.EmailField(max_length=254, null=True)),
                ('address', models.CharField(max_length=255, null=True)),
                ('job_type', models.CharField(choices=[('Permanent', 'Permanent'), ('Remote', 'Remote'), ('Contract', 'Contract'), ('InternShip', 'Internship')], default='Remote', max_length=20)),
                ('education', models.CharField(choices=[('Bachelors', 'Bachelors'), ('Masters', 'Masters'), ('Phd', 'Phd')], max_length=30)),
                ('industry', models.CharField(choices=[('Information and Technology', 'It'), ('Ai Services', 'Ai'), ('Education', 'Education'), ('Telecommunication', 'Comms'), ('Software Development', 'Development'), ('Creative Designs', 'Design'), ('Admin/Customer Support', 'Support'), ('Marketting and Sales', 'Sales')], max_length=30)),
                ('experience', models.CharField(choices=[('No Experience', 'Inexperience'), ('Less than 1 year', 'Less Than A Year'), ('One Year', 'One Year'), ('Two Years', 'Two Years'), ('Two Years and above', 'Above Two Years')], max_length=30)),
                ('salary', models.PositiveIntegerField(default=5, validators=[django.core.validators.MinValueValidator(5), django.core.validators.MaxValueValidator(1000000)])),
                ('positions', models.CharField(max_length=100)),
                ('geo_point', django.contrib.gis.db.models.fields.PointField(default=django.contrib.gis.geos.point.Point(0.0, 0.0), srid=4326)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
