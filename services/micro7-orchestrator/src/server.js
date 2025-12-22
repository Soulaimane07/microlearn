require('dotenv').config();
const fastify = require("fastify")({ logger: true });
const routes = require("./api/pipeline");
const { connectNats } = require("./messaging/nats");
const { listen } = require("./messaging/subscriber");

fastify.register(routes);

async function start() {
  await connectNats();
  listen();

  await fastify.listen({ port: 3000, host: "0.0.0.0" });
  console.log("🚀 Orchestrator running on port 3000");
}

start();
