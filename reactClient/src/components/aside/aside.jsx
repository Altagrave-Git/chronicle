import './aside.scss';
import GitStream from '../gitstream/gitstream';
import Skills from '../skills/skills';

const Aside = ({gitData}) => {
  return (
    <aside>
      <Skills />
      <GitStream gitData={gitData} />
    </aside>
  )
}

export default Aside;