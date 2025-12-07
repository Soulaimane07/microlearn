import { Routes, Route, Link } from "react-router-dom";
import Overview from "./pages/overview/Overview";
import Pipelines from "./pages/pipelines/Pipelines";
import PipelineDetailsPage from "./pages/pipelines/PipelineDetailsPage";
import Datasets from "./pages/datasets/Datasets";
import DatasetDetailsPage from "./pages/datasets/DatasetDetailsPage";

export default function App() {
  return (
      <Routes>
        <Route path="/" element={<Overview />} />
        <Route path="/pipelines">
          <Route index element={<Pipelines />} />
          <Route path=":id" element={<PipelineDetailsPage />} />
        </Route>
        <Route path="/datasets">
          <Route index element={<Datasets />} />
          <Route path=":id" element={<DatasetDetailsPage />} />
        </Route>
      </Routes>
  );
}
