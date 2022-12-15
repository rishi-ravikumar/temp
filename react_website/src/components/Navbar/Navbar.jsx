import React, { useState } from 'react'
import './navbar.css'
import LOGO from '../../assets/Logo.png'

const Navbar = (props) => {
    const[activeNav, setActiveNav] = useState('#')
    window.onscroll = function() {scrollFunction()};
    // alert(document.getElementById("contact").offsetTop);

    //changes active section on navbar based on how much someone has scrolled
    function scrollFunction() {
        // alert(window.scrollY);
        if (document.body.scrollTop > 500 || document.documentElement.scrollTop > 500) {
            document.getElementById("navbar").style.top = "0";
            document.getElementById("navbar").style.backgroundColor = "var(--navbar-color)";
        } else {
            document.getElementById("navbar").style.top = "-10rem";
            document.getElementById("navbar").style.backgroundColor = "transparent";
        }

        if (window.scrollY < 20) {
            document.getElementById("navbar").style.top = "0";
            document.getElementById("navbar").style.backgroundColor = "transparent";
        }

        if(window.scrollY > document.getElementById("about").offsetTop - 100){
            setActiveNav('#about'); props.addClass("abt", "hm", "ctct");
        }
        else if(window.scrollY <= document.getElementById("about").offsetTop){
            setActiveNav('#'); props.addClass("hm", "abt", "ctct");
        }

        if(window.scrollY > document.getElementById("contact").offsetTop - 100){
            setActiveNav('#contact'); props.addClass("ctct", "abt", "hm");
        }
        else if(window.scrollY <= document.getElementById("contact").offsetTop && activeNav==='#contact'){
            setActiveNav('#about'); props.addClass("abt", "hm", "ctct");
        }
        else if(window.scrollY <= document.getElementById("about").offsetTop && activeNav == '#about'){
            setActiveNav('#'); props.addClass("hm", "abt", "ctct");
        }
        
    }
  return (
    <div>
        <nav id="navbar" class="navbar navbar-expand-lg navbar-light">
            <a class="navbar-brand main_name" href="#">
                <img class="logo" src={LOGO} alt="logo" />
                <span class="remaining_name">ishi Ravikumar</span>
            </a>
            <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
                Menu <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
                <div class="navbar-nav ml-auto">
                <a id="hm" class="nav-item nav-link active" href="#" onClick={() => {setActiveNav('#'); props.addClass("hm", "abt", "ctct")}}>Home <span class="sr-only">(current)</span></a>
                <a id="abt" class="nav-item nav-link" href="#about" onClick={() => {setActiveNav('#about'); props.addClass("abt", "hm", "ctct")}}>About</a>
                <a id="ctct" class="nav-item nav-link" href="#contact" onClick={() => {setActiveNav('#contact'); props.addClass("ctct", "abt", "hm")}}>Contact</a>
                </div>
            </div>
        </nav>
    </div>
  )
}

export default Navbar