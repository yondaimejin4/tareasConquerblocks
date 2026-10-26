import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { API_BASE_URL, apiFetch, ensureCsrf, fetchServices } from "../api/client";
const WHATSAPP_NUMBER = "56948708980";
const WHATSAPP_URL = `https://wa.me/${WHATSAPP_NUMBER}?text=${encodeURIComponent(
  "Hola ALPRO, me interesa una consultoria tecnologica."
)}`;

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

const VISION = {
  title: "Vision",
  text: "Ser la referencia en soluciones digitales para pymes de Latinoamerica, reconocidas por innovacion, confianza y resultados medibles en cada proyecto.",
};

const MISSION = {
  title: "Mision",
  text: "Acelerar la transformacion digital de nuestros clientes mediante desarrollo web, automatizacion y consultoria tecnica cercana, con equipos comprometidos y tecnologia de vanguardia.",
};

const VALUES = [
  {
    title: "Excelencia tecnica",
    text: "Codigo mantenible, arquitecturas seguras y entregas que cumplen estandares profesionales.",
  },
  {
    title: "Transparencia",
    text: "Comunicacion clara en plazos, costos y alcance de cada iniciativa.",
  },
  {
    title: "Innovacion util",
    text: "Adoptamos herramientas nuevas solo cuando aportan valor real al negocio.",
  },
  {
    title: "Compromiso con el cliente",
    text: "Acompanamos antes, durante y despues del lanzamiento de cada solucion.",
  },
  {
    title: "Seguridad y datos",
    text: "Protegemos la informacion con buenas practicas y cumplimiento responsable.",
  },
  {
    title: "Mejora continua",
    text: "Iteramos con feedback, metricas y aprendizaje en cada ciclo de trabajo.",
  },
];

