import React from "react";
import { Link, useParams } from "react-router-dom";
import { useSelector, useDispatch } from "react-redux";
import Sidebar from "../../components/sidebar/Sidebar";
import Topbar from "../../components/topbar/Topbar";
import Footer from "../../components/footer/Footer";
import { getStatusColor } from "../../components/Variables";
import PipelineMetrics from "./PipelineMetricss";
import PipelineTimeline from "./PipelineTimeline";
import PipelineLogs from "./PipelineLogs";
import { deletePipeline, rerunPipeline, stopPipeline } from "../../redux/slices/pipelinesSlice";


export default function PipelineDetailsPage() {
  const { id } = useParams();
  const dispatch = useDispatch();

  const pipeline = useSelector(state =>
    state.pipelines.list.find(p => p.id.toString() === id)
  );

  const datasets = useSelector(state => state.datasets.list);
  const dataset = datasets.find(d => d.id === pipeline.datasetId);

  if (!pipeline)
    return (
      <div className="flex items-center justify-center h-screen">
        <p className="text-gray-500 text-lg">Pipeline not found</p>
      </div>
    );

  const showMetrics = pipeline.steps && pipeline.steps.some(step => step.status !== "Success");

  const handleRerun = () => dispatch(rerunPipeline(pipeline.id));
  const handleStop = () => dispatch(stopPipeline(pipeline.id));
  const handleDelete = () => {
    if (window.confirm(`Are you sure to delete pipeline #${pipeline.id}?`)) {
      dispatch(deletePipeline(pipeline.id));
    }
  };

  return (
    <div className="flex min-h-screen bg-gray-50 text-gray-900">
      <Sidebar />
      <div className="flex-1 flex flex-col">
        <Topbar title={`Pipeline #${pipeline.id}`} />
        <main className="flex-1 p-8 space-y-6">

          {/* Pipeline Info Card */}
          <div className="bg-white rounded-lg shadow p-6 space-y-4">
            <div className="flex flex-col md:flex-row md:items-center md:justify-between space-y-4 md:space-y-0">
              <div className="flex flex-col md:flex-row md:items-center space-x-6">
                <h2 className="text-2xl font-semibold">{pipeline.name}</h2>
                <span
                  className={`px-3 py-1 rounded-full text-white text-sm ${getStatusColor(pipeline.status)}`}
                >
                  {pipeline.status}
                </span>
              </div>

              {/* Action Buttons */}
              <div className="flex gap-3">
                {pipeline.status === "Running" ? (
                  <button
                    onClick={handleStop}
                    className="px-4 py-2 bg-red-500 hover:bg-red-600 text-white rounded transition"
                  >
                    Stop
                  </button>
                ) : (
                  <button
                    onClick={handleRerun}
                    className="px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded transition"
                  >
                    Re-run
                  </button>
                )}
                <button
                  onClick={handleDelete}
                  className="px-4 py-2 bg-gray-500 hover:bg-gray-600 text-white rounded transition"
                >
                  Delete
                </button>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
              <p><span className="font-semibold">Dataset:</span> <Link to={`/datasets/${dataset?.id}`} className="hover:underline transition-all text-blue-600"> {dataset?.name || "Unknown"} </Link> </p>
              <p><span className="font-semibold">Created By:</span> {pipeline.createdBy}</p>
              <p><span className="font-semibold">Start Time:</span> {pipeline.startTime}</p>
              <p><span className="font-semibold">Steps Completed:</span> {pipeline.stepsCompleted}</p>
              <p><span className="font-semibold">Duration:</span> {pipeline.duration}</p>
            </div>
          </div>

          <PipelineTimeline pipeline={pipeline} />
          {!showMetrics && pipeline.metrics && <PipelineMetrics pipeline={pipeline} />}
          <PipelineLogs pipeline={pipeline} />

        </main>
        <Footer />
      </div>
    </div>
  );
}
