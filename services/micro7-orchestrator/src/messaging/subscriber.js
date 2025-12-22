const { getNats } = require("./nats");
const { onStepCompleted } = require("../core/orchestrator");

async function listen() {
  const nc = getNats();
  const sub = nc.subscribe("pipeline.*.done");

  console.log("📡 Listening for pipeline step completion events");

  for await (const msg of sub) {
    const event = JSON.parse(msg.data.toString());
    await onStepCompleted(event);
  }
}

module.exports = { listen };
