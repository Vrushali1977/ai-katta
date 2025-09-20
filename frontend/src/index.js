import React from 'react';
import ReactDOM from 'react-dom/client';
import './App.css'; // Import the Tailwind-processed CSS
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
