import { Link } from "react-router-dom";

export default function NavBar() {
  return (
    <nav className="bg-blue-700 text-white p-4 flex justify-between">
      <div className="font-bold text-xl">ONIR Chat</div>
      <div className="space-x-4">
        <Link to="/chat" className="hover:underline">Chat</Link>
        <Link to="/finetune" className="hover:underline">Fine-Tune</Link>
      </div>
    </nav>
  );
}
