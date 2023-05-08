const ProjectDetail = ({ project }) => {
  return (
  <>
    { project &&
      <div className="project-detail">
        <div className="project-detail__header">
          <h2 className="project-detail__title">{project.name}</h2>
          <h3 className="project-detail__category">{project.category}</h3>
        </div>
        <div className="project-detail__body">
          <div className="project-detail__description">
            <p>{project.description}</p>
          </div>
          <div className="project-detail__links">
            <a href={project.site} className="project-detail__link">Site</a>
            <a href={project.repo} className="project-detail__link">Repo</a>
          </div>
        </div>
        <div>
            <h3 className="project-detail__apps">Apps</h3>
            <ul className="project-detail__app-list">
              {project.apps && project.apps.map((app, index) => {
                return (
                  <li key={index} className="project-detail__app">{app.name}</li>
                )
              })}
            </ul>
        </div>
      </div>
    }
  </>
  )
}

export default ProjectDetail;