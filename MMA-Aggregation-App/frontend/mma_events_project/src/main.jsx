import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App.jsx";
import FetchCall from "./hooks/hook.jsx"
import "./index.css";
import Calendar from "./components/Calendar.jsx";

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <Calendar />
  </React.StrictMode>
);