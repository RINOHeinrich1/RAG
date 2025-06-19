import axios from 'axios';

const api = axios.create({
  baseURL: "http://localhost:8000", // Assure-toi que le backend tourne ici
});

export const askQuestion = async (question) => {
  const response = await api.post("/ask", { question });
  return response.data;
};
