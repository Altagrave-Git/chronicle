import './App.scss';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Header from './components/header/header';
import HomeView from './pages/home/home';
import PortfolioView from './pages/portfolio/portfolio';
import BlogView from './pages/blog/blog';
import AboutView from './pages/about/about';
import { Octokit } from "https://cdn.skypack.dev/octokit?dts";
import { useState, useEffect } from 'react';

const App = () => {
  const apiToken = import.meta.env.VITE_GITHUB_TOKEN;
  const octokit = new Octokit({ auth: apiToken }, { userAgent: 'Altagrave-Git' });

  // get octokit rate limit
  octokit.request('GET /rate_limit')
    .then(({ data }) => {
      console.log(data);
    });

  const [gitData, setGitData] = useState([]);

  useEffect(() => {
    octokit.request('GET /users/Altagrave-Git/repos', {
      sort: 'pushed',
    })
      .then(({ data }) => {
        setGitData(data);
      });
  }, []);

  console.log(gitData)

  return (
    <BrowserRouter>
      <Header />
      <Routes>
        <Route path="/" element={<HomeView gitData={gitData} />} />
        <Route path="/portfolio" element={<PortfolioView />} />
        <Route path="/blog" element={<BlogView />} />
        <Route path="/about" element={<AboutView />} />
      </Routes>
    </BrowserRouter>
  );
};

export default App;
