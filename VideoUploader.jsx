import { useState } from "react";
import axios from "axios";

export default function VideoUploader() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);

  const handleUpload = async () => {
    if (!file) return;
    const formData = new FormData();
    formData.append("video", file);
    
    try {
      const response = await axios.post("http://127.0.0.1:5000/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setResult(response.data.result);
    } catch (error) {
      console.error("Upload failed", error);
    }
  };

  return (
    <div className="p-4 flex flex-col items-center gap-4 border rounded-xl">
      <input type="file" accept="video/*" onChange={(e) => setFile(e.target.files[0])} />
      <button className="px-4 py-2 bg-blue-500 text-white rounded-lg" onClick={handleUpload}>
        Upload Video
      </button>
      {result !== null && <p>Analysis Result: {result}</p>}
    </div>
  );
}
