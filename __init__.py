bl_info = {
	"name": "Vray Remove unused materials/nodetrees",
	"author": "JuhaW",
	"version": (0, 1, 0),
	"blender": (2, 78, 0),
	"location": "Scene>Node Tools",
	"description": "Remove unused materials and material nodetrees",
	"warning": "beta",
	"wiki_url": "",
	"category": "",
}


import bpy
from bpy.props import BoolProperty


class VrayDeleteUnusedMaterials(bpy.types.Operator):
	'''Remove all unused materials and material nodetrees'''
	bl_idname = "vray.delete_unused_materials"
	bl_label = "Remove Unused"
	
	def execute(self, context):

		matcnt = 0
		ntreecnt = 0
		if context.scene.materials:
			#delete unused materials
		
			for m in bpy.data.materials:
				if m.users == 0:
					print ("Deleted unused material:",m.name)
					bpy.data.materials.remove(m, do_unlink = True)
					matcnt += 1
		
		if context.scene.nodetrees:
			#delete unused material nodetrees

			nodetrees = [i.name for i in bpy.data.node_groups if i.bl_idname == 'VRayNodeTreeMaterial']
			
			for m in bpy.data.materials:
				if hasattr(m.vray.ntree,'name') and m.vray.ntree.name in nodetrees:
					nodetrees.remove(m.vray.ntree.name)

			for i in nodetrees:
				print ("Deleted unused nodetree:",i)	
				bpy.data.node_groups.remove(bpy.data.node_groups[i], do_unlink = True)
				ntreecnt += 1
			
		self.report({'INFO'},"Deleted {} Materials {} NodeTrees".format(matcnt, ntreecnt))
		return {'FINISHED'}
	

def Vray_Materials_Delete(self, context):
	
	layout = self.layout
	row = layout.row(align=True)
	row.operator("vray.delete_unused_materials", icon = 'ERROR')
	row.prop(context.scene,"materials")
	row.prop(context.scene,"nodetrees")
	
	
def register():
	bpy.utils.register_module(__name__)
	bpy.types.VRayPanelNodeTrees.append(Vray_Materials_Delete)
	bpy.types.Scene.materials = BoolProperty(default=True )
	bpy.types.Scene.nodetrees = BoolProperty(default=True )
	
def unregister():
	bpy.utils.unregister_module(__name__)
	bpy.types.VRayPanelNodeTrees.remove(Vray_Materials_Delete)
	del bpy.types.Scene.materials
	del bpy.types.Scene.nodetrees
	
if __name__ == "__main__":
	register()