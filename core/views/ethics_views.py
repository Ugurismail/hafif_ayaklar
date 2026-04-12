from django.shortcuts import render


def ethics_atlas(request):
    return render(request, 'core/ethics_atlas.html')
