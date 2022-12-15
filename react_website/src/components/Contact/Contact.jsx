import React from 'react'
import emailjs from 'emailjs-com'
import './contact.css'

const Contact = () => {
  // for emailjs
  (function() {
    emailjs.init('###########');
  })();

  window.onload = function() {
    document.getElementById('contact-form').addEventListener('submit', function(event) {
        event.preventDefault();
        this.contact_number.value = Math.random() * 100000 | 0;
        emailjs.sendForm('service_rimpjuk', 'template_min7368', this)
            .then(function() {
                console.log('SUCCESS!');
            }, function(error) {
                console.log('FAILED...', error);
            });
    });
}


  return (
    <>
      
      <div className="padding" id="contact"></div>
      <div className="form anchor">
        <p className="section_title">Contact Me</p>
        <form id="contact-form" className="contact_form" method="POST">
            <input type="hidden" name="contact_number" />
            <label for="name">Name</label>
            <input type="text" id="name" name="name" placeholder="Your name..." />
            <br />
            <label for="email">Email</label>
            <input type="text" id="email" name="email" placeholder="Your email..." />
            <br />
            <label for="message">Message</label>
            <textarea id="message" name="message" placeholder="Write something..."></textarea>
            <br />
            <input type="submit" value="Submit" />
        </form>
      </div>
    </>
  )
}

export default Contact