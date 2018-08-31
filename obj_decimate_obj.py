import bpy
import sys
import os

def delete_all():
        for item in bpy.context.scene.objects:
                bpy.context.scene.objects.unlink(item)

        for item in bpy.data.objects:
                bpy.data.objects.remove(item)

        for item in bpy.data.meshes:
                bpy.data.meshes.remove(item)

        for item in bpy.data.materials:
                bpy.data.materials.remove(item)

def load_obj_file(filepath):
    bpy.ops.import_scene.obj(filepath=filepath,axis_forward='-Z', axis_up='Y' )

def decimate_obj(decimate_ratio):
    obj = bpy.data.objects[obj_name]
    if(obj.type=="MESH"):
        #VERTEX_PAINTモードに変更しとく
        bpy.context.scene.objects.active = bpy.data.objects[obj_name]
        bpy.ops.object.mode_set(mode='VERTEX_PAINT', toggle=False)
        #DECIMATEで頂点数削減
        modifier=obj.modifiers.new('DecimateMod' ,'DECIMATE')
        modifier.ratio=decimate_ratio
        modifier.use_collapse_triangulate=True
        bpy.ops.object.modifier_apply( modifier = 'DecimateMod' )
        
        global mesh 
        mesh = obj.to_mesh(bpy.context.scene, True, 'RENDER')

        #DEBUG
        print("num of vertices:", len(mesh.vertices))
        print("num of polygons:", len(mesh.polygons))
        '''DEBUG
        for idx , pl in enumerate( mesh.polygons):
            print("polygon index:{0:2} ".format(pl.index), end="")
            print("vertices:", end="")
            if(idx==20):
                break
            for vi in pl.vertices:
                print("{0:2}, ".format(vi), end="")
                print("")
        print("num of vertex color layers:", mesh.vertex_colors[0])
        print(mesh.vertex_colors[0])
        print(len(mesh.vertex_colors['Col'].data))
        for ly in mesh.vertex_colors:
            print(ly.name)
            for idx, vc in enumerate(mesh.vertex_colors['Col'].data):
                print("  {0:2}:{1}".format(idx,vc.color))
                if(idx==20):
                    break
        '''

def export_obj( out_file ):
    with open(out_file, mode='w') as f:
        # 頂点カラーをverticesに整列
        v_color_idx = 0
        v_colors = [0] * len(mesh.vertex_colors['Col'].data)
        for pl in mesh.polygons:
            for vi in pl.vertices:
                v_colors[vi] = mesh.vertex_colors['Col'].data[v_color_idx]
                v_color_idx+=1
        # v
        for i , vt in enumerate(mesh.vertices):
            f.write('v '+'{:.2f}'.format(vt.co.x)+' '+'{:.2f}'.format(vt.co.y)+' '+'{:.2f}'.format(vt.co.z))
            f.write(' ' + '{:.2f}'.format(v_colors[i].color.r) + ' ' + '{:.2f}'.format(v_colors[i].color.g) + ' ' + '{:.2f}'.format(v_colors[i].color.b) )
            f.write('\n')
            #print("vertex index:{0:2} co:{1} normal:{2}".format(vt.index, vt.co, vt.normal))
        # f
        for pl in mesh.polygons:
            #print("polygon index:{0:2} ".format(pl.index), end="")
            #print("vertices:", end="")
            #objファイルのfは1始まりなので+1
            f.write('f '+str(pl.vertices[2]+1)+' '+str(pl.vertices[1]+1)+' '+str(pl.vertices[0]+1))
            f.write('\n')
            '''
            for vi in pl.vertices:
                print("{0:2}, ".format(vi), end="")
                print("")
            '''
if __name__ == "__main__":

    # Get object file path from 1st argument after "--".
    # Get png file path from 2nd argument after "--".
    argv = sys.argv
    argv = argv[argv.index("--") + 1:] # get all args after "--"
    print(argv)
    obj_file = argv[0]
    out_file = argv[1]
    decimate_ratio = argv[2]
    filename  = os.path.basename(obj_file)
    obj_name, ext = os.path.splitext(filename)
    delete_all()
    #objファイルをロード
    load_obj_file(obj_file)

    #頂点数減らす
    decimate_obj(float(decimate_ratio))

    #ファイルにはく
    export_obj(out_file)

    #blenderを終了する。
#    bpy.ops.wm.quit_blender()
