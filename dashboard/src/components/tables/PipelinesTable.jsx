import React, { useState, useMemo } from "react";
import { Link } from "react-router-dom";
import { FaRegTrashCan } from "react-icons/fa6";
import { VscDebugRerun } from "react-icons/vsc";
import { pipelinesDataa, getStatusColor } from "../Variables";


export default function PipelinesTable() {
  const pipelinesData = pipelinesDataa

  const [search, setSearch] = useState("");
  const [statusFilter, setStatusFilter] = useState("");

  const filteredPipelines = useMemo(() => {
    return pipelinesData.filter((p) => {
      const matchesSearch =
        p.name.toLowerCase().includes(search.toLowerCase()) ||
        p.id.toString().includes(search);
      const matchesStatus = statusFilter ? p.status === statusFilter : true;
      return matchesSearch && matchesStatus;
    });
  }, [search, statusFilter]);



  return (
    <div className="bg-white rounded-lg shadow p-6 overflow-x-auto">
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 mb-4">
        <h3 className="text-gray-700 font-semibold text-lg">Pipelines</h3>

        {/* Filters */}
        <div className="flex items-center gap-2">
          <input
            type="text"
            placeholder="Search by ID or Name"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="border border-gray-300 rounded px-3 py-1 focus:outline-none focus:ring-1 focus:ring-yellow-500"
          />

          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="border border-gray-300 rounded px-3 py-1 focus:outline-none focus:ring-1 focus:ring-yellow-500"
          >
            <option value="">All Status</option>
            <option value="Success">Success</option>
            <option value="Failed">Failed</option>
            <option value="Running">Running</option>
            <option value="Queued">Queued</option>
          </select>
        </div>
      </div>

      <table className="min-w-full table-auto border-collapse">
        <thead>
          <tr className="bg-gray-100 text-gray-700">
            <th className="px-4 py-2 text-left">ID</th>
            <th className="px-4 py-2 text-left">Name</th>
            <th className="px-4 py-2 text-left">Status</th>
            <th className="px-4 py-2 text-left">Dataset</th>
            <th className="px-4 py-2 text-left">Steps Completed</th>
            <th className="px-4 py-2 text-left">Start Time</th>
            <th className="px-4 py-2 text-left">Duration</th>
            <th className="px-4 py-2 text-left">Actions</th>
          </tr>
        </thead>
        <tbody>
          {filteredPipelines.length > 0 ? (
            filteredPipelines.map((p) => (
              <tr key={p.id} className="border-b border-gray-200 hover:bg-gray-50">
                <td className="px-4 py-2">
                  <Link
                    to={`/pipelines/${p.id}`}
                    className="hover:underline text-blue-600 transition-all"
                  >
                    #{p.id}
                  </Link>
                </td>
                <td className="px-4 py-2">{p.name}</td>
                <td className="px-4 py-2">
                  <span
                    className={`px-2 py-1 rounded-full text-white text-xs ${getStatusColor(
                      p.status
                    )}`}
                  >
                    {p.status}
                  </span>
                </td>
                <td className="px-4 py-2">
                  <Link
                    to={`/datasets/${p.datasetId}`}
                    className="hover:underline text-blue-600 transition-all"
                  >
                    {p.dataset}
                  </Link>
                </td>
                <td className="px-4 py-2">{p.stepsCompleted}</td>
                <td className="px-4 py-2">{p.startTime}</td>
                <td className="px-4 py-2">{p.duration}</td>
                <td className="px-4 py-2 flex gap-2">
                  <button
                    title="Re-run"
                    onClick={() => alert(`Re-running pipeline #${p.id}`)}
                    className="p-1.5 hover:bg-blue-600/10 transition-all rounded text-blue-600 hover:underline"
                  >
                    <VscDebugRerun size={22} />
                  </button>
                  <button
                    title="Delete"
                    onClick={() => {
                      if (window.confirm(`Are you sure to delete pipeline #${p.id}?`)) {
                        alert(`Deleted pipeline #${p.id}`);
                      }
                    }}
                    className="p-1.5 hover:bg-red-600/10 transition-all rounded text-red-600 hover:underline"
                  >
                    <FaRegTrashCan size={19} />
                  </button>
                </td>
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan="9" className="text-center py-4 text-gray-500">
                No pipelines found.
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}
