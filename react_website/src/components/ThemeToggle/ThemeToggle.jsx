import React from 'react'
import Toggle from 'react-toggle'
import './themeToggle.css'

const ThemeToggle = (props) => {
  return (
    <div>
        <p className="toggleSwitch">
        ☀️
        <Toggle
          onChange={props.switchTheme}
          icons={false}
        />
        🌑
      </p>
    </div>
  )
}

export default ThemeToggle