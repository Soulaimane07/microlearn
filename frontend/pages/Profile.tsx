import React, { useState } from 'react';
import { 
  User, 
  Mail, 
  Building, 
  MapPin, 
  Phone, 
  Calendar,
  Camera,
  Save,
  Key,
  Bell,
  Shield,
  CreditCard,
  Users,
  Activity
} from 'lucide-react';

export function Profile() {
  const [activeTab, setActiveTab] = useState('general');
  const [profileData, setProfileData] = useState({
    fullName: 'Alex Johnson',
    email: 'alex.johnson@example.com',
    organization: 'ML Innovations Inc.',
    role: 'ML Engineer',
    location: 'San Francisco, CA',
    phone: '+1 (555) 123-4567',
    bio: 'Machine Learning Engineer passionate about building scalable ML pipelines and automating workflows.',
    joinDate: 'January 15, 2024',
  });

  const [notifications, setNotifications] = useState({
    emailNotifications: true,
    pipelineAlerts: true,
    weeklyReports: false,
    systemUpdates: true,
  });

  const tabs = [
    { id: 'general', label: 'General', icon: User },
    { id: 'security', label: 'Security', icon: Shield },
    { id: 'notifications', label: 'Notifications', icon: Bell },
    { id: 'billing', label: 'Billing', icon: CreditCard },
    { id: 'team', label: 'Team', icon: Users },
  ];

  const stats = [
    { label: 'Pipelines Created', value: '42', icon: Activity, color: 'bg-blue-100 text-blue-600' },
    { label: 'Models Trained', value: '156', icon: Activity, color: 'bg-teal-100 text-teal-600' },
    { label: 'Active Services', value: '8', icon: Activity, color: 'bg-purple-100 text-purple-600' },
    { label: 'Team Members', value: '12', icon: Users, color: 'bg-orange-100 text-orange-600' },
  ];

  return (
    <div className="min-h-screen bg-[#F5F6FA] px-6 py-8">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl text-gray-900 mb-2">Account Settings</h1>
          <p className="text-gray-600">Manage your profile and account preferences</p>
        </div>

        {/* Profile Header Card */}
        <div className="bg-white rounded-2xl shadow-sm border border-gray-200 p-8 mb-6">
          <div className="flex items-start gap-6">
            {/* Avatar */}
            <div className="relative group">
              <div className="w-24 h-24 bg-gradient-to-br from-[#2563EB] to-[#1D4ED8] rounded-2xl flex items-center justify-center">
                <span className="text-3xl text-white">AJ</span>
              </div>
              <button className="absolute bottom-0 right-0 w-8 h-8 bg-white border-2 border-gray-200 rounded-lg flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity shadow-sm">
                <Camera className="w-4 h-4 text-gray-600" />
              </button>
            </div>

            {/* Profile Info */}
            <div className="flex-1">
              <h2 className="text-2xl text-gray-900 mb-1">{profileData.fullName}</h2>
              <p className="text-gray-600 mb-4">{profileData.role} at {profileData.organization}</p>
              <div className="flex flex-wrap gap-4 text-sm text-gray-600">
                <div className="flex items-center gap-2">
                  <Mail className="w-4 h-4" />
                  <span>{profileData.email}</span>
                </div>
                <div className="flex items-center gap-2">
                  <MapPin className="w-4 h-4" />
                  <span>{profileData.location}</span>
                </div>
                <div className="flex items-center gap-2">
                  <Calendar className="w-4 h-4" />
                  <span>Joined {profileData.joinDate}</span>
                </div>
              </div>
            </div>
          </div>

          {/* Stats Grid */}
          <div className="grid grid-cols-4 gap-4 mt-8 pt-8 border-t border-gray-200">
            {stats.map((stat) => {
              const Icon = stat.icon;
              return (
                <div key={stat.label} className="text-center">
                  <div className={`inline-flex items-center justify-center w-12 h-12 ${stat.color} rounded-xl mb-2`}>
                    <Icon className="w-5 h-5" />
                  </div>
                  <div className="text-2xl text-gray-900 mb-1">{stat.value}</div>
                  <div className="text-sm text-gray-600">{stat.label}</div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Tabs & Content */}
        <div className="grid grid-cols-12 gap-6">
          {/* Sidebar Tabs */}
          <div className="col-span-3">
            <div className="bg-white rounded-2xl shadow-sm border border-gray-200 p-2">
              {tabs.map((tab) => {
                const Icon = tab.icon;
                return (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id)}
                    className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-colors text-left ${
                      activeTab === tab.id
                        ? 'bg-[#2563EB] text-white'
                        : 'text-gray-600 hover:bg-gray-100'
                    }`}
                  >
                    <Icon className="w-5 h-5" />
                    <span className="text-sm">{tab.label}</span>
                  </button>
                );
              })}
            </div>
          </div>

          {/* Content Area */}
          <div className="col-span-9">
            <div className="bg-white rounded-2xl shadow-sm border border-gray-200 p-8">
              {/* General Tab */}
              {activeTab === 'general' && (
                <div>
                  <h3 className="text-xl text-gray-900 mb-6">General Information</h3>
                  <div className="space-y-5">
                    <div className="grid grid-cols-2 gap-5">
                      <div>
                        <label className="block text-sm text-gray-700 mb-2">Full Name</label>
                        <input
                          type="text"
                          value={profileData.fullName}
                          onChange={(e) => setProfileData({ ...profileData, fullName: e.target.value })}
                          className="w-full px-4 py-3 bg-white border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#2563EB] focus:border-transparent transition-all"
                        />
                      </div>
                      <div>
                        <label className="block text-sm text-gray-700 mb-2">Email Address</label>
                        <input
                          type="email"
                          value={profileData.email}
                          onChange={(e) => setProfileData({ ...profileData, email: e.target.value })}
                          className="w-full px-4 py-3 bg-white border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#2563EB] focus:border-transparent transition-all"
                        />
                      </div>
                    </div>

                    <div className="grid grid-cols-2 gap-5">
                      <div>
                        <label className="block text-sm text-gray-700 mb-2">Organization</label>
                        <input
                          type="text"
                          value={profileData.organization}
                          onChange={(e) => setProfileData({ ...profileData, organization: e.target.value })}
                          className="w-full px-4 py-3 bg-white border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#2563EB] focus:border-transparent transition-all"
                        />
                      </div>
                      <div>
                        <label className="block text-sm text-gray-700 mb-2">Role</label>
                        <input
                          type="text"
                          value={profileData.role}
                          onChange={(e) => setProfileData({ ...profileData, role: e.target.value })}
                          className="w-full px-4 py-3 bg-white border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#2563EB] focus:border-transparent transition-all"
                        />
                      </div>
                    </div>

                    <div className="grid grid-cols-2 gap-5">
                      <div>
                        <label className="block text-sm text-gray-700 mb-2">Location</label>
                        <input
                          type="text"
                          value={profileData.location}
                          onChange={(e) => setProfileData({ ...profileData, location: e.target.value })}
                          className="w-full px-4 py-3 bg-white border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#2563EB] focus:border-transparent transition-all"
                        />
                      </div>
                      <div>
                        <label className="block text-sm text-gray-700 mb-2">Phone Number</label>
                        <input
                          type="tel"
                          value={profileData.phone}
                          onChange={(e) => setProfileData({ ...profileData, phone: e.target.value })}
                          className="w-full px-4 py-3 bg-white border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#2563EB] focus:border-transparent transition-all"
                        />
                      </div>
                    </div>

                    <div>
                      <label className="block text-sm text-gray-700 mb-2">Bio</label>
                      <textarea
                        value={profileData.bio}
                        onChange={(e) => setProfileData({ ...profileData, bio: e.target.value })}
                        rows={4}
                        className="w-full px-4 py-3 bg-white border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#2563EB] focus:border-transparent transition-all resize-none"
                      />
                    </div>

                    <div className="flex justify-end pt-4">
                      <button className="flex items-center gap-2 px-6 py-3 bg-[#2563EB] text-white rounded-lg hover:bg-[#1D4ED8] transition-colors">
                        <Save className="w-4 h-4" />
                        Save Changes
                      </button>
                    </div>
                  </div>
                </div>
              )}

              {/* Security Tab */}
              {activeTab === 'security' && (
                <div>
                  <h3 className="text-xl text-gray-900 mb-6">Security Settings</h3>
                  <div className="space-y-6">
                    {/* Change Password */}
                    <div className="p-6 bg-gray-50 rounded-xl">
                      <div className="flex items-start gap-4">
                        <div className="w-12 h-12 bg-[#2563EB] bg-opacity-10 rounded-xl flex items-center justify-center flex-shrink-0">
                          <Key className="w-6 h-6 text-[#2563EB]" />
                        </div>
                        <div className="flex-1">
                          <h4 className="text-gray-900 mb-1">Change Password</h4>
                          <p className="text-sm text-gray-600 mb-4">Update your password to keep your account secure</p>
                          <button className="px-4 py-2 bg-white border border-gray-300 rounded-lg text-sm text-gray-700 hover:bg-gray-50 transition-colors">
                            Update Password
                          </button>
                        </div>
                      </div>
                    </div>

                    {/* Two-Factor Authentication */}
                    <div className="p-6 bg-gray-50 rounded-xl">
                      <div className="flex items-start gap-4">
                        <div className="w-12 h-12 bg-teal-500 bg-opacity-10 rounded-xl flex items-center justify-center flex-shrink-0">
                          <Shield className="w-6 h-6 text-teal-600" />
                        </div>
                        <div className="flex-1">
                          <h4 className="text-gray-900 mb-1">Two-Factor Authentication</h4>
                          <p className="text-sm text-gray-600 mb-4">Add an extra layer of security to your account</p>
                          <button className="px-4 py-2 bg-[#2563EB] text-white rounded-lg text-sm hover:bg-[#1D4ED8] transition-colors">
                            Enable 2FA
                          </button>
                        </div>
                      </div>
                    </div>

                    {/* Active Sessions */}
                    <div>
                      <h4 className="text-gray-900 mb-4">Active Sessions</h4>
                      <div className="space-y-3">
                        {[
                          { device: 'MacBook Pro', location: 'San Francisco, CA', time: 'Current session', current: true },
                          { device: 'iPhone 14', location: 'San Francisco, CA', time: '2 hours ago', current: false },
                        ].map((session, index) => (
                          <div key={index} className="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
                            <div>
                              <div className="text-gray-900 mb-1">{session.device}</div>
                              <div className="text-sm text-gray-600">{session.location} • {session.time}</div>
                            </div>
                            {!session.current && (
                              <button className="text-sm text-red-600 hover:text-red-700">Revoke</button>
                            )}
                            {session.current && (
                              <span className="px-3 py-1 bg-green-100 text-green-700 text-xs rounded-full">Active</span>
                            )}
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {/* Notifications Tab */}
              {activeTab === 'notifications' && (
                <div>
                  <h3 className="text-xl text-gray-900 mb-6">Notification Preferences</h3>
                  <div className="space-y-4">
                    {[
                      { key: 'emailNotifications', label: 'Email Notifications', description: 'Receive notifications via email' },
                      { key: 'pipelineAlerts', label: 'Pipeline Alerts', description: 'Get notified about pipeline status changes' },
                      { key: 'weeklyReports', label: 'Weekly Reports', description: 'Receive weekly performance summaries' },
                      { key: 'systemUpdates', label: 'System Updates', description: 'Stay informed about system updates and maintenance' },
                    ].map((item) => (
                      <div key={item.key} className="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
                        <div>
                          <div className="text-gray-900 mb-1">{item.label}</div>
                          <div className="text-sm text-gray-600">{item.description}</div>
                        </div>
                        <label className="relative inline-flex items-center cursor-pointer">
                          <input
                            type="checkbox"
                            checked={notifications[item.key as keyof typeof notifications]}
                            onChange={(e) => setNotifications({ ...notifications, [item.key]: e.target.checked })}
                            className="sr-only peer"
                          />
                          <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-[#2563EB]"></div>
                        </label>
                      </div>
                    ))}
                  </div>
                  <div className="flex justify-end pt-6">
                    <button className="flex items-center gap-2 px-6 py-3 bg-[#2563EB] text-white rounded-lg hover:bg-[#1D4ED8] transition-colors">
                      <Save className="w-4 h-4" />
                      Save Preferences
                    </button>
                  </div>
                </div>
              )}

              {/* Billing Tab */}
              {activeTab === 'billing' && (
                <div>
                  <h3 className="text-xl text-gray-900 mb-6">Billing & Subscription</h3>
                  <div className="space-y-6">
                    {/* Current Plan */}
                    <div className="p-6 bg-gradient-to-br from-[#2563EB] to-[#1D4ED8] rounded-xl text-white">
                      <div className="flex items-start justify-between mb-4">
                        <div>
                          <h4 className="text-xl mb-2">Professional Plan</h4>
                          <p className="text-blue-100">Unlimited pipelines and team collaboration</p>
                        </div>
                        <span className="px-4 py-2 bg-white bg-opacity-20 rounded-lg">$49/month</span>
                      </div>
                      <button className="px-4 py-2 bg-white text-[#2563EB] rounded-lg text-sm hover:bg-opacity-90 transition-colors">
                        Upgrade Plan
                      </button>
                    </div>

                    {/* Payment Method */}
                    <div>
                      <h4 className="text-gray-900 mb-4">Payment Method</h4>
                      <div className="p-4 border border-gray-200 rounded-lg flex items-center justify-between">
                        <div className="flex items-center gap-4">
                          <div className="w-12 h-8 bg-gray-900 rounded flex items-center justify-center text-white text-xs">
                            VISA
                          </div>
                          <div>
                            <div className="text-gray-900">•••• •••• •••• 4242</div>
                            <div className="text-sm text-gray-600">Expires 12/25</div>
                          </div>
                        </div>
                        <button className="text-sm text-[#2563EB] hover:text-[#1D4ED8]">Update</button>
                      </div>
                    </div>

                    {/* Billing History */}
                    <div>
                      <h4 className="text-gray-900 mb-4">Billing History</h4>
                      <div className="space-y-2">
                        {[
                          { date: 'Dec 1, 2024', amount: '$49.00', status: 'Paid' },
                          { date: 'Nov 1, 2024', amount: '$49.00', status: 'Paid' },
                          { date: 'Oct 1, 2024', amount: '$49.00', status: 'Paid' },
                        ].map((invoice, index) => (
                          <div key={index} className="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
                            <div className="flex items-center gap-8">
                              <span className="text-gray-900">{invoice.date}</span>
                              <span className="text-gray-900">{invoice.amount}</span>
                            </div>
                            <div className="flex items-center gap-4">
                              <span className="px-3 py-1 bg-green-100 text-green-700 text-xs rounded-full">{invoice.status}</span>
                              <button className="text-sm text-[#2563EB] hover:text-[#1D4ED8]">Download</button>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {/* Team Tab */}
              {activeTab === 'team' && (
                <div>
                  <div className="flex items-center justify-between mb-6">
                    <h3 className="text-xl text-gray-900">Team Members</h3>
                    <button className="px-4 py-2 bg-[#2563EB] text-white rounded-lg text-sm hover:bg-[#1D4ED8] transition-colors">
                      Invite Member
                    </button>
                  </div>
                  <div className="space-y-3">
                    {[
                      { name: 'Alex Johnson', email: 'alex@example.com', role: 'Owner', avatar: 'AJ' },
                      { name: 'Sarah Chen', email: 'sarah@example.com', role: 'Admin', avatar: 'SC' },
                      { name: 'Mike Davis', email: 'mike@example.com', role: 'Member', avatar: 'MD' },
                      { name: 'Emily Wilson', email: 'emily@example.com', role: 'Member', avatar: 'EW' },
                    ].map((member, index) => (
                      <div key={index} className="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
                        <div className="flex items-center gap-4">
                          <div className="w-10 h-10 bg-gradient-to-br from-[#2563EB] to-[#1D4ED8] rounded-lg flex items-center justify-center text-white">
                            {member.avatar}
                          </div>
                          <div>
                            <div className="text-gray-900">{member.name}</div>
                            <div className="text-sm text-gray-600">{member.email}</div>
                          </div>
                        </div>
                        <div className="flex items-center gap-4">
                          <span className="px-3 py-1 bg-gray-100 text-gray-700 text-sm rounded-lg">{member.role}</span>
                          {member.role !== 'Owner' && (
                            <button className="text-sm text-gray-600 hover:text-gray-900">Edit</button>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
