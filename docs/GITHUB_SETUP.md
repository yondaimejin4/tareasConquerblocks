# Subir el proyecto a GitHub

El repositorio local ya tiene **3 commits** en la rama `main`. Solo falta crear el remoto en GitHub y hacer push.

## Pasos

1. Entra en [github.com/new](https://github.com/new) y crea un repositorio **publico**:
   - Nombre sugerido: `alpro-pfm-fullstack`
   - Sin README ni `.gitignore` (ya existen en el proyecto)

2. En la terminal, desde la carpeta del proyecto:

```bash
cd "/Users/alpro/Documents/Tareas ConquerBlocks/Proyecto Final Master Full Stack"
git remote add origin https://github.com/TU_USUARIO/alpro-pfm-fullstack.git
git branch -M main
git push -u origin main
```

Sustituye `TU_USUARIO` por tu usuario de GitHub.

3. Comprueba en GitHub que ves los 3 commits y la estructura `backend/`, `frontend/`, `docs/`.

## SSH (alternativa)

```bash
git remote add origin git@github.com:TU_USUARIO/alpro-pfm-fullstack.git
git push -u origin main
```
