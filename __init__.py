if "bpy" in locals():
    import importlib
    importlib.reload(sdfexportpanel)
else:
    from . import (
        sdfexportpanel
    )

    
import bpy



def register():
    sdfexportpanel.register()

    

def unregister():
    sdfexportpanel.unregister()
