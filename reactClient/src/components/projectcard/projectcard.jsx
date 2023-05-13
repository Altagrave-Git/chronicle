import './projectcard.scss'

const ProjectCard = ({ project, ordering, click }) => {
  const { name, category, description, site, repo, images, apps } = project;
  const baseUrl = 'http://127.0.0.1:8000';

  return (
    <div onClick={() => click()} className={'project-card' + ' ' + ordering}>
      <div className="project-card__image">
        <img src={baseUrl + images[0].image} alt={images[0].project} />
      </div>
      <div className="project-card__header">
        <h2 className="project-card__title">{name}</h2>
        <h3 className="project-card__category">{category}</h3>
      </div>
      <div className="project-card__body">
      </div>
    </div>
  )
}

export default ProjectCard;