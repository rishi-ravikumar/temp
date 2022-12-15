import React from 'react'
import './footer.css'
import LOGO from '../../assets/Logo.png'
import { BsLinkedin, BsGithub } from 'react-icons/bs'
import { FaDiscord } from 'react-icons/fa'


const Footer = () => {
  return (
    <div className='footer'>
      <div className="Row">
        <div class="Column wuc">Website Partially Under Construction</div>
      </div>
      <div className="Row">
        <div class="Column">Made from scratch using React</div>
        <div class="Column"><a href="https://example.com"><BsLinkedin className='icon' /></a><a href="https://www.github.com/rexample/"><BsGithub className='icon' /></a><a href="https://example.com"><FaDiscord className='icon' /></a></div>
        <div class="Column">&copy; Copyright 2022, Rishi Ravikumar</div>
      </div>
    </div>
  )
}

export default Footer