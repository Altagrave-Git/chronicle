import './gitstream.scss';

const GitStream = ({gitData}) => {
  return (
  <>
    { gitData.length === 0 ? <h2>Loading...</h2> :
      <div className='gitstream text-center pb-1'>
        <h2 className='git-title title-2'>Github Stream</h2>
        <a href='https://github.com/Altagrave-Git' className="git-user">
          <img className='git-logo' src="https://avatars.githubusercontent.com/u/114028969?v=4" alt='Altagrave-Git Logo' />
          <h3 className='subtitle-3'>Altagrave-Git</h3>
        </a>
        <h3 className='git-subtitle subtitle-2 text-left'>Recent Activity</h3>
        {
          gitData.map((repo, index) => {
            { if (index < 5) {
              return (
                <a key={index} href={repo.html_url} target='_blank' rel='noreferrer'>
                  <div className='git-repo text-left'>
                    <h3 className="name text">{repo.name}</h3>
                    <p className="date text-2">{repo.pushed_at.split("T")[0].replaceAll("-", "/")}</p>
                  </div>
                </a>
              )
            }}
          })
        }
      </div>
    }
  </>
  )
}

export default GitStream;