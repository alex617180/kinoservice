# Generated by Django 4.2.16 on 2024-11-28 12:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0003_add_gender_to_person_table'),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
                ALTER TABLE "content"."genre_film_work" 
                ADD CONSTRAINT "genre_film_work_film_work_id_genre_id_uniq" 
                UNIQUE ("film_work_id", "genre_id");
            """,
            reverse_sql='ALTER TABLE "content"."genre_film_work" DROP CONSTRAINT genre_film_work_film_work_id_genre_id_uniq',
        ),
        migrations.RunSQL(
            sql="""
                ALTER TABLE "content"."person_film_work" 
                ADD CONSTRAINT "person_film_work_film_work_id_genre_id_uniq" 
                UNIQUE ("film_work_id", "person_id");
            """,
            reverse_sql='ALTER TABLE "content"."person_film_work" DROP CONSTRAINT person_film_work_film_work_id_genre_id_uniq',
        ),
    ]