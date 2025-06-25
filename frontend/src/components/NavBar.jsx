import { Link, useLocation } from "react-router-dom";

export default function NavBar() {
  const { pathname } = useLocation();

  const isActive = (path) =>
    pathname === path ? "text-white font-semibold underline" : "text-indigo-100 hover:text-white";

  return (
    <nav className="bg-indigo-700 text-white px-6 py-4 shadow-md font-inter">
      <div className="max-w-6xl mx-auto flex items-center justify-between">
        <div className="text-2xl font-bold text-white tracking-tight">
          🤖 ONIR Chat
        </div>
        <div className="space-x-6 text-sm sm:text-base">
          <Link to="/chat" className={isActive("/chat")}>
            💬 Chat
          </Link>
          <Link to="/finetune" className={isActive("/finetune")}>
            🧠 Fine-Tune
          </Link>
          <Link to="/docs" className={isActive("/docs")}>
            📚 Documents
          </Link>
        </div>
      </div>
    </nav>
  );
}
