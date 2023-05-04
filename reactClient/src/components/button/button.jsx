import './button.scss';

const Button = ({ text, color, onClick }) => {
  return (
    <button onClick={onClick} className={`btn btn-${color}`}>{text}</button>
  )
}

export default Button;