import React from "react";
import Sidebar from "../../components/sidebar/Sidebar";
import Topbar from "../../components/topbar/Topbar";
import Footer from "../../components/footer/Footer";
import PipelinesTable from "../../components/tables/PipelinesTable";

function Pipelines() {
  return (
    <div className="flex min-h-screen bg-gray-50 text-gray-900">
      <Sidebar />
      
      <div className="flex-1 flex flex-col">
        <Topbar title="Pipelines"  />

        <main className="flex-1 p-8">
          <PipelinesTable />
        </main>

        <Footer />
      </div>
    </div>
  );
}

export default Pipelines;
