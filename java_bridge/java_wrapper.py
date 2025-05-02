import os
from GlossaryConverter.java_bridge.java_wrapper import run_jar

def convert_sdltb_to_tbx(sdltb_path, output_path=None):
    """
    Converts SDLTB (.mdb) file to TBX using a Java JAR wrapped by run_jar().
    """
    if not os.path.exists(sdltb_path):
        raise FileNotFoundError("SDLTB file not found.")

    if output_path is None:
        output_path = os.path.splitext(sdltb_path)[0] + ".tbx"

    output = run_jar("jackcess-3.0.1.jar", [sdltb_path, output_path])
    print("[JAVA OUTPUT]:", output)
    return output_path
