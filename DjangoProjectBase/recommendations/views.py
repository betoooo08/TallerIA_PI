from django.shortcuts import render
from movie.models import Movie
import random

def recommendation_view(request):
    prompt = request.GET.get('prompt', '')
    recommended_movie = None

    if prompt:
        # Ejemplo simple: buscar películas que contengan el prompt en el título o la descripción.
        movies = Movie.objects.filter(title__icontains=prompt) | Movie.objects.filter(description__icontains=prompt)
        if movies.exists():
            recommended_movie = random.choice(list(movies))
        else:
            # Si no hay coincidencias, se selecciona una película al azar
            movies_all = Movie.objects.all()
            if movies_all.exists():
                recommended_movie = random.choice(list(movies_all))
    
    return render(request, 'recommendation.html', {
        'prompt': prompt,
        'recommended_movie': recommended_movie
    })