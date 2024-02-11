import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);

document.body.style.backgroundColor = "rgb(16, 20, 24)";
document.body.style.color = "white";
document.body.style.margin = "0";

root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
