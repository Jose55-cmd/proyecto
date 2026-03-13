def perfil_nuevo(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        # Lógica para guardar en tu modelo de Base de Datos
        nuevo_perfil = Perfil.objects.create(nombre=nombre, descripcion=descripcion)
        return redirect('perfiles')
    return render(request, 'perfil_nuevo.html')