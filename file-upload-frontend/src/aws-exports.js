const awsConfig = {
  API: {
    endpoints: [
      {
        name: 'fileUploadApi',
        endpoint: process.env.REACT_APP_API_ENDPOINT || 'YOUR_API_GATEWAY_ENDPOINT'
      }
    ]
  }
};

export default awsConfig;