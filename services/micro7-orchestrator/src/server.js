require('dotenv').config();
const fastify = require("fastify")({ logger: true });
const cors = require("@fastify/cors"); // import cors plugin
const routes = require("./api/pipeline");
const { connectNats } = require("./messaging/nats");
const { listen } = require("./messaging/subscriber");

// Enable CORS for all origins (or customize origin)
fastify.register(cors, {
  origin: "*", // allow all origins, or set specific: ["http://localhost:3000"]
  methods: ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
});

fastify.register(routes);

async function start() {
  await connectNats();
  listen();

  await fastify.listen({ port: 3000, host: "0.0.0.0" });
  console.log("🚀 Orchestrator running on port 3000");
}

start();
