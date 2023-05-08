import "./skills.scss";
import { ReactComponent as ReactLogo } from "../../icons/react.svg";
import { ReactComponent as HtmlLogo } from "../../icons/html.svg";
import { ReactComponent as CssLogo } from "../../icons/css.svg";
import { ReactComponent as SassLogo } from "../../icons/sass.svg";
import { ReactComponent as JavascriptLogo } from "../../icons/javascript.svg";
import { ReactComponent as JqueryLogo } from "../../icons/jquery.svg";
import { ReactComponent as BootstrapLogo } from "../../icons/bootstrap.svg";
import { ReactComponent as PythonLogo } from "../../icons/python.svg";
import { ReactComponent as DjangoLogo } from "../../icons/django.svg";
import { ReactComponent as RestLogo } from "../../icons/rest.svg";
import { ReactComponent as PostgresLogo } from "../../icons/postgresql.svg";
import { ReactComponent as AuthLogo } from "../../icons/auth.svg";
import { ReactComponent as SqliteLogo } from "../../icons/sqlite.svg";
import { ReactComponent as GitLogo } from "../../icons/git.svg";
import { ReactComponent as NginxLogo } from "../../icons/nginx.svg";
import { ReactComponent as GunicornLogo } from "../../icons/gunicorn.svg";
import { ReactComponent as LinuxLogo } from "../../icons/linux.svg";
import { ReactComponent as BashLogo } from "../../icons/bash.svg";
import { ReactComponent as AnacondaLogo } from "../../icons/anaconda.svg";

const Skills = () => {

  return (
    <div className="skills">
      <h1>Skills</h1>
      <div className="skills-container">
        <div className="front-end">
          <h3>Front End</h3>
          <div className="icon-container">
            <ul>
              <li className="icon">
                <HtmlLogo />
                HTML
              </li>
              <li className="icon">
                <CssLogo />
                CSS
              </li>
              <li className="icon">
                <SassLogo />
                Sass
              </li>
              <li className="icon">
                <JavascriptLogo className="javascript-logo" />
                JavaScript
              </li>
              <li className="icon">
                <JqueryLogo />
                jQuery
              </li>
              <li className="icon">
                <ReactLogo />
                React
              </li>
            </ul>
          </div>
        </div>
        <div className="back-end">
          <h3>Back End</h3>
          <div className="icon-container">
            <ul>
              <li className="icon">
                <PythonLogo />
                Python
              </li>
              <li className="icon">
                <DjangoLogo />
                Django
              </li>
              <li className="icon">
                <RestLogo />
                Rest API
              </li>
              <li className="icon">
                <AuthLogo />
                Auth0
              </li>
              <li className="icon">
                <PostgresLogo />
                PostgreSQL
              </li>
              <li className="icon">
                <SqliteLogo />
                SQLite
              </li>
            </ul>
          </div>
        </div>
        <div className="dev-ops">
          <h3>DevOps</h3>
          <div className="icon-container">
            <ul>
              <li className="icon">
                <GitLogo className="git-logo" />
                Git
              </li>
              <li className="icon">
                <NginxLogo />
                Nginx
              </li>
              <li className="icon">
                <GunicornLogo className="gunicorn-logo" />
                Gunicorn
              </li>
              <li className="icon">
                <LinuxLogo className="linux-logo" />
                Linux
              </li>
              <li className="icon">
                <BashLogo className="bash-logo" />
                Bash
              </li>
              <li className="icon">
                <AnacondaLogo />
                Anaconda
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Skills;
