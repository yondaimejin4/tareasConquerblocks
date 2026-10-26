import { Component } from "react";

export default class ErrorBoundary extends Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, message: "" };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, message: error?.message || "Error desconocido" };
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="page" style={{ padding: "2rem", textAlign: "center" }}>
          <h1>Algo salio mal</h1>
          <p className="error">{this.state.message}</p>
          <p className="muted">
            Prueba recargar la pagina. Si persiste, reinicia el frontend con{" "}
            <code>npm run dev</code>.
          </p>
          <a href="/" className="btn btn-primary" style={{ marginTop: "1rem" }}>
            Ir al inicio
          </a>
        </div>
      );
    }

    return this.props.children;
  }
}
