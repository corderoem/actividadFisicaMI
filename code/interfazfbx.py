import pyfbx 

def print_hierarchy(node, depth=0):
    for i in range(depth):
        print("  ", end="")
    print(node.GetName())

    for i in range(node.GetChildCount()):
        print_hierarchy(node.GetChild(i), depth + 1)

def main():
    # Crear un gestor de FBX
    fbx_manager = pyfbx.FbxManager.Create()

    # Crear una escena FBX
    fbx_scene = pyfbx.FbxScene.Create(fbx_manager, "MyScene")

    # Cargar el archivo FBX
    fbx_loader = pyfbx.FbxImporter.Create(fbx_manager, "")
    fbx_loader.Initialize("../files/testbody3.fbx")
    fbx_loader.Import(fbx_scene)
    fbx_loader.Destroy()

    # Imprimir la jerarquía del esqueleto
    root_node = fbx_scene.GetRootNode()
    print_hierarchy(root_node)

if __name__ == "__main__":
    main()