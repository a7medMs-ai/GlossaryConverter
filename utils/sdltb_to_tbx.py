import os
import subprocess

def convert_sdltb_to_tbx(sdltb_path, output_path=None, jar_path="java_bridge/libs/sdltb_converter.jar"):
    """
    Converts an SDLTB (.mdb) file to TBX using a Java JAR tool.
    This assumes a Java converter exists and is packaged as a .jar in the project.
    """
    if not os.path.exists(sdltb_path):
        raise FileNotFoundError("SDLTB file not found.")

    if output_path is None:
        output_path = os.path.splitext(sdltb_path)[0] + ".tbx"

    # Construct Java command
    cmd = [
        "java",
        "-jar", jar_path,
        sdltb_path,
        output_path
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print("[INFO] Java conversion output:")
        print(result.stdout)
        return output_path
    except subprocess.CalledProcessError as e:
        print("[ERROR] Java conversion failed:")
        print(e.stderr)
        raise RuntimeError("Failed to convert SDLTB to TBX.")
