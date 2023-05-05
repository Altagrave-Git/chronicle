import React from "react";
import './home.scss';
import Aside from "../../components/aside/aside";

const HomeView = ({gitData}) => {

  return (
    <main className='home container'>
      <section className="bio">
        <h1 className="name title">Damon Turcotte</h1>
        <h2 className="job subtitle mb-1">Full-stack Web Developer</h2>
        <p>
          I am a self-taught developer with a broad range of technical skills, ranging from UI design and scripting to database management and server configuration. I specialize in functional programming, because I like to have clear, readable and fully customizable code.
        </p>
      </section>
      <Aside gitData={gitData} />
    </main>
  )
};

export default HomeView;