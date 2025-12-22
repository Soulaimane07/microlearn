export async function getModelCandidates(pipelineId, dataset, targetColumn, allowedCategories = []) {
  const query = new URLSearchParams({
    pipelineId,
    minio_object: dataset,
    task_type: "classification",
    metric: "accuracy",
    max_models: 5,
    include_deep_learning: false,
    allowed_categories: allowedCategories.join(',')
  });

  const res = await fetch(`http://localhost:8001/select?${query.toString()}`);
  if (!res.ok) throw new Error('API error');
  return res.json();
}
