import Sidebar from "../../components/sidebar/Sidebar";
import Topbar from "../../components/topbar/Topbar";
import Footer from "../../components/footer/Footer";
import { PieChart, Pie, Cell, LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid, BarChart, Bar } from "recharts";

const kpiData = [
  { title: "Total Pipelines", value: 132, subtext: "+12 this week" },
  { title: "Experiments Completed", value: 458, subtext: "Latest: 94% accuracy" },
  { title: "Active Deployments", value: 7, status: "healthy" },
  { title: "GPU Utilization", value: 62, subtext: "NVIDIA T4 GPU" },
];

const pipelineStatusData = [
  { name: "Success", value: 60 },
  { name: "Failed", value: 10 },
  { name: "Running", value: 20 },
  { name: "Queued", value: 10 },
];

const experimentsOverTime = Array.from({ length: 30 }, (_, i) => ({
  date: `Day ${i + 1}`,
  count: Math.floor(Math.random() * 20) + 5,
}));

const gpuUsageData = Array.from({ length: 30 }, (_, i) => ({
  time: `T${i}`,
  usage: Math.floor(Math.random() * 100),
}));

const recentPipelines = [
  { id: 452, status: "Success", duration: "03:12", dataset: "credit-default.csv", createdBy: "Soulaimane" },
  { id: 453, status: "Failed", duration: "01:45", dataset: "loans.csv", createdBy: "Ali" },
  { id: 454, status: "Running", duration: "00:55", dataset: "fraud.csv", createdBy: "Amal" },
  { id: 455, status: "Queued", duration: "-", dataset: "transactions.csv", createdBy: "Soulaimane" },
  { id: 456, status: "Success", duration: "02:33", dataset: "clients.csv", createdBy: "Ali" },
];

const bestModel = {
  type: "XGBoostClassifier",
  f1: 0.942,
  dataset: "fraud.csv",
  trainingTime: "2m 43s",
  scores: [
    { model: "XGBoost", score: 0.942 },
    { model: "RandomForest", score: 0.912 },
    { model: "LightGBM", score: 0.895 },
  ],
};

const COLORS = ["#22c55e", "#ef4444", "#3b82f6", "#facc15"];

export default function Overview() {
  return (
    <div className="flex min-h-screen bg-gray-100 text-gray-900">
      <Sidebar />

      <div className="flex-1 flex flex-col">
        <Topbar title="Overview" />

        <main className="flex-1 p-8 space-y-8">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {kpiData.map((kpi, idx) => (
              <div key={idx} className="bg-white rounded-lg shadow p-6 flex flex-col justify-between">
                <h2 className="text-gray-500 text-sm">{kpi.title}</h2>
                <p className="text-2xl font-bold text-gray-900">{kpi.value}{kpi.status === undefined ? "" : ` ${kpi.status === "healthy" ? "🟢" : kpi.status === "degraded" ? "🟡" : "🔴"}`}</p>
                <span className="text-gray-500 text-sm">{kpi.subtext}</span>
              </div>
            ))}
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-gray-700 font-semibold mb-4">Pipeline Status Distribution</h3>
              <PieChart width={250} height={250}>
                <Pie data={pipelineStatusData} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={80} label>
                  {pipelineStatusData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </div>

            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-gray-700 font-semibold mb-4">Experiments Over Time</h3>
              <LineChart width={300} height={250} data={experimentsOverTime}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" hide />
                <YAxis />
                <Tooltip />
                <Line type="monotone" dataKey="count" stroke="#3b82f6" strokeWidth={2} />
              </LineChart>
            </div>

            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-gray-700 font-semibold mb-4">GPU Usage Over Time</h3>
              <LineChart width={300} height={250} data={gpuUsageData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="time" hide />
                <YAxis />
                <Tooltip />
                <Line type="monotone" dataKey="usage" stroke="#facc15" strokeWidth={2} />
              </LineChart>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6 overflow-x-auto">
            <h3 className="text-gray-700 font-semibold mb-4">Recent Pipelines</h3>
            <table className="min-w-full table-auto">
              <thead>
                <tr className="bg-gray-100 text-gray-700">
                  <th className="px-4 py-2 text-left">ID</th>
                  <th className="px-4 py-2 text-left">Status</th>
                  <th className="px-4 py-2 text-left">Duration</th>
                  <th className="px-4 py-2 text-left">Dataset</th>
                  <th className="px-4 py-2 text-left">Created By</th>
                  <th className="px-4 py-2 text-left">Action</th>
                </tr>
              </thead>
              <tbody>
                {recentPipelines.map((p, idx) => (
                  <tr key={idx} className="border-b border-gray-200">
                    <td className="px-4 py-2">#{p.id}</td>
                    <td className="px-4 py-2">
                      <span className={`px-2 py-1 rounded-full text-white text-xs ${p.status === "Success" ? "bg-green-500" : p.status === "Failed" ? "bg-red-500" : p.status === "Running" ? "bg-blue-500" : "bg-yellow-400"}`}>
                        {p.status}
                      </span>
                    </td>
                    <td className="px-4 py-2">{p.duration}</td>
                    <td className="px-4 py-2">{p.dataset}</td>
                    <td className="px-4 py-2">{p.createdBy}</td>
                    <td className="px-4 py-2"><button className="text-blue-600 hover:underline">View</button></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <div className="bg-white rounded-lg shadow p-6 flex flex-col md:flex-row justify-between items-center">
            <div>
              <h3 className="text-gray-700 font-semibold">{bestModel.type}</h3>
              <p className="text-gray-500">F1 = {bestModel.f1}</p>
              <p className="text-gray-500">Dataset: {bestModel.dataset}</p>
              <p className="text-gray-500">Training time: {bestModel.trainingTime}</p>
              <button className="mt-2 px-4 py-2 bg-yellow-500 text-white rounded hover:bg-yellow-600">View Model</button>
            </div>
            <div className="w-full md:w-48 h-32 mt-4 md:mt-0">
              <BarChart width={200} height={150} data={bestModel.scores}>
                <XAxis dataKey="model" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="score" fill="#3b82f6" />
              </BarChart>
            </div>
          </div>
        </main>
        <Footer />
      </div>
    </div>
  );
}
