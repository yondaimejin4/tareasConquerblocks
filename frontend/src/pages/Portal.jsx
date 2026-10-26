import { useEffect, useState } from "react";
import { Link, Navigate, Route, Routes, useNavigate, useParams } from "react-router-dom";
import { API_BASE_URL, apiFetch, ensureCsrf } from "../api/client";
import "../Portal.css";

function PortalShell({ user, onLogout, children }) {
  const welcomeName = user?.username?.trim() || "cliente";

  return (
    <div className="portal-page">
      <header className="portal-topbar">
        <div className="portal-topbar-brand">
          <Link to="/" className="brand">
            ALPRO TECHNOLOGY SPA
          </Link>
          <p className="portal-welcome">
            Bienvenido, <strong>{welcomeName}</strong>
          </p>
        </div>
        <nav className="portal-nav">
          <Link to="/portal/solicitudes">Mis solicitudes</Link>
          {user?.is_staff && (
            <a href={`${API_BASE_URL}/admin/`} target="_blank" rel="noreferrer">
              Panel admin
            </a>
          )}
          <button type="button" className="link-btn" onClick={onLogout}>
            Cerrar sesion
          </button>
        </nav>
      </header>
      {children}
    </div>
  );
}

function PortalLogin({ onAuth }) {
  const navigate = useNavigate();
  const [form, setForm] = useState({ username: "", password: "" });
  const [error, setError] = useState("");

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError("");
    await ensureCsrf();
    const { response, data } = await apiFetch("/api/auth/login/", {
      method: "POST",
      body: JSON.stringify(form),
    });
    if (!response.ok) {
      setError(data?.detail || "No se pudo iniciar sesion.");
      return;
    }
    onAuth(data.user);
    navigate("/portal/solicitudes");
  };

  return (
    <div className="portal-auth">
      <h1>Area cliente</h1>
      <p className="section-intro">Inicia sesion para ver el estado de tus solicitudes.</p>
      <form className="form" onSubmit={handleSubmit}>
        <input
          placeholder="Usuario"
          value={form.username}
          onChange={(e) => setForm({ ...form, username: e.target.value })}
          required
        />
        <input
          type="password"
          placeholder="Contrasena"
          value={form.password}
          onChange={(e) => setForm({ ...form, password: e.target.value })}
          required
        />
        <button type="submit" className="btn btn-primary">
          Entrar
        </button>
      </form>
      {error && <p className="error">{error}</p>}
      <p className="muted">
        ¿Sin cuenta? <Link to="/portal/registro">Registrate aqui</Link>
      </p>
      <p className="muted">
        <Link to="/">Volver al sitio</Link>
      </p>
    </div>
  );
}

function PortalRegister({ onAuth }) {
  const navigate = useNavigate();
  const [form, setForm] = useState({
    username: "",
    email: "",
    password: "",
    first_name: "",
    last_name: "",
  });
  const [error, setError] = useState("");

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError("");
    await ensureCsrf();
    const { response, data } = await apiFetch("/api/auth/register/", {
      method: "POST",
      body: JSON.stringify(form),
    });
    if (!response.ok) {
      const msg =
        typeof data === "object"
          ? Object.values(data).flat().join(" ")
          : "No se pudo crear la cuenta.";
      setError(msg);
      return;
    }
    onAuth(data.user);
    navigate("/portal/solicitudes");
  };

  return (
    <div className="portal-auth">
      <h1>Crear cuenta</h1>
      <form className="form" onSubmit={handleSubmit}>
        <input
          placeholder="Usuario"
          value={form.username}
          onChange={(e) => setForm({ ...form, username: e.target.value })}
          required
        />
        <input
          type="email"
          placeholder="Correo"
          value={form.email}
          onChange={(e) => setForm({ ...form, email: e.target.value })}
          required
        />
        <input
          placeholder="Nombre (opcional)"
          value={form.first_name}
          onChange={(e) => setForm({ ...form, first_name: e.target.value })}
        />
        <input
          placeholder="Apellido (opcional)"
          value={form.last_name}
          onChange={(e) => setForm({ ...form, last_name: e.target.value })}
        />
        <input
          type="password"
          placeholder="Contrasena (min. 8)"
          value={form.password}
          onChange={(e) => setForm({ ...form, password: e.target.value })}
          required
          minLength={8}
        />
        <button type="submit" className="btn btn-primary">
          Registrarme
        </button>
      </form>
      {error && <p className="error">{error}</p>}
      <p className="muted">
        ¿Ya tienes cuenta? <Link to="/portal/login">Inicia sesion</Link>
      </p>
    </div>
  );
}

