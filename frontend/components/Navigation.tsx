import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Home, GitBranch, Database, Brain, Settings, Box, User, LogOut, CreditCard } from 'lucide-react';

export function Navigation() {
  const location = useLocation();
  const [showProfileMenu, setShowProfileMenu] = React.useState(false);
  
  const links = [
    { path: '/', label: 'Home', icon: Home },
    { path: '/microservices', label: 'Microservices', icon: Box },
    { path: '/datasets', label: 'Datasets', icon: Database },
    { path: '/models', label: 'Models', icon: Brain },
    { path: '/settings', label: 'Settings', icon: Settings },
  ];

  return (
    <nav className="fixed top-0 left-0 right-0 bg-white border-b border-gray-200 z-50">
      <div className="max-w-7xl mx-auto px-6">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center gap-8">
            <Link to="/" className="flex items-center gap-2">
              <div className="w-8 h-8 bg-[#2563EB] rounded-lg flex items-center justify-center">
                <GitBranch className="w-5 h-5 text-white" />
              </div>
              <span className="text-gray-900">MicroLearn</span>
            </Link>
            
            <div className="flex items-center gap-1">
              {links.map((link) => {
                const Icon = link.icon;
                const isActive = location.pathname === link.path;
                return (
                  <Link
                    key={link.path}
                    to={link.path}
                    className={`flex items-center gap-2 px-4 py-2 rounded-lg transition-colors ${
                      isActive
                        ? 'bg-[#2563EB] text-white'
                        : 'text-gray-600 hover:bg-gray-100'
                    }`}
                  >
                    <Icon className="w-4 h-4" />
                    <span className="text-sm">{link.label}</span>
                  </Link>
                );
              })}
            </div>
          </div>
          
          <div className="flex items-center gap-3">
            <div className="relative">
              <button
                onClick={() => setShowProfileMenu(!showProfileMenu)}
                className="w-8 h-8 bg-gradient-to-br from-[#2563EB] to-[#1D4ED8] rounded-full flex items-center justify-center hover:shadow-md transition-shadow"
              >
                <span className="text-sm text-white">AJ</span>
              </button>
              
              {/* Profile Dropdown */}
              {showProfileMenu && (
                <>
                  <div
                    className="fixed inset-0 z-10"
                    onClick={() => setShowProfileMenu(false)}
                  />
                  <div className="absolute right-0 mt-2 w-56 bg-white rounded-xl shadow-lg border border-gray-200 py-2 z-20">
                    <div className="px-4 py-3 border-b border-gray-200">
                      <div className="text-sm text-gray-900">Alex Johnson</div>
                      <div className="text-xs text-gray-600">alex@example.com</div>
                    </div>
                    <Link
                      to="/profile"
                      className="flex items-center gap-3 px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 transition-colors"
                      onClick={() => setShowProfileMenu(false)}
                    >
                      <User className="w-4 h-4" />
                      Profile Settings
                    </Link>
                    <Link
                      to="/profile"
                      className="flex items-center gap-3 px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 transition-colors"
                      onClick={() => setShowProfileMenu(false)}
                    >
                      <CreditCard className="w-4 h-4" />
                      Billing
                    </Link>
                    <div className="border-t border-gray-200 my-2"></div>
                    <Link
                      to="/login"
                      className="flex items-center gap-3 px-4 py-2 text-sm text-red-600 hover:bg-red-50 transition-colors"
                      onClick={() => setShowProfileMenu(false)}
                    >
                      <LogOut className="w-4 h-4" />
                      Sign Out
                    </Link>
                  </div>
                </>
              )}
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
}