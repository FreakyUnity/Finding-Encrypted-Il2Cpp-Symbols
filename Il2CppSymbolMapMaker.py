import json, string

goodRefs = open("good.txt", "r").read().splitlines()
badRefs = open("bad.txt", "r").read().splitlines()

symbolDict : dict = {}

def ExtractString(obj : str) -> str:
    obj = str(obj).strip()
    nstr : str = ""
    if "il2cpp: " in obj:
        nstr = obj.split(" ")[2]
    elif "\"" in obj:
        on = False
        for char in obj:
            if char == "\"":
                on = not on
                continue
            else:
                if on:
                    nstr += char
    
    return nstr

def GetCodeLines(lines : list[str]) -> list[str]:
    nlines = []
    for line in lines:
        if "il2cpp: " in line:
            continue 
        elif "\"" in line:
            if "\"\"" not in line:
                nlines.append(ExtractString(line))

    return nlines

def DumpToBNMFile(data : dict):
    sheesh = """#pragma once\n\n#define BNM_IL2CPP_API_il2cpp_init "{}"\n#define BNM_IL2CPP_API_il2cpp_class_from_il2cpp_type "{}"\n#define BNM_IL2CPP_API_il2cpp_array_new_specific "{}"\n#define BNM_IL2CPP_API_il2cpp_class_from_type "{}"\n\n#define BNM_IL2CPP_API_il2cpp_type_get_class_or_element_class "{}"\n#define BNM_IL2CPP_API_il2cpp_domain_get_assemblies "{}"\n#define BNM_IL2CPP_API_il2cpp_domain_assembly_open "{}"\n\n#define BNM_IL2CPP_API_il2cpp_image_get_class "{}"\n#define BNM_IL2CPP_API_il2cpp_get_corlib "{}"\n#define BNM_IL2CPP_API_il2cpp_class_from_name "{}"\n#define BNM_IL2CPP_API_il2cpp_assembly_get_image "{}"\n#define BNM_IL2CPP_API_il2cpp_method_get_param_name "{}"\n#define BNM_IL2CPP_API_il2cpp_array_class_get "{}"\n#define BNM_IL2CPP_API_il2cpp_type_get_object "{}"\n#define BNM_IL2CPP_API_il2cpp_object_new "{}"\n#define BNM_IL2CPP_API_il2cpp_value_box "{}"\n#define BNM_IL2CPP_API_il2cpp_array_new "{}"\n#define BNM_IL2CPP_API_il2cpp_field_static_get_value "{}"\n#define BNM_IL2CPP_API_il2cpp_field_static_set_value "{}"\n#define BNM_IL2CPP_API_il2cpp_string_new "{}"\n#define BNM_IL2CPP_API_il2cpp_resolve_icall "{}"\n#define BNM_IL2CPP_API_il2cpp_runtime_invoke "{}"\n#define BNM_IL2CPP_API_il2cpp_domain_get "{}"\n#define BNM_IL2CPP_API_il2cpp_thread_current "{}"\n#define BNM_IL2CPP_API_il2cpp_thread_attach "{}"\n#define BNM_IL2CPP_API_il2cpp_thread_detach "{}"\n#define BNM_IL2CPP_API_il2cpp_alloc "{}"\n#define BNM_IL2CPP_API_il2cpp_free "{}"\n"""

    sheesh = sheesh.format( data["il2cpp_init"], data["il2cpp_class_from_il2cpp_type"], data["il2cpp_array_new_specific"], data["il2cpp_class_from_type"], data["il2cpp_type_get_class_or_element_class"], data["il2cpp_domain_get_assemblies"], data["il2cpp_domain_assembly_open"], data["il2cpp_image_get_class"], data["il2cpp_get_corlib"], data["il2cpp_class_from_name"], data["il2cpp_assembly_get_image"], data["il2cpp_method_get_param_name"], data["il2cpp_array_class_get"], data["il2cpp_type_get_object"], data["il2cpp_object_new"], data["il2cpp_value_box"], data["il2cpp_array_new"], data["il2cpp_field_static_get_value"], data["il2cpp_field_static_set_value"], data["il2cpp_string_new"], data["il2cpp_resolve_icall"], data["il2cpp_runtime_invoke"], data["il2cpp_domain_get"], data["il2cpp_thread_current"], data["il2cpp_thread_attach"], data["il2cpp_thread_detach"], data["il2cpp_alloc"], data["il2cpp_free"] )
        
    with open("Il2CppMethodNames.hpp", "w") as f:
        f.write(sheesh)

def DumpToDumperFile(data: dict):
    txt = "#pragma once\n\n"
    for key in data.keys():
        txt += "#define symbol_{} \"{}\"\n".format(key, data[key])

    with open("Il2Cpp-Headers.hpp", "w") as f:
        f.write(txt)

goods = GetCodeLines(goodRefs)
bads = GetCodeLines(badRefs)

il2cpp_init : str = "il2cpp_init"

if len(bads) == len(goods) + 1:
    il2cpp_init = bads[0]
    bads.remove(bads[0])

symbolDict["il2cpp_init"] = il2cpp_init

for i in range(len(goods)):
    symbolDict[goods[i]] = bads[i]

with open("SymbolMap.json", "w") as f:
    json.dump(symbolDict, f, indent = 2)

# not really needed but are kinda useful :)
DumpToBNMFile(symbolDict)
DumpToDumperFile(symbolDict)