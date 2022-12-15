import React, { useState } from "react"
import "./App.css"
import Navbar from './components/Navbar/Navbar'
import Home from './components/Home/Home'
import About from "./components/About/About"
import Footer from "./components/Footer/Footer"
import Contact from "./components/Contact/Contact"
// import WorkInProgress from "./components/WorkInProgress/WorkInProgress"
// import useLocalStorage from 'use-local-storage'

export default function App() {
  // the following will allow for the user's preferred colour scheme to be the initial colour scheme of the website
  // const defaultDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  // if(defaultDark)
  //   document.body.className = 'bg';
  // const [theme, setTheme] = useLocalStorage('theme', defaultDark ? 'dark' : 'light');

  const [theme, setTheme] = useState('light');

  const switchTheme = () => {
    const newTheme = theme === 'light' ? 'dark' : 'light';
    setTheme(newTheme);
    if(document.body.className === 'bg'){
      document.body.className = ''
    }
    else
      document.body.className = 'bg'
  }

  // to change active section in navbar
  function addClass(id, remid1, remid2){
    document.getElementById(id).classList.add("active");
    document.getElementById(remid1).classList.remove("active");
    document.getElementById(remid2).classList.remove("active");
  }

  return (
    <>
    <div data-theme={theme} className="app" id="app">
      <Navbar addClass={addClass}/>      
      <Home switchTheme={switchTheme}/>
      <About/>
      <Contact />
      <Footer className="footer" />
    </div>
  </>
  );
}