import { useEffect } from "react";
import { useLocation } from "react-router-dom";

function resetScrollPosition() {
  window.history.scrollRestoration = "manual";
  if (window.location.hash) {
    window.history.replaceState(null, "", window.location.pathname + window.location.search);
  }
  window.scrollTo(0, 0);
}

export default function ScrollToTop() {
  const { pathname } = useLocation();

  useEffect(() => {
    resetScrollPosition();
    window.addEventListener("pageshow", resetScrollPosition);
    return () => window.removeEventListener("pageshow", resetScrollPosition);
  }, [pathname]);

  return null;
}
