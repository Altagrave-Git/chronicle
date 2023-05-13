import Slider from 'react-slick';
import { useState, useEffect } from 'react';
import './slider.scss';

const SliderComponent = () => {
  const [portfolioData, setPortfolioData] = useState([]);

  useEffect(() => {
    fetch(import.meta.env.VITE_CHRONICLE_URL + '/projects/')
      .then(response => response.json())
      .then(data => setPortfolioData(data));
  }, []);



  const settings = {
    dots: true,
    infinite: true,
    speed: 500,
    slidesToShow: 1,
    slidesToScroll: 1,
    vertical: true,
    verticalSwiping: true,
    arrows: true,
    responsive: [
      {
        breakpoint: 768,
        settings: {
          vertical: false,
          verticalSwiping: false,
        },
      },
    ],
  };

  return (
    <Slider {...settings}>
      {portfolioData &&
        portfolioData.map((project, index) => (
          <div className="slider-card" key={index}>
            <img src={'http://127.0.0.1:8000' + project.images[0].image} alt={project.name} />
            <div>
              <h3>{project.name}</h3>
            </div>
          </div>
        ))}
    </Slider>
  );
}

export default SliderComponent;