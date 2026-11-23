/**
 * Web Worker for periodic 2-minute stock price fetch trigger.
 * Running in a dedicated worker prevents browser tab throttling when
 * the portfolio tab is minimized or in the background.
 */

let timerId = null;
const INTERVAL_MS = 1 * 60 * 1000; // 1 minute (60,000 ms)

self.onmessage = function (e) {
  const command = e.data;

  if (command === "start") {
    if (timerId) clearInterval(timerId);
    timerId = setInterval(() => {
      self.postMessage({ type: "tick", timestamp: Date.now() });
    }, INTERVAL_MS);
  } else if (command === "stop") {
    if (timerId) {
      clearInterval(timerId);
      timerId = null;
    }
  }
};
