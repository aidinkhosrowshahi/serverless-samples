import React, { useState } from 'react';
import { Amplify, Auth } from 'aws-amplify';
import { withAuthenticator } from '@aws-amplify/ui-react';
import '@aws-amplify/ui-react/styles.css';

// Amplify configuration is now handled in aws-exports.js

function App({ signOut, user }) {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);

  const handleFileSelect = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) return;
    
    try {
      setUploading(true);
      
      // Get pre-signed URL from API Gateway
      const response = await fetch('YOUR_API_GATEWAY_ENDPOINT', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${(await Auth.currentSession()).getAccessToken().getJwtToken()}`
        },
        body: JSON.stringify({
          fileName: file.name,
          contentType: file.type
        })
      });

      const { uploadUrl } = await response.json();

      // Upload file using pre-signed URL
      await fetch(uploadUrl, {
        method: 'PUT',
        body: file,
        headers: {
          'Content-Type': file.type
        }
      });

      alert('File uploaded successfully!');
      setFile(null);
    } catch (error) {
      console.error('Error uploading file:', error);
      alert('Error uploading file');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>Private S3 File Upload</h1>
      <div>Hello {user.username}</div>
      <div style={{ marginTop: 20 }}>
        <input
          type="file"
          onChange={handleFileSelect}
          disabled={uploading}
        />
        <button
          onClick={handleUpload}
          disabled={!file || uploading}
          style={{ marginLeft: 10 }}
        >
          {uploading ? 'Uploading...' : 'Upload'}
        </button>
      </div>
      <button onClick={signOut} style={{ marginTop: 20 }}>Sign out</button>
    </div>
  );
}

export default withAuthenticator(App);