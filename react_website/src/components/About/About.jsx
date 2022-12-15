import React from 'react'
import './About.css'
import ME from '../../assets/me.png'
import RESUME from '../../assets/rishi_resume.pdf'

const About = () => {
  return (
    <div className="about anchor" id="about">
        <p className='section_title'>About Me</p>
        <img className="me" src={ME} />
        <table className="info_table">
            <tr>
                <td className="info_title">Name: </td>
                <td className="data info_title">Rishi Ravikumar</td>
            </tr>
            <tr>
                <td className="info_title">Date of birth: </td>
                <td className="data info_title">dd mm yy</td>
            </tr>
            <tr>
                <td className="info_title">Email: </td>
                <td className="data info_title">example@example.com</td>
            </tr>
            <tr>
                <td className="info_title">University: </td>
                <td className="data info_title">The University of Manchester</td>
            </tr>
            <tr>
                <td className="info_title">Degree: </td>
                <td className="data info_title">MEng(Hons.) Artificial Intelligence (2nd Year)</td>
            </tr>
            <tr colspan="3" className="rw">
                <td className="info_title info_title"><a href={RESUME} download><button className='dwnld_resume'>Download Résumé</button></a></td>
            </tr>
        </table>
    </div>
  )
}

export default About