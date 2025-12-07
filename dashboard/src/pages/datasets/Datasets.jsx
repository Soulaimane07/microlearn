import React, { useState } from "react";
import Sidebar from "../../components/sidebar/Sidebar";
import Topbar from "../../components/topbar/Topbar";
import Footer from "../../components/footer/Footer";
import DatasetsTable from "../../components/tables/DatasetsTable";
import Modal from "../../components/Modal";
import AddDatasetForm from "./AddDatasetForm";

export default function Datasets() {
  const [isModalOpen, setIsModalOpen] = useState(false);

  return (
    <div className="flex min-h-screen bg-gray-50 text-gray-900">
      <Sidebar />

      <div className="flex-1 flex flex-col">
        <Topbar title="Datasets" />
        <main className="flex-1 p-8">
          <DatasetsTable setIsModalOpen={setIsModalOpen} />
        </main>
        <Footer />
      </div>

      <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} title="Add New Dataset">
        <AddDatasetForm onClose={() => setIsModalOpen(false)} />
      </Modal>
    </div>
  );
}
