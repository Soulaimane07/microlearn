module.exports = {
  redis: {
    host: process.env.REDIS_HOST || "redis",
    port: 6379,
  },
  nats: {
    url: `nats://${process.env.NATS_HOST || "nats"}:4222`,
  },
};
