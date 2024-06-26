import React, { useState, useEffect } from 'react';
import { Form, Button } from 'react-bootstrap';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const login = () => {

  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate(); // Get the history object to navigate

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      navigate('/'); // Redirect to home page if token exists
    }
  }, []); 

  const handleSubmit = async (event) => {
      event.preventDefault(); // Prevent the default form submission  

      try {
        // Send POST request to API
        const response = await axios.post('http://127.0.0.1:8000/login', {
          username,
          password
        });
  
        // Store token in localStorage
        localStorage.setItem('token', response.data.token);
  
        // Redirect user to home page
        navigate('/');
      } catch (error) {
          console.error(error); // Log any errors
          // Handle error
          console.log("Some error occurred")
      }
  };

  const handleUsernameChange = (event) => {
    setUsername(event.target.value); // Update username state
  };

  const handlePasswordChange = (event) => {
    setPassword(event.target.value); // Update password state
  };

  return (
    <div id="loginContainer">
      <Form id="loginForm" onSubmit={handleSubmit}>
      <Form.Group className="mb-3" controlId="formBasicusername">
        <Form.Label>Username</Form.Label>
        <Form.Control 
          type="text" 
          placeholder="Enter username"
          value={username}
          onChange={handleUsernameChange} // Call handleUsernameChange on change
        />
        <Form.Text className="text-muted">
          We'll never share your username with anyone else.
        </Form.Text>
      </Form.Group>

      <Form.Group className="mb-3" controlId="formBasicPassword">
          <Form.Label>Password</Form.Label>
          <Form.Control
            type="password"
            placeholder="Password"
            value={password}
            onChange={handlePasswordChange} // Call handlePasswordChange on change
          />
        </Form.Group>
      <Button variant="primary" type="submit">
        Submit
      </Button>
    </Form>
  </div>
  )
}

export default login;