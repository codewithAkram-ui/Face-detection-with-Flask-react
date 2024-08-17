import React, { useState } from 'react';
import axios from 'axios';

function App() {
    const [file, setFile] = useState(null);
    const [result, setResult] = useState(null);

    const handleFileChange = (e) => {
        const selectedFile = e.target.files[0];
        console.log("Selected file:", selectedFile.name, selectedFile.size);
        setFile(selectedFile);
    };
    
    const handleSubmit = async (e) => {
        e.preventDefault();
        const formData = new FormData();
        formData.append('file', file);

        try {
            console.log("Uploading file...");
            const response = await axios.post('http://localhost:5000/predict', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
            console.log("Response received:", response.data);  // Debugging line
            setResult(response.data.is_face ? "This is a face" : "This is not a face");
            console.log("Result set:", response.data.is_face);  // Debugging line
        } catch (error) {
            console.error("Error during file upload:", error);
        }
    };
    
    return (
        <div className="App">
            <h1>Face Recognition</h1>
            <form onSubmit={handleSubmit}>
                <input type="file" onChange={handleFileChange} />
                <button type="submit">Submit</button>
            </form>
            {result && <p>{result}</p>}
        </div>
    );
}

export default App;
