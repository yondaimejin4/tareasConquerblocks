# Memoria tecnica PFM — ALPRO TECHNOLOGY SPA

**Proyecto Final del Master en Desarrollo Full Stack**

---

## 1. Definicion del problema

### Contexto

Las pymes y medianas empresas del sector servicios suelen gestionar la captacion comercial mediante canales dispersos (WhatsApp, correo, llamadas) sin un registro centralizado. Esto genera perdida de oportunidades, respuestas tardias y dificultad para medir demanda por tipo de servicio.

### Carencias detectadas

- Ausencia de un catalogo digital actualizado de servicios.
- Formularios de contacto no integrados con una base de datos consultable.
- Dependencia de hojas de calculo para seguimiento de leads.
- Poca visibilidad de metricas basicas (solicitudes recibidas, servicios activos).

### Impacto

Retrasos en la respuesta comercial, imagen poco profesional y mayor carga administrativa para equipos reducidos.

### Solucion propuesta

Plataforma web **ALPRO TECHNOLOGY SPA** con:

- Landing corporativa en **Django** (templates) y **React** (SPA).
- API REST para servicios y contacto.
- Panel **Django Admin** para administrar catalogo y leads.

---

## 2. Reflexion: aportacion y eficiencia

| Antes | Despues con la herramienta |
|-------|----------------------------|
| Consultas por mensajes sueltos | Formulario estructurado con validacion |
| Catalogo en PDF o redes | Servicios dinamicos desde base de datos |
| Sin historial ordenado | Leads con fecha en admin |
| Dos personas repiten la misma info | Un solo punto de verdad en la API |

**Beneficios:** menor tiempo de respuesta, estandarizacion de datos del cliente, mejor trazabilidad y base para futuras automatizaciones (CRM, email transaccional).

---

## 3. Tecnologias utilizadas y justificacion

| Tecnologia | Uso | Justificacion |
|------------|-----|---------------|
| **Django 6** | Backend principal, ORM, admin, auth | Framework obligatorio del master; madurez y seguridad integrada |
| **Django REST Framework** | API JSON | Integracion limpia con React |
| **SQLite** (dev) / **PostgreSQL** (prod) | Persistencia | Simplicidad local; escalabilidad en nube |
| **React + Vite** | Frontend SPA | Requisito PFM; consumo real de API |
| **django-cors-headers** | CORS | Comunicacion segura entre origenes en desarrollo y produccion |
| **WhiteNoise + Gunicorn** | Static y servidor WSGI | Despliegue en PaaS |
| **Git / GitHub** | Control de versiones | Entrega y trazabilidad del trabajo |

---

## 4. Tipos de usuarios

| Rol | Acciones |
|-----|----------|
| **Visitante** | Ver el catalogo en React, enviar el formulario de consultoria |
| **Cliente** | Registrarse o usar una cuenta creada por el admin, iniciar sesion en `/portal/login`, crear solicitudes, enviar aportes e ideas y consultar estado, pago y comentarios |
| **Administrador** | Entrar en `/admin/`, crear usuarios cliente, revisar solicitudes y aportes, actualizar estado del proyecto, comentario visible y estado de pago |

El portal y el admin usan sesiones distintas para que una pestaña de administracion no contamine las solicitudes del cliente.

---

## 5. Casos de uso

### CU-01: Consultar servicios (Visitante — React)

1. El visitante abre la SPA.
2. React llama `GET /api/services/` y `GET /api/services/featured/`.
3. Se muestran tarjetas y detalle expandible.

**Exito:** lista renderizada. **Error:** backend caido → mensaje de error en pantalla.

### CU-02: Enviar solicitud de contacto (Visitante)

1. Completa nombre, email, mensaje (empresa opcional).
2. React envia `POST /api/contact/`.
3. Serializer valida; se crea `ContactLead`.

**Exito:** HTTP 201 y mensaje de confirmacion. **Error:** email invalido → 400; red → mensaje al usuario.

### CU-03: Seguimiento de una solicitud (Cliente)

1. Inicia sesion en `/portal/login`.
2. Crea una solicitud y, en el detalle, agrega un aporte o una imagen.
3. El registro queda asociado solo a su usuario.

**Exito:** la solicitud aparece en "Mis solicitudes". **Error:** sin sesion de portal → 403; solicitud de otro usuario → 404.

### CU-04: Actualizar estado y pago (Administrador)

1. Abre la solicitud en Django Admin.
2. Cambia el estado del proyecto, escribe el comentario para el cliente y ajusta el estado de pago.
3. El cliente recarga el detalle y ve esos campos. Las notas internas no se exponen en la API.

### CU-05: Actualizar catalogo (Administrador)

1. Crea o edita `Service` y marca `is_featured`.
2. Los cambios aparecen en la API y en React al recargar.

---

## 6. Seguridad y proteccion de datos

| Medida | Implementacion |
|--------|----------------|
| Autenticacion | `django.contrib.auth` en el admin; cookie `portal_sessionid` en el portal |
| Aislamiento | Cada cliente solo lee y escribe sus `ContactLead` |
| Validacion | Serializers DRF en contacto, registro, solicitudes y aportes |
| CSRF | Token en el portal y en el admin; el formulario publico no usa la sesion de staff |
| XSS | Templates Django con auto-escape; React escapa por defecto |
| Contrasenas | Hash PBKDF2 (Django) |
| Secretos | `SECRET_KEY` y flags por variables de entorno |
| HTTPS | Proporcionado por el proveedor cloud en produccion |
| CORS | Lista blanca de origenes (`CORS_ALLOWED_ORIGINS`) |
| Backups | Recomendado backup automatico de PostgreSQL en Render |

---

## 7. Arquitectura

```
[Visitante / Cliente] → [React SPA] ──HTTP JSON──→ [Django + DRF] → [PostgreSQL/SQLite]
                              ↑                          ↓
                         [Vite build]              [Django Admin]
                         portal_sessionid          sessionid
```

---

## 8. Evidencias para el PDF

1. Captura landing Django (`/`)
2. Captura React con servicios y destacados
3. Captura envio exitoso del formulario
4. Captura admin con `Service` y `ContactLead`
5. Salida de `python manage.py test core`
6. Diagrama de arquitectura (seccion 7)

---

## 9. Despliegue

Ver `docs/DEPLOY.md`. Tras desplegar, incluir en la entrega:

- URL publica del backend y del frontend
- Enlace al repositorio GitHub
- Vídeo de 5 minutos con demo de integracion React ↔ API
