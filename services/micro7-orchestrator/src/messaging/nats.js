const { connect } = require("nats");
const config = require("../config");

let nc;

async function connectNats() {
  if (!nc) {
    nc = await connect({ servers: config.nats.url });
    console.log("✅ Connected to NATS");
  }
  return nc;
}

function getNats() {
  if (!nc) {
    throw new Error("NATS not connected");
  }
  return nc;
}

module.exports = { connectNats, getNats };
