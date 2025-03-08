import { useState, useEffect } from "react";
import "./App.css";

function App() {
  const [lightStatus, setLightStatus] = useState("off");

  const fetchLightStatus = async () => {
    const response = await fetch("http://localhost:8000/light-status");
    const data = await response.json();
    setLightStatus(data.state);
  };

  useEffect(() => {
    fetchLightStatus();
    const interval = setInterval(fetchLightStatus, 3000); // Actualiza cada 3 segundos
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="App">
      <h1>Home Automation Dashboard</h1>
      <div>
        <h2>Light Status:</h2>
        <p className={lightStatus === "on" ? "on" : "off"}>
            {lightStatus === "on" ? "💡 On" : "🌑 Off"}
        </p>
      </div>
    </div>
  );
}

export default App;