export default function LandingPage() {
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

  const scrollToSection = (sectionId) => (event) => {
    event.preventDefault();
    document.getElementById(sectionId)?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    const loadData = async () => {
      try {
        const { services: allData, featured: featuredData } = await fetchServices();
        setServices(allData);
        setFeatured(featuredData);
        setStatus("ready");
      } catch {
        setServices([]);
        setFeatured([]);
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
      await ensureCsrf();
      const { response, data } = await apiFetch("/api/contact/", {
        method: "POST",
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        const detail =
          typeof data === "object" && data !== null
            ? Object.values(data).flat().join(" ")
            : null;
        throw new Error(detail || "Error al enviar solicitud");
      }

      setContactMessage(data.message);
      setFormData({ name: "", email: "", company: "", message: "" });
    } catch (error) {
      setContactError(true);
      const detail = error instanceof Error ? error.message : "";
      setContactMessage(
        detail && detail !== "Error al enviar solicitud"
          ? detail
          : "No se pudo enviar la solicitud. Revisa los datos e intenta de nuevo.",
      );
    }
  };

  const toggleDetails = (id) => {
    setExpandedId((current) => (current === id ? null : id));
  };

  return (
    <>
    <div className="page">
      <header className="topbar">
        <p className="brand">ALPRO TECHNOLOGY SPA</p>
        <nav className="nav">
          <a href="/" onClick={scrollToSection("nosotros")}>
            Nosotros
          </a>
          <a href="/" onClick={scrollToSection("servicios")}>
            Servicios
          </a>
          <a href="/" onClick={scrollToSection("proceso")}>
            Proceso
          </a>
          <a href="/" onClick={scrollToSection("contacto")}>
            Contacto
          </a>
          <Link to="/portal/login">Area cliente</Link>
        </nav>
      </header>

      <section className="hero">
        <p className="eyebrow">Soluciones digitales para empresas que quieren crecer</p>
        <h1>Tu negocio merece tecnologia que genera resultados — no complicaciones</h1>
        <p className="hero-text">
          Desarrollo web, automatizacion de procesos y consultoria tecnologica para empresas que
          quieren crecer con soluciones digitales seguras, escalables y alineadas a sus objetivos de negocio.
        </p>
        <div className="hero-actions">
          <a className="btn btn-primary" href="/" onClick={scrollToSection("contacto")}>
            Solicitar consultoria
          </a>
          <a className="btn btn-secondary" href="/" onClick={scrollToSection("servicios")}>
            Ver servicios
          </a>
        </div>
      </section>

      {status === "ready" && (
        <p className="api-alert ok">
          Conectado al servidor — {services.length} servicios, {featured.length} destacados
        </p>
      )}
      {status === "error" && (
        <p className="api-alert error">
          No se conecto con el backend. Usa <strong>http://127.0.0.1:8000/</strong> y ejecuta:{" "}
          <code>./scripts/dev.sh</code> desde la raiz del proyecto.
        </p>
      )}

      <section className="stats">
        <article>
          <strong>{status === "loading" ? "..." : services.length}</strong>
          <span>Servicios activos</span>
        </article>
        <article>
          <strong>{status === "loading" ? "..." : featured.length}</strong>
          <span>Destacados</span>
        </article>
        <article>
          <strong>24/7</strong>
          <span>Soporte acordado</span>
        </article>
        <article>
          <strong>100%</strong>
          <span>Enfoque personalizado</span>
        </article>
      </section>

      <section id="nosotros" className="about">
        <h2>Quienes somos</h2>
        <p className="section-intro">
          ALPRO TECHNOLOGY SPA nace para acercar tecnologia de nivel empresarial a organizaciones
          que necesitan crecer con orden, datos y presencia digital profesional.
        </p>
        <div className="vmv-grid">
          <article className="card card-vmv card-vision">
            <span className="vmv-icon" aria-hidden="true">
              ◈
            </span>
            <h3>{VISION.title}</h3>
            <p>{VISION.text}</p>
          </article>
          <article className="card card-vmv card-mission">
            <span className="vmv-icon" aria-hidden="true">
              ◆
            </span>
            <h3>{MISSION.title}</h3>
            <p>{MISSION.text}</p>
          </article>
        </div>
        <h2>Nuestros valores</h2>
        <div className="grid values-grid">
          {VALUES.map((item) => (
            <article key={item.title} className="card card-value">
              <h4>{item.title}</h4>
              <p>{item.text}</p>
            </article>
          ))}
        </div>
      </section>

      <section id="destacados">
        <h2>Servicios destacados</h2>
        <p className="section-intro">
          Las soluciones mas demandadas por nuestros clientes, listas para impulsar tu transformacion digital.
        </p>
        {status === "loading" && <p className="muted">Cargando servicios destacados...</p>}
        {status === "error" && (
          <p className="error">
            No pudimos cargar los servicios en este momento. Intenta de nuevo en unos minutos.
          </p>
        )}
        {status === "ready" && featured.length === 0 && (
          <p className="muted">Muy pronto publicaremos nuevas soluciones destacadas.</p>
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
          Explora todas nuestras areas de especializacion y solicita asesoria sobre la que mejor se adapte a tu empresa.
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

      <section id="contacto" className="contact-section">
        <h2>Solicita una consultoria</h2>
        <p className="section-intro">
          Cuentanos tu proyecto y te responderemos a la brevedad para agendar una consultoria sin compromiso.
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
        <p>ALPRO TECHNOLOGY SPA — Innovacion digital y soluciones informaticas</p>
        <p>Desarrollo web · Automatizacion · Consultoria · Chile</p>
      </footer>
    </div>

    <a
      href={WHATSAPP_URL}
      className="whatsapp-float"
      target="_blank"
      rel="noopener noreferrer"
      aria-label="Contactar por WhatsApp al +56948708980"
      title="Escríbenos por WhatsApp"
    >
      <svg viewBox="0 0 24 24" aria-hidden="true" className="whatsapp-icon">
        <path
          fill="currentColor"
          d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.435 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"
        />
      </svg>
    </a>
    </>
  );
}
