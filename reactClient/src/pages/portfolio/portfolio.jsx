import Content from "../../components/content/content";
import { useState, useEffect } from 'react';
import ProjectCard from "../../components/projectcard/projectcard";
import Project from '../../components/project/project';

const PortfolioView = ({ gitData }) => {

  const [portfolioData, setPortfolioData] = useState([]);

  useEffect(() => {
    fetch('http://127.0.0.1:8000/portfolio')
      .then(response => response.json())
      .then(data => setPortfolioData(data));
  }, []);

  console.log(portfolioData)

  return (
    <main>
      <section>
        <div className="portfolio">
          {portfolioData &&
            portfolioData.map((project, index) => {
              return (
                <ProjectCard key={index} project={project} />
              )
            })
          }
        </div>
      </section>
      <Content />
    </main>
  )
}

export default PortfolioView;