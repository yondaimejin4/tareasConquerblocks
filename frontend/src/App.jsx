import { useEffect, useState } from "react";
import "./App.css";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

const BENEFITS = [
  {
    title: "Implementacion rapida",
    text: "MVP funcional en semanas, no meses, con entregas iterativas visibles.",
  },
  {
    title: "Enfoque en negocio",
    text: "Cada funcionalidad responde a un proceso real de tu empresa.",
  },
  {
    title: "Soporte continuo",
    text: "Acompanamiento post-lanzamiento, mantenimiento y mejoras evolutivas.",
  },
];

const PROCESS_STEPS = [
  "Diagnostico y definicion de objetivos",
  "Diseno de arquitectura y plan de trabajo",
  "Desarrollo e integracion con tu operacion",
  "Pruebas, despliegue y capacitacion",
];

function App() {
  const [services, setServices] = useState([]);
  const [featured, setFeatured] = useState([]);
  const [status, setStatus] = useState("loading");
  const [expandedId, setExpandedId] = useState(null);
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    company: "",
    message: "",
  });
  const [contactMessage, setContactMessage] = useState("");
  const [contactError, setContactError] = useState(false);

  useEffect(() => {
    const loadData = async () => {
      try {
        const [allRes, featuredRes] = await Promise.all([
          fetch(`${API_BASE_URL}/api/services/`),
          fetch(`${API_BASE_URL}/api/services/featured/`),
        ]);

        if (!allRes.ok || !featuredRes.ok) {
          throw new Error("API error");
        }

        const allData = await allRes.json();
        const featuredData = await featuredRes.json();
        setServices(allData);
        setFeatured(featuredData);
        setStatus("ready");
      } catch {
        setStatus("error");
      }
    };

    loadData();
  }, []);

  const handleChange = (event) => {
    const { name, value } = event.target;
    setFormData((previous) => ({ ...previous, [name]: value }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setContactMessage("Enviando...");
    setContactError(false);

    try {
      const response = await fetch(`${API_BASE_URL}/api/contact/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });

      const data = await response.json();
      if (!response.ok) {
        throw new Error("Error al enviar solicitud");
      }

      setContactMessage(data.message);
      setFormData({ name: "", email: "", company: "", message: "" });
    } catch {
      setContactError(true);
      setContactMessage("No se pudo enviar la solicitud. Revisa los datos e intenta de nuevo.");
    }
  };

  const toggleDetails = (id) => {
    setExpandedId((current) => (current === id ? null : id));
  };

  return (
    <div className="page">
      <header className="topbar">
        <p className="brand">ALPRO TECHNOLOGY SPA</p>
        <nav className="nav">
          <a href="#servicios">Servicios</a>
          <a href="#proceso">Proceso</a>
          <a href="#contacto">Contacto</a>
        </nav>
      </header>

      <section className="hero">
        <p className="eyebrow">Innovacion digital para pymes y medianas empresas</p>
        <h1>Tecnologia que impulsa tu negocio con datos reales y procesos ordenados</h1>
        <p className="hero-text">
          Desarrollo web, automatizacion y consultoria tecnologica. Esta aplicacion integra
          React con Django para mostrar servicios y captar solicitudes comerciales en tiempo real.
        </p>
        <div className="hero-actions">
          <a className="btn btn-primary" href="#contacto">
            Solicitar consultoria
          </a>
          <a className="btn btn-secondary" href="#servicios">
            Ver servicios
          </a>
        </div>
      </section>

      <section className="stats">
        <article>
          <strong>{services.length || "—"}</strong>
          <span>Servicios activos</span>
        </article>
        <article>
          <strong>{featured.length || "—"}</strong>
          <span>Destacados</span>
        </article>
        <article>
          <strong>24/7</strong>
          <span>Soporte acordado</span>
        </article>
        <article>
          <strong>100%</strong>
          <span>Integracion API Django</span>
        </article>
      </section>

      <section id="destacados">
        <h2>Servicios destacados</h2>
        <p className="section-intro">
          Datos obtenidos desde <code>GET /api/services/featured/</code>
        </p>
        {status === "loading" && <p className="muted">Cargando destacados...</p>}
        {status === "error" && (
          <p className="error">No se pudo conectar con el backend Django.</p>
        )}
        {status === "ready" && featured.length === 0 && (
          <p className="muted">No hay servicios destacados. Cargalos desde el admin o con seed_demo.</p>
        )}
        {status === "ready" && featured.length > 0 && (
          <div className="grid grid-featured">
            {featured.map((service) => (
              <article key={service.id} className="card card-featured">
                <span className="badge">Destacado</span>
                <h3>{service.title}</h3>
                <p>{service.short_description}</p>
              </article>
            ))}
          </div>
        )}
      </section>

      <section id="servicios">
        <h2>Catalogo completo de servicios</h2>
        <p className="section-intro">
          Listado dinamico desde <code>GET /api/services/</code>
        </p>
        {status === "ready" && (
          <div className="grid">
            {services.map((service) => (
              <article key={service.id} className="card">
                <h3>{service.title}</h3>
                <p>{service.short_description}</p>
                <button
                  type="button"
                  className="link-btn"
                  onClick={() => toggleDetails(service.id)}
                >
                  {expandedId === service.id ? "Ocultar detalle" : "Ver detalle"}
                </button>
                {expandedId === service.id && (
                  <p className="details">{service.details}</p>
                )}
              </article>
            ))}
          </div>
        )}
      </section>

      <section className="benefits">
        <h2>Por que trabajar con ALPRO</h2>
        <div className="grid">
          {BENEFITS.map((item) => (
            <article key={item.title} className="card">
              <h3>{item.title}</h3>
              <p>{item.text}</p>
            </article>
          ))}
        </div>
      </section>

      <section id="proceso" className="process">
        <h2>Nuestro proceso de trabajo</h2>
        <ol>
          {PROCESS_STEPS.map((step) => (
            <li key={step}>{step}</li>
          ))}
        </ol>
      </section>

      <section id="contacto">
        <h2>Solicita una consultoria</h2>
        <p className="section-intro">
          El formulario envia datos a <code>POST /api/contact/</code> y los guarda en la base de datos.
        </p>
        <form onSubmit={handleSubmit} className="form">
          <input
            name="name"
            placeholder="Nombre completo"
            value={formData.name}
            onChange={handleChange}
            required
          />
          <input
            name="email"
            type="email"
            placeholder="Correo corporativo"
            value={formData.email}
            onChange={handleChange}
            required
          />
          <input
            name="company"
            placeholder="Empresa (opcional)"
            value={formData.company}
            onChange={handleChange}
          />
          <textarea
            name="message"
            placeholder="Describe tu necesidad: web, automatizacion, consultoria..."
            value={formData.message}
            onChange={handleChange}
            required
            rows={5}
          />
          <button type="submit" className="btn btn-primary">
            Enviar solicitud
          </button>
        </form>
        {contactMessage && (
          <p className={contactError ? "feedback error" : "feedback"}>{contactMessage}</p>
        )}
      </section>

      <footer className="footer">
        <p>ALPRO TECHNOLOGY SPA — Proyecto Final Master Full Stack</p>
        <p>
          Backend Django · Frontend React · API REST · Panel administrativo
        </p>
      </footer>
    </div>
  );
}

export default App;
