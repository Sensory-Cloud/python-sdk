import os
import sys


python_proto_root = "src/sensory_cloud/generated/"

def replace_imports(path, packages):
    with open(path, "r") as f:
        filedata = f.read()
    
    for package in packages:
        filedata = filedata.replace(f"from {package}", f"from sensory_cloud.generated.{package}")

    with open(path, "w") as f:
        f.write(filedata)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("A proto file directory path must be passed as an argument!  Exiting script.")
        quit()

    proto_root = sys.argv[1]

    if not proto_root.endswith("/"):
        proto_root = proto_root + "/"

    proto_paths = [
        os.path.join(root, _file) 
        for root, _, files in os.walk(proto_root)
        for _file in files
        if _file.endswith(".proto")
    ]

    for path in proto_paths:
        cmd = f"python3 -m grpc_tools.protoc -I {proto_root} --python_out={python_proto_root} --grpc_python_out={python_proto_root} {path}"
        os.system(cmd)
    
    proto_python_paths = [
        {
            "abs_path": os.path.join(root, _file),
            "rel_path": os.path.split(os.path.join(root, _file).replace(python_proto_root, ""))[0].replace("/", ".")
        }
        for root, _, files in os.walk(python_proto_root)
        for _file in files
        if _file.endswith(".py") and _file != "__init__.py"
    ]

    python_proto_files = []
    packages = []
    for root, _, files in os.walk(python_proto_root):
        for _file in files:
            if _file.endswith(".py") and _file != "__init__.py":
                python_proto_file = os.path.join(root, _file)
                python_proto_files.append(python_proto_file)
                package = os.path.split(python_proto_file.replace(python_proto_root, ""))[0].replace("/", ".")
                if package not in packages:
                    packages.append(package)

    for path in python_proto_files:
        replace_imports(path, packages)