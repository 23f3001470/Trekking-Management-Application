module.exports = {
  devServer: {
    proxy: {
      "/auth": {
        target: "http://127.0.0.1:5000",
        changeOrigin: true,
      },
    },
  },
};
