import React, { useMemo, useState } from "react";
import { useSelector, useDispatch } from "react-redux";
import { deleteDataset } from "../../redux/slices/datasetsSlice";
import { FaRegTrashCan } from "react-icons/fa6";
import { Link } from "react-router-dom";

export default function DatasetsTable({setIsModalOpen}) {
  const datasets = useSelector(state => state.datasets.list);
  const dispatch = useDispatch();
  const [search, setSearch] = useState("");

  const filteredDatasets = useMemo(() => {
    return datasets.filter(d =>
      d.name.toLowerCase().includes(search.toLowerCase()) ||
      d.type.toLowerCase().includes(search.toLowerCase())
    );
  }, [datasets, search]);

  return (
    <div className="bg-white rounded-lg shadow p-6 overflow-x-auto">
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 mb-4">
        <h3 className="text-gray-700 font-semibold text-lg"> Datasets ( {datasets?.length} ) </h3>
        <div className="flex items-center gap-2">
            <input
                type="text"
                placeholder="Search by name or type"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                className="border border-gray-300 rounded px-3 py-1.5 focus:outline-none focus:ring-1 focus:ring-yellow-500"
            />
            <button
                onClick={() => setIsModalOpen(true)}
                className="bg-yellow-600 text-white px-6 py-1.5 rounded hover:bg-yellow-700 transition"
            >
                Add Dataset
            </button>
        </div>
      </div>

      <table className="min-w-full table-auto border-collapse">
        <thead>
          <tr className="bg-gray-100 text-gray-700">
            <th className="px-4 py-2 text-left">ID</th>
            <th className="px-4 py-2 text-left">Name</th>
            <th className="px-4 py-2 text-left">Type</th>
            <th className="px-4 py-2 text-left">Created By</th>
            <th className="px-4 py-2 text-left">Created At</th>
            <th className="px-4 py-2 text-left">Size</th>
            <th className="px-4 py-2 text-left">Actions</th>
          </tr>
        </thead>
        <tbody>
          {filteredDatasets.length > 0 ? filteredDatasets.map(d => (
            <tr key={d.id} className="border-b border-gray-200 hover:bg-gray-50 transition-all">
              <td className="px-4 py-2">  
                <Link to={`/datasets/${d.id}`} className="hover:underline text-blue-600">
                    #{d.id}
                </Link>
              </td>
              <td className="px-4 py-2">{d.name}</td>
              <td className="px-4 py-2">{d.type}</td>
              <td className="px-4 py-2">{d.createdBy}</td>
              <td className="px-4 py-2">{d.createdAt}</td>
              <td className="px-4 py-2">{d.size}</td>
              <td className="px-4 py-2">
                <button
                    title="Delete"
                    onClick={() => dispatch(deleteDataset(d.id))}
                    className="p-1.5 hover:bg-red-600/10 transition-all rounded text-red-600"
                >
                  <FaRegTrashCan size={19} />
                </button>
              </td>
            </tr>
          )) : (
            <tr>
              <td colSpan="7" className="text-center py-4 text-gray-500">No datasets found.</td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}