function PortalDashboard({ user }) {
  const [requests, setRequests] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [newRequest, setNewRequest] = useState({ company: "", message: "" });
  const [feedback, setFeedback] = useState("");

  const load = async () => {
    setLoading(true);
    const { response, data } = await apiFetch("/api/my-requests/");
    if (response.ok) {
      setRequests(data);
    }
    setLoading(false);
  };

  useEffect(() => {
    load();
  }, []);

  const handleCreate = async (event) => {
    event.preventDefault();
    setFeedback("");
    await ensureCsrf();
    const { response, data } = await apiFetch("/api/my-requests/", {
      method: "POST",
      body: JSON.stringify(newRequest),
    });
    if (!response.ok) {
      setFeedback("No se pudo crear la solicitud.");
      return;
    }
    setNewRequest({ company: "", message: "" });
    setShowForm(false);
    setFeedback("Solicitud creada correctamente.");
    await load();
  };

  return (
    <div className="portal-content">
      <p className="portal-welcome-banner">
        Hola <strong>{user?.username}</strong>, aqui puedes ver y gestionar tus solicitudes.
      </p>
      <div className="portal-header-row">
        <h1>Mis solicitudes</h1>
        <button type="button" className="btn btn-primary" onClick={() => setShowForm(!showForm)}>
          {showForm ? "Cancelar" : "Nueva solicitud"}
        </button>
      </div>
      {feedback && <p className="feedback">{feedback}</p>}
      {showForm && (
        <form className="form portal-form-block" onSubmit={handleCreate}>
          <input
            placeholder="Empresa (opcional)"
            value={newRequest.company}
            onChange={(e) => setNewRequest({ ...newRequest, company: e.target.value })}
          />
          <textarea
            placeholder="Describe tu proyecto..."
            value={newRequest.message}
            onChange={(e) => setNewRequest({ ...newRequest, message: e.target.value })}
            required
            rows={4}
          />
          <button type="submit" className="btn btn-primary">
            Enviar solicitud
          </button>
        </form>
      )}
      {loading && <p className="muted">Cargando...</p>}
      {!loading && requests.length === 0 && (
        <p className="muted">Aun no tienes solicitudes. Crea la primera con el boton de arriba.</p>
      )}
      <div className="grid">
        {requests.map((item) => (
          <article key={item.id} className="card">
            <span className="badge">{item.status_label}</span>
            <h3>Solicitud #{item.id}</h3>
            <p>{item.message.slice(0, 120)}{item.message.length > 120 ? "..." : ""}</p>
            <p className="meta-line">
              Pago: <strong>{item.payment_status_label}</strong>
            </p>
            {item.pending_summary && (
              <p className="pending-alert">{item.pending_summary}</p>
            )}
            {item.team_comment && (
              <p className="team-comment-preview">{item.team_comment.slice(0, 100)}
                {item.team_comment.length > 100 ? "..." : ""}
              </p>
            )}
            <Link to={`/portal/solicitudes/${item.id}`} className="link-btn">
              Ver detalle →
            </Link>
          </article>
        ))}
      </div>
    </div>
  );
}

