module.exports = {
  devServer: {
    proxy: {
      "/auth": {
        target: "http://127.0.0.1:5000",
        changeOrigin: true,
      },
      "/admin": {
        target: "http://127.0.0.1:5000",
        changeOrigin: true,
      },
      "/staff": {
        target: "http://127.0.0.1:5000",
        changeOrigin: true,
      },
      "/user": {
        target: "http://127.0.0.1:5000",
        changeOrigin: true,
      },
    },
  },
};
