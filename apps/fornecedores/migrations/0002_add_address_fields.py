from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("fornecedores", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="fornecedor",
            name="cep",
            field=models.CharField(blank=True, max_length=9, verbose_name="CEP"),
        ),
        migrations.AddField(
            model_name="fornecedor",
            name="logradouro",
            field=models.CharField(blank=True, max_length=200, verbose_name="Logradouro"),
        ),
        migrations.AddField(
            model_name="fornecedor",
            name="numero",
            field=models.CharField(blank=True, max_length=20, verbose_name="Número"),
        ),
        migrations.AddField(
            model_name="fornecedor",
            name="bairro",
            field=models.CharField(blank=True, max_length=100, verbose_name="Bairro"),
        ),
    ]
