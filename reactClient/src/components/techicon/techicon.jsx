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
import { ReactComponent as GithubLogo } from "../../icons/github.svg";
import { ReactComponent as NginxLogo } from "../../icons/nginx.svg";
import { ReactComponent as GunicornLogo } from "../../icons/gunicorn.svg";
import { ReactComponent as LinuxLogo } from "../../icons/linux.svg";
import { ReactComponent as BashLogo } from "../../icons/bash.svg";
import { ReactComponent as AnacondaLogo } from "../../icons/anaconda.svg";
import { ReactComponent as SiteLogo } from "../../icons/website.svg";
import { ReactComponent as JinjaLogo } from "../../icons/jinja.svg";
import { ReactComponent as UbuntuLogo } from "../../icons/ubuntu.svg";

const TechIcon = ({ tech }) => {
  const techIcons = [
    { name: "React", icon: <ReactLogo /> },
    { name: "HTML", icon: <HtmlLogo /> },
    { name: "CSS", icon: <CssLogo /> },
    { name: "SASS", icon: <SassLogo /> },
    { name: "Javascript", icon: <JavascriptLogo /> },
    { name: "jQuery", icon: <JqueryLogo /> },
    { name: "Bootstrap", icon: <BootstrapLogo /> },
    { name: "Python", icon: <PythonLogo /> },
    { name: "Django", icon: <DjangoLogo /> },
    { name: "Rest API", icon: <RestLogo /> },
    { name: "PostgreSQL", icon: <PostgresLogo /> },
    { name: "AuthO", icon: <AuthLogo /> },
    { name: "SQLite", icon: <SqliteLogo /> },
    { name: "Git", icon: <GitLogo /> },
    { name: "GitHub", icon: <GithubLogo /> },
    { name: "NGINX", icon: <NginxLogo /> },
    { name: "Gunicorn", icon: <GunicornLogo /> },
    { name: "Linux", icon: <LinuxLogo /> },
    { name: "Bash", icon: <BashLogo /> },
    { name: "Anaconda", icon: <AnacondaLogo /> },
    { name: "Site", icon: <SiteLogo /> },
    { name: "Jinja", icon: <JinjaLogo /> },
    { name: "Ubuntu", icon: <UbuntuLogo /> },
  ];

  const techIcon = techIcons.find((icon) => icon.name == tech);

  return (
    <>
      {techIcon ? techIcon.icon : null}
    </>
  )
}

export default TechIcon;