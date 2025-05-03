import os
import shutil

def is_java_available():
    """
    Checks if 'java' command is available in the system.
    """
    return shutil.which("java") is not None

def convert_sdltb_to_tbx(sdltb_path, output_path=None):
    """
    Converts SDLTB (.mdb) file to TBX using a Java JAR wrapped by run_jar().
    """
    if not os.path.exists(sdltb_path):
        raise FileNotFoundError("SDLTB file not found.")

    if not is_java_available():
        raise EnvironmentError("Java runtime not available. Please install Java or run locally.")
