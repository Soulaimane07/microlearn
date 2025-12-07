import React, { useMemo, useState } from "react";
import { useSelector, useDispatch } from "react-redux";
import { Link } from "react-router-dom";
import { FaRegTrashCan } from "react-icons/fa6";
import { VscDebugRerun, VscRunErrors } from "react-icons/vsc";
import { getStatusColor } from "../Variables";
import { deletePipeline, rerunPipeline, stopPipeline } from "../../redux/slices/pipelinesSlice";
import AddPipelineForm from "../../pages/pipelines/AddPipelineForm";
import Modal from "../Modal";


export default function PipelinesTable() {
  const pipelines = useSelector(state => state.pipelines.list);
  const datasets = useSelector(state => state.datasets.list);

  const dispatch = useDispatch();

  const [search, setSearch] = useState("");
  const [statusFilter, setStatusFilter] = useState("");
  const [isModalOpen, setIsModalOpen] = useState(false);

  const filteredPipelines = useMemo(() => {
    return pipelines.filter((p) => {
      const matchesSearch =
        p.name.toLowerCase().includes(search.toLowerCase()) ||
        p.id.toString().includes(search);
      const matchesStatus = statusFilter ? p.status === statusFilter : true;
      return matchesSearch && matchesStatus;
    });
  }, [pipelines, search, statusFilter]);

  return (
    <div className="bg-white rounded-lg shadow p-6 overflow-x-auto">
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 mb-4">
        <h3 className="text-gray-700 font-semibold text-lg">Pipelines</h3>
        <div className="flex items-center gap-2">
          <input
            type="text"
            placeholder="Search by ID or Name"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="border border-gray-300 rounded px-3 py-1.5 focus:outline-none focus:ring-1 focus:ring-yellow-500"
          />
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="border border-gray-300 rounded px-5 py-1.5 focus:outline-none focus:ring-1 focus:ring-yellow-500"
          >
            <option value="">All Status</option>
            <option value="Success">Success</option>
            <option value="Failed">Failed</option>
            <option value="Running">Running</option>
            <option value="Queued">Queued</option>
          </select>
          <button
            onClick={() => setIsModalOpen(true)}
            className="bg-yellow-600 text-white px-6 py-1.5 rounded hover:bg-yellow-700 transition"
          >
            Add Pipeline
          </button>
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
            filteredPipelines.map(p => (
              <tr key={p.id} className="border-b border-gray-200 hover:bg-gray-50 transition-all">
                <td className="px-4 py-2">
                  <Link to={`/pipelines/${p.id}`} className="hover:underline text-blue-600">
                    #{p.id}
                  </Link>
                </td>
                <td className="px-4 py-2">{p.name}</td>
                <td className="px-4 py-2">
                  <span className={`px-2 py-1 rounded-full text-white text-xs ${getStatusColor(p.status)}`}>
                    {p.status}
                  </span>
                </td>
                <td className="px-4 py-2"> <Link to={`/datasets/${datasets.find(d => d.id === p.datasetId)?.id}`} className="hover:underline transition-all text-blue-600"> {datasets.find(d => d.id === p.datasetId)?.name || "Unknown"} </Link> </td>
                <td className="px-4 py-2">{p.stepsCompleted}</td>
                <td className="px-4 py-2">{p.startTime}</td>
                <td className="px-4 py-2">{p.duration}</td>
                <td className="px-4 py-2 flex gap-2">
                  {p.status === "Running" ? (
                    <button
                      title="Stop"
                      onClick={() => dispatch(stopPipeline(p.id))}
                      className="p-1.5 hover:bg-red-600/10 transition-all rounded text-red-600"
                    >
                      <VscRunErrors size={22} />
                    </button>
                  ) : (
                    <button
                      title="Re-run"
                      onClick={() => dispatch(rerunPipeline(p.id))}
                      className="p-1.5 hover:bg-blue-600/10 transition-all rounded text-blue-600"
                    >
                      <VscDebugRerun size={22} />
                    </button>
                  )}

                  <button
                    title="Delete"
                    onClick={() => dispatch(deletePipeline(p.id))}
                    className="p-1.5 hover:bg-red-600/10 transition-all rounded text-red-600"
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

      {/* Modal */}
      <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} title="Add New Pipeline">
        <AddPipelineForm onClose={() => setIsModalOpen(false)} />
      </Modal>
    </div>
  );
}
