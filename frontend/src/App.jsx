// src/App.jsx
import React, { useState } from "react";
import "./App.css";

function App() {
  // Estados para subir archivo
  const [selectedFile, setSelectedFile] = useState(null);

  // Estados para grabación
  const [isRecording, setIsRecording] = useState(false);
  const [mediaRecorder, setMediaRecorder] = useState(null);
  const [recordedChunks, setRecordedChunks] = useState([]);
  const [recordingStartTime, setRecordingStartTime] = useState(null);

  // Estados para mostrar resultados y mensajes
  const [message, setMessage] = useState("");
  const [transcription, setTranscription] = useState("");
  const [summary, setSummary] = useState("");
  const [loading, setLoading] = useState(false);

  // Maneja la selección de archivo manual
  const handleFileChange = (e) => {
    if (e.target.files && e.target.files.length > 0) {
      setSelectedFile(e.target.files[0]);
    }
  };

  // Iniciar grabación
  const startRecording = async () => {
    try {
      setMessage("");
      setTranscription("");
      setSummary("");
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const recorder = new MediaRecorder(stream);

      recorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          setRecordedChunks((prev) => [...prev, event.data]);
        }
      };

      recorder.start();
      setMediaRecorder(recorder);
      setRecordedChunks([]);
      setIsRecording(true);
      setRecordingStartTime(Date.now());
    } catch (error) {
      console.error("Error al acceder al micrófono:", error);
      alert("No se pudo acceder al micrófono. Verifica los permisos.");
    }
  };

  // Detener grabación
  const stopRecording = () => {
    if (mediaRecorder) {
      mediaRecorder.stop();
      setIsRecording(false);
      setMediaRecorder(null);
    }
  };

  /**
   *  Sube el archivo al backend:
   *  - Si isRecorded = true, sube lo grabado.
   *  - Si isRecorded = false, sube el archivo seleccionado manualmente.
   */
  const handleUpload = async (isRecorded = false) => {
    setLoading(true);
    setMessage("");
    setTranscription("");
    setSummary("");

    try {
      let fileToUpload = null;

      if (isRecorded) {
        if (!recordedChunks.length) {
          alert("Primero graba algo antes de subir.");
          setLoading(false);
          return;
        }
        // Crear un File con nombre único basado en la hora de inicio
        const blob = new Blob(recordedChunks, { type: "audio/webm" });
        const startTime = recordingStartTime || Date.now();
        const dateString = new Date(startTime)
          .toISOString()
          .replace(/[\W_]+/g, "-");
        const fileName = `grabacion_${dateString}.webm`;
        fileToUpload = new File([blob], fileName, { type: "audio/webm" });
      } else {
        if (!selectedFile) {
          alert("Selecciona un archivo de audio antes de subir.");
          setLoading(false);
          return;
        }
        fileToUpload = selectedFile;
      }

      const formData = new FormData();
      formData.append("file", fileToUpload);

      // Petición al backend
      const response = await fetch(
        "http://127.0.0.1:8000/audio/upload-audio/",
        {
          method: "POST",
          body: formData,
        },
      );

      if (!response.ok) {
        throw new Error(`Error: Código ${response.status}`);
      }

      const data = await response.json();
      setLoading(false);

      if (data.error) {
        setMessage(`Error: ${data.error}`);
      } else {
        setMessage(data.message || "¡Audio procesado correctamente!");
        setTranscription(data.transcription || "");
        setSummary(data.summary || "");
      }
    } catch (error) {
      setLoading(false);
      console.error(error);
      setMessage("Ocurrió un error al subir el archivo.");
    }
  };

  return (
    <div className="container">
      <h1>Audio Uploader & Recorder</h1>
      <p className="subtitle">Transcribe y resume tus audios con IA</p>

      <div className="box">
        <h2>1. Subir un archivo de audio existente</h2>
        <div className="input-row">
          <input
            className="file-input"
            type="file"
            accept="audio/*"
            onChange={handleFileChange}
          />
          <button
            className="primary-button"
            onClick={() => handleUpload(false)}
            disabled={loading}
          >
            {loading ? "Procesando..." : "Subir y Procesar"}
          </button>
        </div>
      </div>

      <div className="box">
        <h2>2. Grabar desde el micrófono</h2>
        <div className="record-buttons">
          {!isRecording ? (
            <button className="secondary-button" onClick={startRecording}>
              Iniciar Grabación
            </button>
          ) : (
            <button className="secondary-button" onClick={stopRecording}>
              Detener Grabación
            </button>
          )}
          <button
            className="primary-button"
            onClick={() => handleUpload(true)}
            disabled={loading || !recordedChunks.length}
          >
            {loading ? "Procesando..." : "Subir Grabación"}
          </button>
        </div>
      </div>

      {message && <p className="msg">{message}</p>}

      {transcription && (
        <div className="result-box">
          <h3>Transcripción</h3>
          <pre>{transcription}</pre>
        </div>
      )}

      {summary && (
        <div className="result-box">
          <h3>Resumen</h3>
          <pre>{summary}</pre>
        </div>
      )}
    </div>
  );
}

export default App;
