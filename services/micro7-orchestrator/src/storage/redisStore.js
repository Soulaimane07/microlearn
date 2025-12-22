const redis = require("./redis");

async function savePipeline(pipeline) {
  pipeline.updatedAt = new Date().toISOString();
  await redis.set(`pipeline:${pipeline.id}`, JSON.stringify(pipeline));
}

async function getPipeline(id) {
  const data = await redis.get(`pipeline:${id}`);
  return data ? JSON.parse(data) : null;
}

module.exports = { savePipeline, getPipeline };
