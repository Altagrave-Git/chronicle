import './gitstream.scss';

const GitStream = ({gitData}) => {
  return (
    <div className='gitstream'>
      { gitData.length === 0 ? <h2>Loading...</h2> :
        gitData.map((repo, index) => {
          return (
            <div key={index} className='repo'>
              <h3>{repo.name}</h3>
              <p>{repo.description}</p>
              <p>{repo.language}</p>
              <p>{repo.updated_at}</p>
              <a href={repo.html_url} target='_blank' rel='noreferrer'>View on GitHub</a>
            </div>
          )
        })
      }
    </div>
  )
}

export default GitStream;
