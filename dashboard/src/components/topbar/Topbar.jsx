import { FiBell } from "react-icons/fi";
import { Link, useLocation } from "react-router-dom";

function Topbar({ title = "Overview" }) {
  const location = useLocation();

  const pathSegments = location.pathname.split("/").filter(Boolean);

  let cumulativePath = "";
  const breadcrumbLinks = pathSegments.map((segment, idx) => {
    cumulativePath += `/${segment}`;
    const name = segment.charAt(0).toUpperCase() + segment.slice(1);
    return (
      <span key={idx}>
        / <Link to={cumulativePath} className="text-gray-700 hover:underline">{name}</Link>
      </span>
    );
  });

  return (
    <header className="w-full border-b border-gray-300 px-8 py-4 flex items-center justify-between bg-gray-100">
      <div>
        <h1 className="text-2xl font-semibold text-gray-900">{title}</h1>
        <p className="text-sm text-gray-500 mt-1">
          <Link to="/" className="text-gray-700 hover:underline">Dashboard</Link>
          {breadcrumbLinks}
        </p>
      </div>

      <div className="flex items-center gap-4">
        <button className="p-2 rounded-lg bg-gray-200 hover:bg-gray-300 transition relative">
          <FiBell size={18} className="text-gray-700" />
          <span className="absolute top-1 right-1 w-2 h-2 bg-yellow-400 rounded-full"></span>
        </button>

        <div className="relative group">
          <img
            src="https://i.pravatar.cc/40"
            alt="user"
            className="w-9 h-9 rounded-full border border-gray-300 cursor-pointer"
          />

          <div className="absolute right-0 mt-2 w-44 bg-white border border-gray-300 rounded-lg shadow-lg opacity-0 group-hover:opacity-100 pointer-events-none group-hover:pointer-events-auto transition">
            <ul className="py-2 text-gray-700 text-sm">
              <li className="px-4 py-2 hover:bg-gray-100 cursor-pointer">Profile</li>
              <li className="px-4 py-2 hover:bg-gray-100 cursor-pointer">Settings</li>
              <li className="px-4 py-2 hover:bg-red-100 cursor-pointer text-red-600">Logout</li>
            </ul>
          </div>
        </div>
      </div>
    </header>
  );
}

export default Topbar;
