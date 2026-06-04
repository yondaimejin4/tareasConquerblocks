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
| **Visitante** | Ver servicios (web Django y React), enviar formulario de contacto |
| **Administrador** | Login en `/admin/`, CRUD de `Service` y `ContactLead`, marcar servicios destacados |
| **Staff (login web)** | Acceso a `/accounts/login/` para flujos de autenticacion Django (panel admin) |

No se implementa registro publico de usuarios finales para mantener el MVP acotado al alcance del PFM.

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

### CU-03: Gestionar leads (Administrador)

1. Inicia sesion en `/admin/`.
2. Revisa listado de `ContactLead` con busqueda y jerarquia por fecha.
3. Contacta al cliente por canal externo.

### CU-04: Actualizar catalogo (Administrador)

1. Crea o edita `Service`, marca `is_featured`.
2. Los cambios aparecen al instante en API y en React al recargar.

---

## 6. Seguridad y proteccion de datos

| Medida | Implementacion |
|--------|----------------|
| Autenticacion | `django.contrib.auth` + admin protegido |
| Validacion | Serializers DRF en contacto |
| CSRF | Middleware activo en vistas Django con formularios |
| XSS | Templates Django con auto-escape; React escapa por defecto |
| Contrasenas | Hash PBKDF2 (Django) |
| Secretos | `SECRET_KEY` y flags por variables de entorno |
| HTTPS | Proporcionado por el proveedor cloud en produccion |
| CORS | Lista blanca de origenes (`CORS_ALLOWED_ORIGINS`) |
| Backups | Recomendado backup automatico de PostgreSQL en Render |

---

## 7. Arquitectura

```
[Visitante] → [React SPA] ──HTTP JSON──→ [Django + DRF] → [PostgreSQL/SQLite]
                      ↑                        ↓
                 [Vite build]            [Django Admin]
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
