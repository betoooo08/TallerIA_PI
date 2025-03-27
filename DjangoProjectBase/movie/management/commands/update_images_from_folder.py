import os
from django.core.management.base import BaseCommand
from django.core.files import File
from movie.models import Movie

class Command(BaseCommand):
    help = "Actualiza las imágenes de las películas en la base de datos a partir de archivos en media/movie/images"

    def handle(self, *args, **kwargs):
        # 📥 Ruta de la carpeta con las imágenes de las películas
        images_folder = os.path.join('media', 'movie', 'images')

        # ✅ Verifica si la carpeta existe
        if not os.path.exists(images_folder):
            self.stderr.write(f"Carpeta de imágenes '{images_folder}' no encontrada.")
            return

        updated_count = 0

        # 📁 Iteramos sobre cada archivo en la carpeta
        for filename in os.listdir(images_folder):
            # Procesamos solo archivos con extensiones de imagen válidas
            if not filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                continue

            # Procesamos únicamente archivos que comiencen con "m_"
            if not filename.startswith("m_"):
                continue

            # Eliminamos el prefijo "m_" y obtenemos el nombre sin la extensión
            movie_title_raw = os.path.splitext(filename)[0][2:]
            # Reemplazamos guiones bajos por espacios y eliminamos espacios extras
            movie_title = movie_title_raw.replace("_", " ").strip()

            image_path = os.path.join(images_folder, filename)

            try:
                # Buscamos la película de forma insensible a mayúsculas/minúsculas
                movie = Movie.objects.get(title__iexact=movie_title)
                # Actualizamos el campo de imagen utilizando Django File
                with open(image_path, 'rb') as img_file:
                    movie.image.save(filename, File(img_file), save=True)

                updated_count += 1
                self.stdout.write(self.style.SUCCESS(f"Imagen actualizada para: {movie_title}"))

            except Movie.DoesNotExist:
                self.stderr.write(f"Película no encontrada: {movie_title}")
            except Exception as e:
                self.stderr.write(f"Error al actualizar la imagen para {movie_title}: {str(e)}")

        # ✅ Al finalizar, mostramos cuántas películas se actualizaron
        self.stdout.write(self.style.SUCCESS(f"Se actualizaron las imágenes de {updated_count} películas."))