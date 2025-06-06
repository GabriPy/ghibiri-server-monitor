function updateStats() {
  fetch("http://192.168.1.70:5000/api/system")
    .then((res) => res.json())
    .then((data) => {
      document.getElementById(
        "diskusage"
      ).textContent = `${data.disk.percent}%`;
      // document.getElementById("cputemp").textContent = `${data.cpu_temp}%`;
      document.getElementById("cputemp").textContent =
        data.cpu_temp !== null ? `${data.cpu_temp}°C` : "N/D";

      document.getElementById(
        "ramusage"
      ).textContent = `${data.memory.percent}%`;
      document.getElementById("cpuusage").textContent = `${data.cpu_percent}%`;
      document.getElementById("uptime").textContent = `${data.uptime}`;

      document.getElementById("ossystem").textContent = `${data.os}`;
      document.getElementById("hostname").textContent = `${data.hostname}`;

      document.getElementById("ip_interno").textContent = `${data.ip_interno}`;
      document.getElementById("ip_esterno").textContent = `${data.ip_esterno}`;

      document.getElementById(
        "conn-in"
      ).textContent = `${data.network_bytes_recv}`;
      document.getElementById(
        "conn-out"
      ).textContent = `${data.network_bytes_sent}`;
    });
}
