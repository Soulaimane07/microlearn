import React, { useState } from "react";
import { useDispatch } from "react-redux";
import { addDataset } from "../../redux/slices/datasetsSlice";

export default function AddDatasetForm({ onClose }) {
  const dispatch = useDispatch();
  const [name, setName] = useState("");
  const [createdBy, setCreatedBy] = useState("Admin");
  const [file, setFile] = useState(null);
  const [size, setSize] = useState("");
  const [type, setType] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!file) return alert("Please select a file");

    const newDataset = {
      id: Date.now(),
      name,
      type,
      createdBy,
      createdAt: new Date().toISOString().split("T")[0],
      size,
      fileName: file.name
    };
    dispatch(addDataset(newDataset));
    onClose();
  };

  const handleFileChange = (e) => {
    if (e.target.files.length > 0) {
      const selectedFile = e.target.files[0];
      const fileExtension = selectedFile.name.split(".").pop().toLowerCase();

      if (!["csv", "json"].includes(fileExtension)) {
        alert("Only CSV and JSON files are allowed");
        e.target.value = null;
        return;
      }

      setFile(selectedFile);
      setSize(`${(selectedFile.size / 1024 / 1024).toFixed(2)} MB`);
      setType(fileExtension.toUpperCase());
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <input
        type="text"
        placeholder="Dataset Name"
        value={name}
        onChange={(e) => setName(e.target.value)}
        className="w-full border px-3 py-2 rounded"
        required
      />

      <div className="flex items-center justify-center w-full">
        <label
          htmlFor="dropzone-file"
          className="flex flex-col items-center justify-center w-full h-40 bg-neutral-secondary-medium border border-dashed border-gray-400 rounded cursor-pointer hover:bg-neutral-tertiary-medium"
        >
          <div className="flex flex-col items-center justify-center text-center pt-5 pb-6">
            <svg
              className="w-8 h-8 mb-4"
              aria-hidden="true"
              xmlns="http://www.w3.org/2000/svg"
              width="24"
              height="24"
              fill="none"
              viewBox="0 0 24 24"
            >
              <path
                stroke="currentColor"
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                d="M15 17h3a3 3 0 0 0 0-6h-.025a5.56 5.56 0 0 0 .025-.5A5.5 5.5 0 0 0 7.207 9.021C7.137 9.017 7.071 9 7 9a4 4 0 1 0 0 8h2.167M12 19v-9m0 0-2 2m2-2 2 2"
              />
            </svg>
            <p className="mb-2 text-sm">
              <span className="font-semibold">Click to upload</span> or drag and drop
            </p>
            <p className="text-xs">Only CSV or JSON files</p>
            {file && (
              <p className="mt-2 text-sm text-gray-600">
                Selected file: {file.name} ({size})
              </p>
            )}
          </div>
          <input
            id="dropzone-file"
            type="file"
            accept=".csv,.json"
            className="hidden"
            onChange={handleFileChange}
          />
        </label>
      </div>

      <div className="flex justify-end gap-2">
        <button
          type="button"
          onClick={onClose}
          className="px-4 py-2 bg-gray-200 rounded hover:bg-gray-300"
        >
          Cancel
        </button>
        <button
          type="submit"
          className="px-4 py-2 bg-yellow-600 text-white rounded hover:bg-yellow-700"
        >
          Add
        </button>
      </div>
    </form>
  );
}
