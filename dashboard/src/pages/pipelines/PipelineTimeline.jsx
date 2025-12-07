import React from 'react'
import { getStatusColor } from '../../components/Variables'

function PipelineTimeline({pipeline}) {
  return (
    <div className="bg-white rounded-lg shadow p-6">
        <h3 className="font-semibold mb-3">Steps Timeline</h3>
        <div className="flex gap-4 overflow-x-auto">
            {pipeline.steps && pipeline.steps.length > 0 ? (
            pipeline.steps.map((step, idx) => (
                <div key={idx} className="flex flex-col items-center">
                <div
                    className={`px-4 py-2 rounded-md font-medium flex items-center justify-center text-sm text-white ${getStatusColor(
                    step.status
                    )}`}
                >
                    {step.name}
                </div>
                <span className="text-xs mt-1">{step.status}</span>
                    {step.duration && <span className="text-xs mt-0.5 text-gray-600">{step.duration}</span>}
                </div>
            ))
            ) : (
                <p className="text-gray-500">No steps available</p>
            )}
        </div>
    </div>
  )
}

export default PipelineTimeline