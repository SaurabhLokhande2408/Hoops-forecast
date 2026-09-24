import { NavLink } from "react-router-dom";

const links = [
  { to: "/", label: "Predict" },
  { to: "/history", label: "History" },
  { to: "/about", label: "About" }
];

export default function Navbar() {
  return (
    <header className="navbar">
      <div className="navbar__inner">
        <NavLink to="/" className="navbar__brand">
          <span className="navbar__ball">🏀</span> Hoops Forecast
        </NavLink>
        <nav className="navbar__links">
          {links.map((l) => (
            <NavLink
              key={l.to}
              to={l.to}
              className={({ isActive }) =>
                "navbar__link" + (isActive ? " navbar__link--active" : "")
              }
              end={l.to === "/"}
            >
              {l.label}
            </NavLink>
          ))}
        </nav>
      </div>
    </header>
  );
}
