import React from "react";
import { Link, useLocation } from "react-router-dom";
import { ReactComponent as Logo } from '../../icons/name.svg';
import './header.scss';

const headerNav = [
  {
    label: "Portfolio",
    path: "/portfolio"
  },
  {
    label: "Dev Blog",
    path: "/blog"
  },
  {
    label: "About",
    path: "/about"
  }
];

const Header = () => {
  const location = useLocation();
  const headerRef = React.useRef(null);

  const [active, setActive] = React.useState(0);

  React.useEffect(() => {
    const path = location.pathname;
    const index = headerNav.findIndex(nav => nav.path === path);
    setActive(index);
  }, [location]);

  return (
    <>
      <header className="header" ref={headerRef}>
        <div className="container">
          <Link className="logo-link" to="/">
            <Logo />
          </Link>
          <ul className="header-links">
            {
              headerNav.map((nav, index) => (
                <li key={index} className={index === active ? "active" : ""}>
                  <Link to={nav.path}>{nav.label}</Link>
                </li>
              ))
            }
          </ul>
        </div>
      </header>
      <div className="header-spacer">
        <div />
      </div>
    </>
  );
}

export default Header;