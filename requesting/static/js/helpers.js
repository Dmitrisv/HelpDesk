"use strict";
(() => {
  const proto = window.location.protocol === "https:" ? "wss" : "ws";
  const url = `${proto}://${window.location.host}/ws/rtm/`;
  const chatSocket = new WebSocket(url);
  chatSocket.onmessage = () => window.location.reload();
})();
