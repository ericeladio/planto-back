# Docker - Planto Backend

## Comandos Docker

### 1. Build - Construir la imagen

```bash
docker build -t planto-backend .
```

**Que hace:** Crea una imagen Docker con todo lo necesario para correr el backend.

- `docker build` - Construye la imagen
- `-t planto-backend` - Nombre de la imagen
- `.` - Contexto actual (donde esta el Dockerfile)

**Por que se necesita:** Docker no puede correr tu codigo directamente. Necesita "empaquetar" Python, las dependencias de `requirements.txt`, y tu codigo `app/` en una imagen replicable. Sin esto, tendrias que instalar todo manualmente en cada maquina.

---

### 2. Run - Ejecutar el contenedor

```bash
docker run -p 8000:8000 --env-file .env planto-backend
```

**Que hace:** Saca una instancia (contenedor) de la imagen y la ejecuta.

- `docker run` - Ejecuta un contenedor
- `-p 8000:8000` - Mapea puerto 8000 del host al 8000 del contenedor
- `--env-file .env` - Pasa las variables de entorno (DATABASE_URL, JWT_SECRET, etc.)
- `planto-backend` - Usa la imagen que construiste

**Por que se necesita:** La imagen es solo una plantilla. El contenedor es la instancia corriendo. Sin `-p`, no podrias acceder al API desde afuera. Sin `--env-file`, el backend no tendria acceso a la DB ni secrets.

---

## Resumen

| Comando | Que crea | Para que |
|---------|----------|----------|
| `build` | Imagen (plantilla) | Empaquetar codigo + deps |
| `run` | Contenedor (instancia) | Ejecutar el API |

Primero construyes, despues ejecutas. No puedes ejecutar sin construir primero.
