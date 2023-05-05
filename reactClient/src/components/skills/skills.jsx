import './skills.scss';
import { ReactComponent as ReactLogo } from '../../icons/react.svg';
import { ReactComponent as HtmlLogo } from '../../icons/html.svg';
import { ReactComponent as CssLogo } from '../../icons/css.svg';
import { ReactComponent as SassLogo } from '../../icons/sass.svg';
import { ReactComponent as JavascriptLogo } from '../../icons/javascript.svg';
import { ReactComponent as JqueryLogo } from '../../icons/jquery.svg';
import { ReactComponent as BootstrapLogo } from '../../icons/bootstrap.svg';
import { ReactComponent as PythonLogo } from '../../icons/python.svg';
import { ReactComponent as DjangoLogo } from '../../icons/django.svg';
import { ReactComponent as RestLogo } from '../../icons/rest.svg';
import { ReactComponent as PostgresLogo } from '../../icons/postgresql.svg';
import { ReactComponent as SqliteLogo } from '../../icons/sqlite.svg';
import { ReactComponent as GithubLogo } from '../../icons/github.svg';
import { ReactComponent as NginxLogo } from '../../icons/nginx.svg';
import { ReactComponent as GunicornLogo } from '../../icons/gunicorn.svg';
import { ReactComponent as BashLogo } from '../../icons/bash.svg';
import { ReactComponent as AnacondaLogo } from '../../icons/anaconda.svg';

const Skills = () => {
    return (
        <div className="skills">
            <h1>Skills</h1>
            <div className="skills-container">
                <div className="skill">
                    <h3>Front End</h3>
                    <ul>
                        <li>
                          <ReactLogo />
                          React
                        </li>
                        <li>
                          <HtmlLogo />
                          HTML
                        </li>
                        <li>
                          <CssLogo />
                          CSS
                        </li>
                        <li>
                          <SassLogo />
                          Sass
                        </li>
                        <li>
                          <JavascriptLogo />
                          JavaScript
                        </li>
                        <li>
                          <JqueryLogo />
                          jQuery
                        </li>
                        <li>
                          <BootstrapLogo />
                          Bootstrap
                        </li>
                    </ul>
                </div>
                <div className="skill">
                    <h3>Back End</h3>
                    <ul>
                        <li>
                          <PythonLogo />
                          Python
                        </li>
                        <li>
                          <DjangoLogo />
                          Django
                        </li>
                        <li>
                          <RestLogo />
                          Rest API
                        </li>
                        <li>
                          <PostgresLogo />
                          PostgreSQL
                        </li>
                        <li>
                          <SqliteLogo />
                          SQLite
                        </li>
                    </ul>
                </div>
                <div className="skill">
                    <h3>DevOps</h3>
                    <ul>
                        <li>
                          <GithubLogo className="github-logo" />
                          GitHub
                        </li>
                        <li>
                          <NginxLogo />
                          Nginx
                        </li>
                        <li>
                          <GunicornLogo className="gunicorn-logo" />
                          Gunicorn
                        </li>
                        <li>
                          <BashLogo className="bash-logo" />
                          Bash
                        </li>
                        <li>
                          <AnacondaLogo />
                          Anaconda
                        </li>
                    </ul>
                </div>
            </div>
        </div>
    );
}

export default Skills;