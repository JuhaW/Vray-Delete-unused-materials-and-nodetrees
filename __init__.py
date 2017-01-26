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
	'''Remove all unused materials and nodetrees'''
	bl_idname = "vray.delete_unused_materials"
	bl_label = "Remove Unused"
	
	def execute(self, context):

		matcnt = 0
		mat_treecnt = 0
		obj_treecnt = 0
		light_treecnt = 0
		scene_treecnt = 0
		world_treecnt = 0
		
		#MATERIAL
		if context.scene.materials:
			#delete unused materials
		
			for m in bpy.data.materials:
				if m.users == 0:
					print ("Deleted unused material:",m.name)
					bpy.data.materials.remove(m, do_unlink = True)
					matcnt += 1
		
		if context.scene.mat_ntree:
			#delete unused material nodetrees

			nodetrees = [i.name for i in bpy.data.node_groups if i.bl_idname == 'VRayNodeTreeMaterial']
			
			for m in bpy.data.materials:
				if hasattr(m.vray.ntree,'name') and m.vray.ntree.name in nodetrees:
					nodetrees.remove(m.vray.ntree.name)

			for i in nodetrees:
				print ("Deleted unused material nodetree:",i)	
				bpy.data.node_groups.remove(bpy.data.node_groups[i], do_unlink = True)
				mat_treecnt += 1
		
		#OBJECT	
		if context.scene.obj_ntree:
			nodetrees = [i.name for i in bpy.data.node_groups if i.bl_idname == 'VRayNodeTreeObject']
			for m in bpy.data.objects:
				if hasattr(m.vray.ntree,'name') and m.vray.ntree.name in nodetrees:
					nodetrees.remove(m.vray.ntree.name)

			for i in nodetrees:
				print ("Deleted unused object nodetree:",i)	
				bpy.data.node_groups.remove(bpy.data.node_groups[i], do_unlink = True)
				obj_treecnt += 1
	
		#LIGHT	
		if context.scene.light_ntree:	
			nodetrees = [i.name for i in bpy.data.node_groups if i.bl_idname == 'VRayNodeTreeLight']
			for m in bpy.data.lamps:
				if hasattr(m.vray.ntree,'name') and m.vray.ntree.name in nodetrees:
					nodetrees.remove(m.vray.ntree.name)

			for i in nodetrees:
				print ("Deleted unused light nodetree:",i)	
				bpy.data.node_groups.remove(bpy.data.node_groups[i], do_unlink = True)
				light_treecnt += 1
		
		#SCENE
		if context.scene.scene_ntree:	
			ntree_list = list(set([i.vray.ntree for i in bpy.data.scenes if i.vray.ntree]))
			scene_trees = [i for i in bpy.data.node_groups if i.bl_idname == 'VRayNodeTreeScene' and i not in(ntree_list)]
			for i in scene_trees:
				bpy.data.node_groups.remove(i)
				scene_treecnt +=1
		#WORLD
		if context.scene.world_ntree:
			worlds = list(set([s.world for s in bpy.data.scenes if s.world]))
			w = list(set(worlds).symmetric_difference(set(bpy.data.worlds[:])))
			for i in w:
				bpy.data.worlds.remove(i)

			used_ntrees = [w.vray.ntree for w in worlds if w.vray.ntree]
			ntrees = [i for i in bpy.data.node_groups if i.bl_idname == 'VRayNodeTreeWorld' and i not in(used_ntrees)]
			for i in ntrees:
				bpy.data.node_groups.remove(i)
				world_treecnt +=1
			
		self.report({'INFO'},"Deleted: {} Materials {} MaterialTrees {} ObjectTrees {} LightTrees, {} SceneTrees, {} WorldTrees".format(matcnt, mat_treecnt, obj_treecnt, light_treecnt, scene_treecnt, world_treecnt))
		return {'FINISHED'}
	

def Vray_Materials_Delete(self, context):
	
	layout = self.layout
	row = layout.row(align=True)
	row.operator("vray.delete_unused_materials", icon = 'ERROR')
	row.prop(context.scene,"materials", text = "Object materials")
	row = layout.row(align=True)
	row.label("Nodetrees:")
	row.prop(context.scene,"mat_ntree", text = "Material")
	row.prop(context.scene,"obj_ntree", text = "Object")
	row = layout.row(align=True)
	row.prop(context.scene,"light_ntree", text = "Light")
	row.prop(context.scene,"scene_ntree", text = "Scene")
	row.prop(context.scene,"world_ntree", text = "World")
	
def register():
	bpy.utils.register_module(__name__)
	bpy.types.VRayPanelNodeTrees.append(Vray_Materials_Delete)
	bpy.types.Scene.materials = BoolProperty(default=True )
	bpy.types.Scene.mat_ntree = BoolProperty(default=True )
	bpy.types.Scene.obj_ntree = BoolProperty(default=True )
	bpy.types.Scene.light_ntree = BoolProperty(default=True )
	bpy.types.Scene.scene_ntree = BoolProperty(default=True )
	bpy.types.Scene.world_ntree = BoolProperty(default=True )
	
def unregister():
	bpy.utils.unregister_module(__name__)
	bpy.types.VRayPanelNodeTrees.remove(Vray_Materials_Delete)
	del bpy.types.Scene.materials
	del bpy.types.Scene.mat_ntree
	del bpy.types.Scene.obj_ntree
	del bpy.types.Scene.light_ntree
	del bpy.types.Scene.scene_ntree
	del bpy.types.Scene.world_ntree
	
if __name__ == "__main__":
	register()