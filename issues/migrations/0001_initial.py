# Generated by Django 4.1.5 on 2023-01-26 19:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('name', models.CharField(max_length=50, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={'verbose_name_plural': 'categories',},
        ),
        migrations.CreateModel(
            name='Issue',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('description', models.TextField()),
                (
                    'assignee',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT,
                        related_name='assigned_issues',
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    'category',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT, to='issues.category',
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name='IssueStateChange',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'new_state',
                    models.CharField(
                        choices=[
                            ('TO_DO', 'TO DO'),
                            ('IN_PROGRESS', 'IN PROGRESS'),
                            ('DONE', 'DONE'),
                            ('CANCELED', 'CANCELED'),
                        ],
                        default='TO_DO',
                        max_length=20,
                    ),
                ),
                ('occurred_at', models.DateTimeField(auto_now_add=True)),
                (
                    'issue',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT, to='issues.issue'
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name='issue',
            name='last_state_change',
            field=models.ForeignKey(
                blank=True,
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.RESTRICT,
                related_name='current_state_issue',
                to='issues.issuestatechange',
            ),
        ),
        migrations.AddField(
            model_name='issue',
            name='reporter',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.RESTRICT,
                related_name='reported_issues',
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]