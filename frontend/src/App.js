import { useState } from "react";
import RegistroForm from "./components/RegistroForm";
import RegistrosPage from "./pages/RegistrosPage";
import "./styles/app.css";

function App() {
  const [patientId, setPatientId] = useState("");

  return (
    <div className="container">
      <h1>Prontuário UTI com Blockchain</h1>
      <input
        placeholder="ID do paciente"
        value={patientId}
        onChange={(e) => setPatientId(e.target.value)}
      />
      <RegistroForm patientId={patientId} />
      <RegistrosPage patientId={patientId} />
    </div>
  );
}

export default App;
