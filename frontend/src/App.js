import React, {useState} from "react";
import ReactDOM from "react-dom/client";
import "./styles.css";

function App(){
  const [preview, setPreview] = useState(null);
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [file, setFile] = useState(null);
  function onFileChange(e){
    const f = e.target.files[0];
    if(!f) return;
    setFile(f);
    setPreview(URL.createObjectURL(f));
  }
  async function onSearch(e){
    e.preventDefault();
    if(!file){
      alert("Please choose an image file to upload (URL search is disabled in this offline package).");
      return;
    }
    setLoading(true);
    const fd = new FormData();
    fd.append("image", file);
    try{
      const resp = await fetch("/api/search", {method:"POST", body: fd});
      const data = await resp.json();
      if(resp.ok){
        setResults(data.results);
      } else {
        alert(data.error || "Search failed");
      }
    } catch(err){
      alert("Failed to contact backend. Make sure Flask backend is running on port 5000.");
    } finally{
      setLoading(false);
    }
  }
  return (
    <div className="app">
      <h1>Visual Product Matcher (Demo)</h1>
      <form onSubmit={onSearch} className="uploader">
        <input type="file" accept="image/*" onChange={onFileChange} />
        <button type="submit" disabled={loading}>{loading? "Searching...":"Search similar"}</button>
      </form>
      <div className="content">
        <div className="preview">
          <h3>Uploaded Image</h3>
          {preview ? <img src={preview} alt="preview"/> : <div className="placeholder">No image</div>}
        </div>
        <div className="results">
          <h3>Results</h3>
          {results.length===0 && <div className="placeholder">No results yet</div>}
          <ul>
            {results.map(r=>(
              <li key={r.id}>
                <img src={r.image} alt={r.name} onError={(e)=>{e.target.src="/products/"+r.image.split("/").pop()}}/>
                <div>
                  <strong>{r.name}</strong>
                  <div>{r.category}</div>
                  <div>Similarity: {r.similarity}%</div>
                </div>
              </li>
            ))}
          </ul>
        </div>
      </div>
      <footer>
        <small>Demo uses simple color-based similarity computed server-side.</small>
      </footer>
    </div>
  );
}

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(<App />);