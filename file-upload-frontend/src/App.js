import React, { useState } from 'react';
import { Amplify, API } from 'aws-amplify';
import { Button, Flex, Text } from '@aws-amplify/ui-react';
import '@aws-amplify/ui-react/styles.css';

// Configure Amplify
Amplify.configure({
  API: {
    endpoints: [
      {
        name: 'fileUploadApi',
        endpoint: process.env.REACT_APP_API_ENDPOINT
      }
    ]
  }
});

function App() {
  const [file, setFile] = useState(null);
  const [uploadStatus, setUploadStatus] = useState('');

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) {
      setUploadStatus('Please select a file first');
      return;
    }

    try {
      // Get presigned URL from API Gateway
      const response = await API.get('fileUploadApi', '/presigned-url', {
        queryStringParameters: {
          fileName: file.name,
          fileType: file.type
        }
      });

      const { uploadUrl } = response;

      // Upload file using presigned URL
      await fetch(uploadUrl, {
        method: 'PUT',
        body: file,
        headers: {
          'Content-Type': file.type
        }
      });

      setUploadStatus('File uploaded successfully!');
    } catch (error) {
      console.error('Error uploading file:', error);
      setUploadStatus('Error uploading file');
    }
  };

  return (
    <Flex direction="column" padding="2rem">
      <Text variation="primary" fontSize="2rem" marginBottom="1rem">
        File Upload Demo
      </Text>
      
      <input type="file" onChange={handleFileChange} />
      
      <Button onClick={handleUpload} marginTop="1rem">
        Upload File
      </Button>
      
      {uploadStatus && (
        <Text variation={uploadStatus.includes('Error') ? 'error' : 'success'} marginTop="1rem">
          {uploadStatus}
        </Text>
      )}
    </Flex>
  );
}

export default App;