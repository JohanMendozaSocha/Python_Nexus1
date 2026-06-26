from django.contrib import admin
from .models import Foro, Publicacion, Reporte

@admin.register(Foro)
class ForoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'categoria', 'id_creador', 'created_at')
    search_fields = ('titulo', 'descripcion', 'categoria')
    list_filter = ('categoria', 'created_at')

@admin.register(Publicacion)
class PublicacionAdmin(admin.ModelAdmin):
    list_display = ('id', 'id_foro', 'id_usuario', 'created_at')
    search_fields = ('contenido',)
    list_filter = ('created_at',)


@admin.register(Reporte)
class ReporteAdmin(admin.ModelAdmin):
    list_display = ('motivo', 'id_usuario', 'get_target', 'comentario_adicional', 'created_at')
    list_filter = ('motivo', 'created_at')
    search_fields = ('comentario_adicional',)
    
    
    actions = ['eliminar_contenido_inapropiado', 'descartar_reporte_falso']

    def get_target(self, obj):
        if obj.id_foro:
            return f"FORUM: {obj.id_foro.titulo}"
        elif obj.id_publicacion:
            return f"COMMENT: {obj.id_publicacion.contenido[:30]}..."
        return "Unknown"
    get_target.short_description = 'Reported Content'


    @admin.action(description="❌ DELETE reported content (Inappropriate)")
    def eliminar_contenido_inapropiado(self, request, queryset):
        for reporte in queryset:
            
            if reporte.id_foro:
                reporte.id_foro.delete()
           
            elif reporte.id_publicacion:
                reporte.id_publicacion.delete()
            
           
            try:
                reporte.delete()
            except:
                pass
                
        self.message_user(request, "The inappropriate content has been successfully deleted from the platform.")

    @admin.action(description="🛡️ DISMISS report (Content is OK)")
    def descartar_reporte_falso(self, request, queryset):
        
        queryset.delete()
        self.message_user(request, "Reports dismissed. The content was kept online.")