import React from "react";
import './home.scss';
import GitStream from "../../components/gitstream/gitstream";

const HomeView = ({gitData}) => {

  return (
    <main className='home container'>
      <GitStream gitData={gitData} />
    </main>
  )
};

export default HomeView;