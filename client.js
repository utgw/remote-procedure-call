const net = require('net');
const serverPath = '/tmp/socket_file'
const client = net.createConnection(serverPath, () => {
  console.log('connected to the server');
  
  const request = {
    method: 'reverse',
    "params": 'abcdeff', 
    "param_types": ['int'],
    "id": 1
  }
  
  client.write(JSON.stringify(request))
});

client.on('data', (data) => {
    const response = JSON.parse(data.toString());

    if ('result' in response) {
        console.log('Result:', response.result);
        console.log('Result type:', response.result_type);
    } else {
        console.log('Error:', response.error);
    }

    client.end();
});

client.on('end', () => {
    console.log('Disconnected from server');
});

client.on('error', (err) => {
    console.error(`Connection error: ${err.message}`);
});