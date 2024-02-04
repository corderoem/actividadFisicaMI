import bpy

# Ruta al archivo BVH
ruta_bvh = "../files/testhlt1.bvh"

# Limpia la escena actual en Blender
bpy.ops.wm.read_factory_settings(use_empty=True)

# Importa el archivo BVH
bpy.ops.import_anim.bvh(filepath=ruta_bvh)

# Establece la línea de tiempo para que coincida con la duración de la animación importada
bpy.context.scene.frame_start = bpy.context.scene.frame_preview_start = bpy.context.scene.frame_end = bpy.context.scene.frame_preview_end = bpy.context.scene.frame_step = 1

# Muestra la ventana de animación
bpy.context.scene.frame_preview_start = 1
bpy.context.scene.frame_preview_end = bpy.context.scene.frame_end

# Refresca la interfaz de usuario
bpy.context.view_layer.update()

# Actualiza la pantalla
bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
