import subprocess
import datetime
import sys
import os
import shutil

# ------------------------------------------------------
# Ejecutar comandos con control de errores
# ------------------------------------------------------
def run(cmd, msg_ok=None):
    result = subprocess.run(cmd, shell=True, text=True)
    if result.returncode != 0:
        print(f"\n❌  ERROR ejecutando: {cmd}")
        sys.exit(1)
    if msg_ok:
        print(f"   ✔️  {msg_ok}")

# ------------------------------------------------------
# Crear backup del proyecto completo
# ------------------------------------------------------
def hacer_backup():
    origen = os.path.abspath(os.getcwd())
    destino_base = r"C:\BACKUPS_JAREK\Backup-FirstPro"

    # Crear carpeta si no existe
    os.makedirs(destino_base, exist_ok=True)

    # Carpeta con fecha y hora
    fecha = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    destino = os.path.join(destino_base, f"Backup_{fecha}")

    try:
        print("\n🗂️  Creando backup del proyecto…")
        shutil.copytree(origen, destino)
        print(f"   ✔️  Backup creado en:\n       {destino}")
    except Exception as e:
        print(f"❌  Error creando backup: {e}")
        sys.exit(1)

# ------------------------------------------------------
# PROCESO PRINCIPAL
# ------------------------------------------------------
if __name__ == "__main__":
    mensaje = f"Auto-commit {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    print("\n====================================================")
    print(" 🔥  GIT PUSH + BACKUP – Fénix Engine v3 ")
    print("====================================================\n")

    print("📌  Inicializando proceso...\n")

    # 1) ADD
    print("📂  Añadiendo archivos…")
    run("git add .", "Archivos añadidos al stage")

    # 2) COMMIT
    print("\n📝  Creando commit…")
    run(f'git commit -m "{mensaje}"', "Commit creado")

    # 3) PUSH
    print("\n🚀  Subiendo cambios al repositorio remoto…")
    run("git push", "Push completado")

    # 4) BACKUP
    hacer_backup()

    print("\n✨  Todo ok, Jarek. Repo actualizado + Backup asegurado.\n")
