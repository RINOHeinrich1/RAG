import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import ChatPage from "./components/ChatPage";
import FineTunePage from "./components/FineTunePage";
import Navbar from "./components/NavBar";
import DocumentManager from "./components/DocumentManagement";

export default function App() {
  return (
    <React.StrictMode>
      <Router>
        <Navbar />
        <Routes>
          <Route path="/" element={<ChatPage />} />
          <Route path="/chat" element={<ChatPage />} />
          <Route path="/finetune" element={<FineTunePage />} />
          <Route path="/docs" element={<DocumentManager />} />
        </Routes>
      </Router>
    </React.StrictMode>
  );
}
