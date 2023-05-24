import { useState, useEffect } from 'react';
import ProjectCard from "../../components/projectcard/projectcard";
import ProjectDetail from "../../components/projectdetail/projectdetail";
import './portfolio.scss';

const PortfolioView = () => {
  const [portfolioData, setPortfolioData] = useState([]);
  const [projectDetail, setProjectDetail] = useState({});
  const [activeIndex, setActiveIndex] = useState(0);

  // Retrieve project data from Chronicle API
  useEffect(() => {
    fetch(import.meta.env.VITE_CHRONICLE_URL + '/projects/')
      .then(response => response.json())
      .then(data => setPortfolioData(data));
  }, []);

  console.log(portfolioData)

  // Rotate active index state backwards
  const handlePrev = () => {
    if (activeIndex === 0) {
      setActiveIndex(portfolioData.length - 1);
    } else {
      setActiveIndex(activeIndex - 1);
    }
    window.scrollTo(0, 0);
  }

  // Rotate active index state forwards
  const handleNext = () => {
    if (activeIndex === portfolioData.length - 1) {
      setActiveIndex(0);
      setProjectDetail(portfolioData[0]);
    } else {
      setActiveIndex(activeIndex + 1);
      setProjectDetail(portfolioData[activeIndex + 1]);
    }
    window.scrollTo(0, 0);
  }

  // Set project detail (aside) to active
  const handleActive = () => {
    if (document.querySelector('section.active')) {
      document.querySelector('section.portfolio').classList.remove('active');
      document.querySelector('aside.portfolio').classList.add('active');
    } else if (document.querySelector('aside.active')) {
      document.querySelector('aside.portfolio').classList.remove('active');
      document.querySelector('section.portfolio').classList.add('active');
    }
    // scroll to top of page
    window.scrollTo(0, 0);
  }

  useEffect(() => {
    setProjectDetail(portfolioData[activeIndex]);
  }, [activeIndex, portfolioData])

  useEffect(() => {
    if (portfolioData.length > 0) {
      const prev = document.querySelector('.prev-container');
      const active = document.querySelector('.active-container');
      const next = document.querySelector('.next-container');
      const prevCard = document.querySelector('.prev-card');
      const activeCard = document.querySelector('.active-card');
      const nextCard = document.querySelector('.next-card');
  
      prev.appendChild(prevCard);
      active.appendChild(activeCard);
      next.appendChild(nextCard);
    }
  }, [activeIndex, portfolioData])

  return (
    <main>
      <section className="portfolio fixed active">
        <div className="portfolio">
          <div className="prev-container"></div>
          <div className="active-container"></div>
          <div className="next-container"></div>
          {portfolioData &&
            portfolioData.map((project, index) => {
              if (index === activeIndex) {
                return <ProjectCard key={index} project={project} click={setProjectDetail} handleActive={handleActive} ordering="active-card" />
              } else if (index === activeIndex - 1 || (activeIndex === 0 && index === portfolioData.length - 1)) {
                return <ProjectCard key={index} project={project} click={handlePrev} ordering="prev-card" />
              } else if (index === activeIndex + 1 || (activeIndex === portfolioData.length - 1 && index === 0)) {
                return <ProjectCard key={index} project={project} click={handleNext} ordering="next-card" />
              } else {
                return <ProjectCard key={index} project={project} click={() => {return}} />
              }
            })
          }
        </div>
      </section>
      <section className="portfolio placeholder"></section>
      <aside className="portfolio">
          <ProjectDetail project={projectDetail} handleActive={handleActive} />
      </aside>
    </main>
  )
}

export default PortfolioView;