import React from "react";
import { Link, NavLink } from "react-router-dom";
import {
  MdHome,
  MdModelTraining,
  MdDataset
} from "react-icons/md";
import { FiGitMerge, FiCpu, FiBox } from "react-icons/fi";

function Sidebar() {
  const pages = [
    { title: "Overview", icon: <MdHome size={22} />, path: "/" },
    { title: "Pipelines", icon: <FiGitMerge size={22} />, path: "/pipelines" },
    { title: "Experiments", icon: <FiCpu size={22} />, path: "/experiments" },
    { title: "Models", icon: <MdModelTraining size={22} />, path: "/models" },
    { title: "Deployments", icon: <FiBox size={22} />, path: "/deployments" },
    { title: "Datasets", icon: <MdDataset size={22} />, path: "/datasets" },
  ];

  return (
    <nav className="bg-gray-950 px-2 text-gray-100 w-62 h-screen sticky top-0 flex flex-col py-8 border-r border-gray-800">
      
      {/* Logo */}
      <Link to="/" className="px-6 mb-10 block">
        <h1 className="text-2xl font-bold tracking-tight">MicroLearn</h1>
        <p className="text-xs text-gray-400 tracking-wide ml-1">AutoML Platform</p>
      </Link>

      {/* Menu */}
      <ul className="flex flex-col gap-1">
        {pages.map((item, idx) => (
          <NavLink
            key={idx}
            to={item.path}
            className={({ isActive }) =>
              `flex items-center gap-3 px-6 py-3 rounded-lg transition-all 
              ${isActive ? "bg-yellow-500 text-gray-900 font-semibold" : "text-gray-300 hover:bg-gray-800"}`
            }
          >
            <span>{item.icon}</span>
            <span className="font-medium">{item.title}</span>
          </NavLink>
        ))}
      </ul>

      {/* Footer small */}
      <div className="mt-auto px-6 pt-6 text-xs text-center text-gray-500">
        © 2025 MicroLearn
      </div>
    </nav>
  );
}

export default Sidebar;
