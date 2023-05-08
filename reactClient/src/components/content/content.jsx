import './content.scss';
import GitStream from '../gitstream/gitstream';
import Skills from '../skills/skills';

const Content = ({gitData, className}) => {
  return (
    <aside className={className}>
      {className === "home" &&
        <>
          <Skills />
          <GitStream gitData={gitData} />
        </>
      }
      {className === "portfolio" &&
        <>
          <Skills />
          <GitStream gitData={gitData} />
        </>
      }
      {className === "blog" &&
        <>
          <Skills />
          <GitStream gitData={gitData} />
        </>
      }
      {className === "about" &&
        <>
          <Skills />
          <GitStream gitData={gitData} />
        </>
      }
    </aside>
  )
}

export default Content;