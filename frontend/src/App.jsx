import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import ChatPage from "./components/ChatPage";
import FineTunePage from "./components/FineTunePage";
import Navbar from "./components/NavBar";

export default function App() {
  return (
    <React.StrictMode>
      <Router>
        <Navbar />
        <Routes>
          <Route path="/" element={<ChatPage />} />
          <Route path="/chat" element={<ChatPage />} />
          <Route path="/finetune" element={<FineTunePage />} />
        </Routes>
      </Router>
    </React.StrictMode>
  );
}