function PortalRequestDetail() {
  const { id } = useParams();
  const [request, setRequest] = useState(null);
  const [error, setError] = useState("");
  const [contrib, setContrib] = useState({ message: "", attachment: null });
  const [sending, setSending] = useState(false);

  const load = async () => {
    const { response, data } = await apiFetch(`/api/my-requests/${id}/`);
    if (!response.ok) {
      setError("Solicitud no encontrada.");
      return;
    }
    setRequest(data);
  };

  useEffect(() => {
    load();
  }, [id]);

  const handleContribution = async (event) => {
    event.preventDefault();
    setSending(true);
    await ensureCsrf();
    const body = new FormData();
    body.append("message", contrib.message);
    if (contrib.attachment) {
      body.append("attachment", contrib.attachment);
    }
    const { response } = await apiFetch(`/api/my-requests/${id}/contributions/`, {
      method: "POST",
      body,
    });
    setSending(false);
    if (!response.ok) {
      setError("No se pudo enviar el aporte.");
      return;
    }
    setContrib({ message: "", attachment: null });
    setError("");
    await load();
  };

  if (!request && !error) {
    return <p className="muted portal-content">Cargando detalle...</p>;
  }

  if (error && !request) {
    return (
      <div className="portal-content">
        <p className="error">{error}</p>
        <Link to="/portal/solicitudes">Volver</Link>
      </div>
    );
  }

  return (
    <div className="portal-content">
      <Link to="/portal/solicitudes" className="link-btn">
        ← Volver a mis solicitudes
      </Link>
      <h1>Solicitud #{request.id}</h1>
      <div className="detail-grid">
        <article className="card portal-status-card">
          <h3>Estado del proyecto</h3>
          <p className="status-value">
            <strong>{request.status_label}</strong>
          </p>
          <p className="muted">
            Ultima actualizacion: {new Date(request.updated_at).toLocaleString("es-CL")}
          </p>
          <div className="team-comment-box">
            <h4>Comentario del equipo sobre tu proyecto</h4>
            {request.team_comment ? (
              <p>{request.team_comment}</p>
            ) : (
              <p className="muted">
                Aun no hay comentarios. El equipo los publicara cuando revise tu solicitud.
              </p>
            )}
          </div>
        </article>
        <article className="card portal-status-card">
          <h3>Estado de pago</h3>
          <p className="status-value">
            <strong>{request.payment_status_label}</strong>
          </p>
          {request.pending_summary ? (
            <p className="pending-alert">{request.pending_summary}</p>
          ) : (
            <p className="muted">Sin detalle de pago pendiente.</p>
          )}
        </article>
      </div>
      <article className="card">
        <h3>Descripcion</h3>
        <p>{request.message}</p>
        {request.company && <p className="muted">Empresa: {request.company}</p>}
      </article>
      <section>
        <h2>Tus aportes e ideas</h2>
        <p className="section-intro">
          Agrega comentarios o una imagen de referencia para tu proyecto.
        </p>
        {request.contributions?.length > 0 && (
          <ul className="contrib-list">
            {request.contributions.map((item) => (
              <li key={item.id} className="card">
                <p>{item.message}</p>
                {item.attachment_url && (
                  <a href={item.attachment_url} target="_blank" rel="noreferrer">
                    Ver imagen adjunta
                  </a>
                )}
                <p className="muted">{new Date(item.created_at).toLocaleString("es-CL")}</p>
              </li>
            ))}
          </ul>
        )}
        <form className="form portal-form-block" onSubmit={handleContribution}>
          <textarea
            placeholder="Escribe una idea, cambio o comentario..."
            value={contrib.message}
            onChange={(e) => setContrib({ ...contrib, message: e.target.value })}
            required
            rows={3}
          />
          <input
            type="file"
            accept="image/*"
            onChange={(e) =>
              setContrib({ ...contrib, attachment: e.target.files?.[0] || null })
            }
          />
          <button type="submit" className="btn btn-primary" disabled={sending}>
            {sending ? "Enviando..." : "Agregar aporte"}
          </button>
        </form>
        {error && <p className="error">{error}</p>}
      </section>
    </div>
  );
}

export default function Portal() {
  const [user, setUser] = useState(null);
  const [checking, setChecking] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const init = async () => {
      try {
        await ensureCsrf();
        const { response, data } = await apiFetch("/api/auth/me/");
        if (response.ok && data?.authenticated) {
          setUser({ ...data.user, is_staff: data.is_staff });
        }
      } catch {
        /* backend apagado: mostrar login igualmente */
      } finally {
        setChecking(false);
      }
    };
    init();
  }, []);

  const handleLogout = async () => {
    await ensureCsrf();
    await apiFetch("/api/auth/logout/", { method: "POST" });
    setUser(null);
    navigate("/portal/login");
  };

  if (checking) {
    return (
      <div className="portal-page">
        <p className="muted portal-content">Cargando...</p>
      </div>
    );
  }

  const RequireAuth = ({ children }) =>
    user ? (
      <PortalShell user={user} onLogout={handleLogout}>
        {children}
      </PortalShell>
    ) : (
      <Navigate to="/portal/login" replace />
    );

  return (
    <Routes>
      <Route
        path="login"
        element={
          user ? (
            <Navigate to="/portal/solicitudes" replace />
          ) : (
            <div className="portal-page">
              <PortalLogin onAuth={setUser} />
            </div>
          )
        }
      />
      <Route
        path="registro"
        element={
          user ? (
            <Navigate to="/portal/solicitudes" replace />
          ) : (
            <div className="portal-page">
              <PortalRegister onAuth={setUser} />
            </div>
          )
        }
      />
      <Route
        path="solicitudes"
        element={
          <RequireAuth>
            <PortalDashboard user={user} />
          </RequireAuth>
        }
      />
      <Route
        path="solicitudes/:id"
        element={
          <RequireAuth>
            <PortalRequestDetail />
          </RequireAuth>
        }
      />
      <Route path="*" element={<Navigate to="/portal/login" replace />} />
    </Routes>
  );
}
