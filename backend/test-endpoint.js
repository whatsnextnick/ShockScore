/**
 * Quick test script to verify the /api/analyze/frame endpoint works
 * Run this while the backend server is running to test the API
 */

const http = require('http');
const fs = require('fs');
const path = require('path');

// Create a simple test image (1x1 pixel black PNG)
const testImageBuffer = Buffer.from([
  0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A, 0x00, 0x00, 0x00, 0x0D,
  0x49, 0x48, 0x44, 0x52, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x01,
  0x08, 0x06, 0x00, 0x00, 0x00, 0x1F, 0x15, 0xC4, 0x89, 0x00, 0x00, 0x00,
  0x0A, 0x49, 0x44, 0x41, 0x54, 0x78, 0x9C, 0x63, 0x00, 0x01, 0x00, 0x00,
  0x05, 0x00, 0x01, 0x0D, 0x0A, 0x2D, 0xB4, 0x00, 0x00, 0x00, 0x00, 0x49,
  0x45, 0x4E, 0x44, 0xAE, 0x42, 0x60, 0x82
]);

const boundary = '----WebKitFormBoundary7MA4YWxkTrZu0gW';
const formData = [
  `--${boundary}`,
  'Content-Disposition: form-data; name="frame"; filename="test.png"',
  'Content-Type: image/png',
  '',
  testImageBuffer.toString('binary'),
  `--${boundary}--`
].join('\r\n');

const options = {
  hostname: 'localhost',
  port: 5000,
  path: '/api/analyze/frame',
  method: 'POST',
  headers: {
    'Content-Type': `multipart/form-data; boundary=${boundary}`,
    'Content-Length': Buffer.byteLength(formData)
  }
};

console.log('🧪 Testing /api/analyze/frame endpoint...');
console.log('');

const req = http.request(options, (res) => {
  console.log(`✓ Response Status: ${res.statusCode}`);
  console.log(`✓ Response Headers:`, JSON.stringify(res.headers, null, 2));
  console.log('');

  let data = '';

  res.on('data', (chunk) => {
    data += chunk;
  });

  res.on('end', () => {
    console.log('✓ Response Body:');
    try {
      const json = JSON.parse(data);
      console.log(JSON.stringify(json, null, 2));
      console.log('');

      if (json.shockScore !== undefined) {
        console.log('✅ SUCCESS! Mock data is working correctly.');
        console.log(`   Shock Score: ${json.shockScore}`);
        console.log(`   Dominant Emotion: ${json.dominantEmotion}`);
        console.log(`   Mode: ${json._mode || 'unknown'}`);
      } else {
        console.log('⚠️  WARNING: Response missing shockScore field');
      }
    } catch (e) {
      console.log(data);
      console.log('');
      console.log('❌ ERROR: Response is not valid JSON');
    }
  });
});

req.on('error', (e) => {
  console.error('❌ ERROR: Cannot connect to backend server');
  console.error(`   Message: ${e.message}`);
  console.error('');
  console.error('   Make sure the backend is running:');
  console.error('   cd backend && npm start');
});

req.write(formData);
req.end();
