import './projectdetail.scss'
import { ReactComponent as GithubLogo } from "../../icons/github.svg";
import { ReactComponent as SiteLogo } from "../../icons/website.svg";
import TechIcon from '../techicon/techicon';

const ProjectDetail = ({ project, handleActive }) => {

  return (
  <>
    { project &&
      <div className="project-detail">
        <div className="btn-back" onClick={() => handleActive()}>
          <svg viewBox="6 5 10 15" fill="none"><g strokeWidth="0"></g><g strokeLinecap="round" strokeLinejoin="round"></g><g> <path d="M8 12L16 12" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"></path> <path d="M11 9L8.08704 11.913V11.913C8.03897 11.961 8.03897 12.039 8.08704 12.087V12.087L11 15" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"></path> </g></svg>
          <div>Back</div>
        </div>
        <div className="project-detail__header">
          <div>
            <h2 className="project-detail__title">{project.name}</h2>
            <h3 className="project-detail__category">{project.category}</h3>
          </div>
          <div className="project-detail__links">
            { project.site &&
            <a href={project.site} className="project-detail__link website">
              <SiteLogo />
              Website
            </a>
            }
            { project.repo &&
            <a href={project.repo} className="project-detail__link github">
              <GithubLogo />
              Github
            </a>
            }
          </div>
        </div>
        <div className="project-detail__body">
          <div className="project-detail__description">
            <p>{project.description}</p>
          </div>
          { project.tech &&
            <div className="project-detail__section">
              <h4>Technologies</h4>
              <div className="project-detail__tech">
                  {project.tech.map((tech, index) => {
                    return (
                      <div key={index} className="project-detail__tech-item">
                        <TechIcon tech={tech.tech} />
                        <span>{tech.tech}</span>
                      </div>
                    )
                  })}
              </div>
            </div>
          }
          <div className="project-detail__sections">
            {
              project.sections && project.sections.map((section, index) => {
                return (
                  <div key={index} className="project-detail__section">
                    <h4>{section.title}</h4>
                    {section.type === 'text' &&
                      <p>{section.description}</p>
                    }
                    { section.type === 'list' &&
                      <ul>
                        {section.description.split('\n').map((item, index) => {
                          return <li key={index}>{item}</li>
                        })}
                      </ul>
                    }
                    {section.snippets &&
                      section.snippets.map((snippet, index) => {
                        return <div key={index} dangerouslySetInnerHTML={{__html: snippet.highlighted}} />
                      })
                    }
                  </div>
                )
              })
            }     
          </div>
        </div>
        <div className="project-detail__apps">
            {project.apps &&
              project.apps.map((app, index) => {
                return (
                  <div key={index} className="project-detail__app">
                    <h4>{app.name}</h4>
                    <p>{app.description}</p>
                    <div className="project-detail__app-images">
                      { app.images &&
                        app.images.map((image, index) => {
                        return (
                          <img key={index} src={image} alt={app.name} />
                        )
                      })}
                    </div>
                  </div>
                )
              })
            }
        </div>
      </div>
    }
  </>
  )
}

export default ProjectDetail;