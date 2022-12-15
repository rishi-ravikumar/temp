import React from 'react'
import ThemeToggle from '../ThemeToggle/ThemeToggle'
import './home.css'
import Typewriter from 'typewriter-effect'

const Home = (props) => {
  return (
    <div className="home" id="home">
        <ThemeToggle className="toggle" switchTheme={props.switchTheme} />
        <div className="main_text">
          <span className="iam">Hey! I am</span>
          <br />
          <span className="animated_name">Rishi Ravikumar</span>
          <br />
          <p className='animated_line'>
            <Typewriter className="typewriter"
              options={{
                strings: ['Developer', 'Student'],
                autoStart: true,
                loop: true,
                pauseFor: 2000,
                wrapperClassName: "typewriter",
                cursorClassName: "cursor"
              }}
            />
          </p>
        </div>
        <div className='mouse_container'>
          <div class="mousey">
            <div class="scroller"></div>
          </div>
        </div>
    </div>
  )
}

export default Home