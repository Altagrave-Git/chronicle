import { useState, useEffect } from 'react';
import ProjectCard from "../../components/projectcard/projectcard";
import ProjectDetail from "../../components/projectdetail/projectdetail";

const PortfolioView = () => {

  const [portfolioData, setPortfolioData] = useState([]);
  const [projectDetail, setProjectDetail] = useState({});

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
                <ProjectCard key={index} project={project} click={setProjectDetail} />
              )
            })
          }
        </div>
      </section>
      <aside className="portfolio">
          <ProjectDetail project={projectDetail} />
      </aside>
    </main>
  )
}

export default PortfolioView;