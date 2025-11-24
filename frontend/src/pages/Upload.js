import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './Upload.css';

const Upload = () => {
  const navigate = useNavigate();
  const [file, setFile] = useState(null);
  const [filmTitle, setFilmTitle] = useState('');
  const [genre, setGenre] = useState('Horror');
  const [studioName, setStudioName] = useState('');
  const [uploading, setUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      setFile(selectedFile);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!file) {
      alert('Please select a video file');
      return;
    }

    setUploading(true);

    const formData = new FormData();
    formData.append('video', file);
    formData.append('filmTitle', filmTitle);
    formData.append('genre', genre);
    formData.append('studioName', studioName);

    try {
      const response = await fetch('/api/videos/upload', {
        method: 'POST',
        body: formData
      });

      const data = await response.json();

      if (response.ok) {
        // Start processing
        await fetch(`/api/videos/${data.video.id}/process`, {
          method: 'POST'
        });

        alert('Video uploaded and processing started!');
        navigate('/');
      } else {
        alert('Upload failed: ' + data.error);
      }
    } catch (error) {
      console.error('Upload error:', error);
      alert('Upload failed. Please try again.');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="upload-page fade-in">
      <div className="container">
        <div className="upload-header">
          <h1>Upload Film for Analysis</h1>
          <p>Upload your horror/thriller film to get Shock Score analytics</p>
        </div>

        <div className="upload-card card">
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label>Film Title *</label>
              <input
                type="text"
                className="form-input"
                value={filmTitle}
                onChange={(e) => setFilmTitle(e.target.value)}
                placeholder="Enter film title"
                required
              />
            </div>

            <div className="form-row">
              <div className="form-group">
                <label>Genre</label>
                <select
                  className="form-input"
                  value={genre}
                  onChange={(e) => setGenre(e.target.value)}
                >
                  <option>Horror</option>
                  <option>Thriller</option>
                  <option>Psychological Horror</option>
                  <option>Slasher</option>
                  <option>Supernatural</option>
                </select>
              </div>

              <div className="form-group">
                <label>Studio Name</label>
                <input
                  type="text"
                  className="form-input"
                  value={studioName}
                  onChange={(e) => setStudioName(e.target.value)}
                  placeholder="Your studio name"
                />
              </div>
            </div>

            <div className="form-group">
              <label>Video File *</label>
              <div className="file-upload-area">
                <input
                  type="file"
                  id="video-file"
                  accept="video/mp4,video/avi,video/mov,video/mkv,video/webm"
                  onChange={handleFileChange}
                  className="file-input"
                />
                <label htmlFor="video-file" className="file-upload-label">
                  {file ? (
                    <div>
                      <div className="file-icon">✓</div>
                      <div>{file.name}</div>
                      <div className="file-size">
                        {(file.size / (1024 * 1024)).toFixed(2)} MB
                      </div>
                    </div>
                  ) : (
                    <div>
                      <div className="file-icon">📁</div>
                      <div>Click to select video file</div>
                      <div className="file-hint">
                        Supported: MP4, AVI, MOV, MKV, WebM (Max 500MB)
                      </div>
                    </div>
                  )}
                </label>
              </div>
            </div>

            <div className="privacy-notice">
              <h4>Privacy Guarantee</h4>
              <p>
                ✓ Your video is processed locally and never stored permanently<br />
                ✓ Only anonymized aggregate emotion data is saved<br />
                ✓ 100% GDPR/CCPA compliant - no facial data retained
              </p>
            </div>

            <button
              type="submit"
              className="btn btn-primary btn-large"
              disabled={uploading}
            >
              {uploading ? 'Uploading...' : 'Upload & Analyze'}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default Upload;
