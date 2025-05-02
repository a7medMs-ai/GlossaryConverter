import subprocess
import os

def run_jar(jar_name, args):
    """
    Runs a JAR file with given arguments.
    The JAR must be located inside java_bridge/libs/
    """
    jar_path = os.path.join(os.path.dirname(__file__), "libs", jar_name)
    if not os.path.exists(jar_path):
        raise FileNotFoundError(f"JAR not found: {jar_path}")

    cmd = ["java", "-jar", jar_path] + args
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        raise RuntimeError(f"[JAVA ERROR] {result.stderr.strip()}")

    return result.stdout.strip()
