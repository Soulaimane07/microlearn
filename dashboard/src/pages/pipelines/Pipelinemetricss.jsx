import React from 'react'

function Pipelinemetricss({pipeline}) {
  return (
    <div className="bg-white rounded-lg shadow p-6 grid grid-cols-1 md:grid-cols-3 gap-4">
        <h3 className="col-span-full font-semibold mb-2">Metrics</h3>
        <p>
            <span className="font-semibold">Accuracy:</span> {pipeline.metrics.accuracy ?? "N/A"}
        </p>
        <p>
            <span className="font-semibold">F1 Score:</span> {pipeline.metrics.f1 ?? "N/A"}
        </p>
        <p>
            <span className="font-semibold">AUC:</span> {pipeline.metrics.auc ?? "N/A"}
        </p>
    </div>
  )
}

export default Pipelinemetricss