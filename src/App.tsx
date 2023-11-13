import { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [file, setFile] = useState<File | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setFile(e.target.files[0]);
    }
  };

  function handleUpload() {
    if (file) {
      const formData = new FormData();
      formData.append("file", file);

      axios
        .post("http://127.0.0.1:8000/file", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        })
        .then((response) => {
          console.log("File uploaded successfully", response.data);
        })
        .catch((error) => {
          console.error("Error uploading file", error);
        });
    }
  }

  return (
    <div className="container">
      <div className="row">
        <div>
          <label htmlFor="file" className="sr-only">
            Choose a file
          </label>
          <input id="file" type="file" onChange={handleFileChange} />
        </div>

        {file && (
          <section>
            File details:
            <ul>
              <li>Name: {file.name}</li>
              <li>Type: {file.type}</li>
              <li>Size: {file.size} bytes</li>
            </ul>
          </section>
        )}

        {file && <button onClick={handleUpload}>Upload a file</button>}
      </div>
    </div>
  );
}

export default App;
