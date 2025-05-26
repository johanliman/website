---
layout: page
title: Contact Me
permalink: /contact/
---


<form action="https://formspree.io/f/xldbykny" method="POST">
  <div>
    <label for="name">Name*</label>
    <input type="text" id="name" name="name" placeholder="Name*" required>
  </div>

  <div>
    <label for="email">Email Address*</label>
    <input type="email" id="email" name="email" placeholder="Email Address*" required>
  </div>

  <div>
    <label for="subject">Subject*</label>
    <input type="text" id="subject" name="subject" placeholder="Subject*" required>
  </div>

  <div>
    <label for="comments">Comments*</label>
    <textarea id="comments" name="message" placeholder="Comments*" rows="5" required></textarea>
  </div>

  <button type="submit">Send</button>
</form>

<style>
  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol"; /* Common system font stack */
    margin: 0; /* Remove default body margin if page layout handles it */
    padding: 20px; /* Add some padding around the whole page content if needed */
    background-color: #fff; 
  }

  h1 {
    font-size: 2.5em; /* Larger heading */
    font-weight: 600;
    margin-bottom: 30px; /* Space below heading */
    color: #333;
  }

  form {
    background-color: #fff;
    padding: 30px; /* Increased padding inside the form */
    border-radius: 8px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1); /* Adjusted shadow for a bit more depth */
    max-width: 700px; /* Form is wider */
    /* margin-left: auto; and margin-right: auto; removed for left alignment within parent */
    margin-top: 20px; /* Space above the form, below H1 */
    margin-bottom: 20px; /* Space below the form */
  }

  div {
    margin-bottom: 20px; /* Increased space between fields */
  }

  label {
    display: block;
    margin-bottom: 8px; /* Space between label and input */
    font-weight: bold; /* Kept bold as in screenshot */
    font-size: 0.95em; /* Slightly adjusted size */
    color: #333;
  }

  input[type="text"],
  input[type="email"],
  textarea { /* select removed as it's not in this version of the form */
    width: 100%;
    padding: 12px; /* Increased padding */
    border: 1px solid #ccc; 
    border-radius: 6px; /* Slightly more rounded corners like screenshot */
    box-sizing: border-box;
    font-size: 1rem; /* Standard font size */
    color: #333;
  }

  input[type="text"]::placeholder,
  input[type="email"]::placeholder,
  textarea::placeholder {
    color: #999; 
  }

  textarea {
    resize: vertical;
    min-height: 120px; /* Give textarea a good default minimum height */
  }

  button[type="submit"] {
    background-color: #007bff;
    color: white;
    padding: 12px 25px; /* Adjusted padding */
    border: none;
    border-radius: 6px; /* Consistent border-radius */
    cursor: pointer;
    font-size: 1rem; /* Standard font size */
    font-weight: 500;
    transition: background-color 0.2s;
  }

  button[type="submit"]:hover {
    background-color: #0056b3;
  }
</style>