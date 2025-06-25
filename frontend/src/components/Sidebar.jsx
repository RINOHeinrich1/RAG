import { useState } from "react";
import { Link, useLocation } from "react-router-dom";
import { MessageSquare, Cpu, BookOpen } from "lucide-react";

export default function Sidebar() {
  const { pathname } = useLocation();
  const [expanded, setExpanded] = useState(false);

  // Pour gérer le style actif du lien
  const isActive = (path) =>
    pathname === path
      ? "bg-indigo-700 text-white font-semibold"
      : "text-indigo-300 hover:bg-indigo-600 hover:text-white";

  // Les items avec icône + label + route
  const menuItems = [
    { label: "Chat", icon: MessageSquare, to: "/chat" },
    { label: "Fine-Tune", icon: Cpu, to: "/finetune" },
    { label: "Documents", icon: BookOpen, to: "/docs" },
  ];

  return (
   <nav
  onMouseEnter={() => setExpanded(true)}
  onMouseLeave={() => setExpanded(false)}
  className={`
    fixed left-4
    top-1/2
    -translate-y-1/2  // Remonte de la moitié de la hauteur
    flex flex-col
    bg-indigo-800 text-indigo-300
    rounded-xl
    shadow-lg
    transition-[width] duration-300 ease-in-out
    overflow-hidden
    ${expanded ? "w-48" : "w-16"}
    h-auto  // hauteur automatique pour adapter au contenu
    z-50
  `}
  aria-label="Sidebar de navigation"
>
  {menuItems.map(({ label, icon: Icon, to }) => (
    <Link
      to={to}
      key={to}
      className={`flex items-center gap-4 px-4 py-3 cursor-pointer select-none transition-colors rounded-lg mx-2 my-1 ${
        isActive(to)
      }`}
    >
      <Icon className="w-6 h-6" aria-hidden="true" />
      {expanded && <span className="whitespace-nowrap">{label}</span>}
    </Link>
  ))}
</nav>

  );
}
