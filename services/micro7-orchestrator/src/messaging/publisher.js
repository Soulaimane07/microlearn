const { getNats } = require("./nats");

async function publishStep(stepName, payload) {
  const nc = getNats();

  nc.publish(
    `pipeline.${stepName}.start`,
    Buffer.from(JSON.stringify(payload))
  );
}

module.exports = { publishStep };
