import './projectcard.scss'

/*
project = {
  name: 'Project Title',
  category: 'Project Category',
  description: 'Project Description',
  site: 'Project Site',
  repo: 'Project Repo',
  images: [
    {
      image: imageUrl,
      project: 'Project Title'
      app: 'App Name'
    }]
  apps: [
    {
      name: 'App Name',
      description: 'App Description',
      project: 'Project Title',
      site: 'App Site',
      images: [
        {
          image: imageUrl,
          project: 'Project Title'
          app: 'App Name'
        }]
    }]
}
*/

const ProjectCard = ({ project }) => {
  const { name, category, description, site, repo, images, apps } = project;
  const baseUrl = 'http://127.0.0.1:8000';

  return (
    <div className="project-card">
      <div className="project-card__image">
        <img src={baseUrl + images[0].image} alt={images[0].project} />
      </div>
      <div className="project-card__header">
        <h2 className="project-card__title">{name}</h2>
        <h3 className="project-card__category">{category}</h3>
      </div>
      <div className="project-card__body">
        <p className="project-card__description">{description}</p>
        <div className="project-card__links">
          <a href={site} className="project-card__link">Site</a>
          <a href={repo} className="project-card__link">Repo</a>
        </div>
      </div>
    </div>
  )
}

export default ProjectCard;