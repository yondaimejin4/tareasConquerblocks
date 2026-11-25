# Inicio rapido — ALPRO PFM

## Un solo comando

Desde la carpeta del proyecto:

```bash
source .venv/bin/activate
./scripts/dev.sh
```

## Abrir en el navegador

**http://127.0.0.1:8000/**

No uses el puerto 5173 salvo que estes desarrollando con `npm run dev`.

## Credenciales

| Rol | URL | Usuario | Clave |
|-----|-----|---------|-------|
| Admin | http://127.0.0.1:8000/admin/ | admin | Admin123 |
| Cliente | http://127.0.0.1:8000/portal/login | (registro o cuenta creada en admin) | — |

### Crear cliente desde el admin

1. Entra en http://127.0.0.1:8000/admin/ con `admin` / `Admin123`
2. **Usuarios** → **Añadir usuario**: usuario, correo, nombre (opcional) y contraseña
3. Al abrir un usuario veras sus **solicitudes/leads** en la misma pagina (o el enlace **Solicitudes** en la lista)
4. En **Solicitudes de clientes** tambien puedes asignar el campo **Usuario** a una solicitud sin cuenta
5. El cliente inicia sesion en `/portal/login` con el usuario y contraseña que definiste

**Admin y portal en pestañas distintas:** el panel `/admin/` y el portal usan sesiones separadas. Puedes estar logueado como admin y, en otra pestaña, entrar al portal con la cuenta cliente sin mezclar solicitudes.

### Gestionar solicitudes del cliente en admin

En **Solicitudes de clientes** ves el mensaje y puedes cambiar el **estado**. Las notas internas no las ve el cliente.

Tras guardar, el cliente ve los cambios en `/portal/solicitudes` (recarga el detalle si ya lo tenia abierto).

## Si algo falla

```bash
./scripts/verificar.sh
```

Debe decir: **Todo correcto. Usa SOLO: http://127.0.0.1:8000/**

Recarga el navegador con **Cmd+Shift+R** (borrar cache).
