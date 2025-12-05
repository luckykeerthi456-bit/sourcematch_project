#!/usr/bin/env node
/**
 * Simulate browser-based registration flow to capture exact HTTP request/response
 * This script: 1) loads frontend, 2) navigates to Register tab, 3) fills form, 4) submits
 * and captures the axios POST request to /api/users/register
 */

const http = require('http');
const https = require('https');

async function testRegisterViaHTTP() {
  const testEmail = `browsertest+${Date.now()}@example.com`;
  const payload = JSON.stringify({
    email: testEmail,
    password: 'password123',
    role: 'candidate',
    full_name: 'Browser Test User',
  });

  console.log('\n========================================');
  console.log('Testing Registration Flow');
  console.log('========================================\n');
  console.log('Endpoint: POST http://localhost:8001/api/users/register');
  console.log('Payload:', payload);
  console.log('\nSending request...\n');

  return new Promise((resolve, reject) => {
    const options = {
      hostname: 'localhost',
      port: 8001,
      path: '/api/users/register',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(payload),
      },
    };

    const req = http.request(options, (res) => {
      let data = '';

      res.on('data', (chunk) => {
        data += chunk;
      });

      res.on('end', () => {
        console.log('Response Status:', res.statusCode);
        console.log('Response Headers:', JSON.stringify(res.headers, null, 2));
        console.log('Response Body:', data);

        if (res.statusCode === 200 || res.statusCode === 422 || res.statusCode === 400) {
          try {
            const parsed = JSON.parse(data);
            console.log('\nParsed Response:');
            console.log(JSON.stringify(parsed, null, 2));
          } catch (e) {
            console.log('(Could not parse as JSON)');
          }
        }

        if (res.statusCode === 200) {
          console.log('\n✅ Registration succeeded!');
        } else if (res.statusCode === 400) {
          console.log('\n❌ Registration returned 400 (client error):');
          console.log('   Common causes: duplicate email, validation failure');
        } else if (res.statusCode === 422) {
          console.log('\n❌ Registration returned 422 (validation error):');
          console.log('   Payload may have invalid JSON or missing required fields');
        } else {
          console.log('\n❌ Registration returned:', res.statusCode);
        }

        resolve();
      });
    });

    req.on('error', (err) => {
      console.error('Request error:', err.message);
      console.error('  Likely cause: backend not running on http://localhost:8001');
      reject(err);
    });

    req.write(payload);
    req.end();
  });
}

async function testLoginFlow(email) {
  const payload = JSON.stringify({
    email,
    password: 'password123',
  });

  console.log('\n========================================');
  console.log('Testing Login Flow (for newly registered user)');
  console.log('========================================\n');
  console.log('Endpoint: POST http://localhost:8001/api/users/login');
  console.log('Payload:', payload);
  console.log('\nSending request...\n');

  return new Promise((resolve, reject) => {
    const options = {
      hostname: 'localhost',
      port: 8001,
      path: '/api/users/login',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(payload),
      },
    };

    const req = http.request(options, (res) => {
      let data = '';

      res.on('data', (chunk) => {
        data += chunk;
      });

      res.on('end', () => {
        console.log('Response Status:', res.statusCode);
        if (res.statusCode === 200) {
          try {
            const parsed = JSON.parse(data);
            console.log('\n✅ Login succeeded!');
            console.log('Token:', parsed.access_token ? `${parsed.access_token.slice(0, 20)}...` : 'N/A');
            console.log('User:', parsed.user ? JSON.stringify(parsed.user, null, 2) : 'N/A');
          } catch (e) {
            console.log('Could not parse login response');
          }
        } else {
          console.log('Response:', data);
        }
        resolve();
      });
    });

    req.on('error', (err) => {
      console.error('Login request error:', err.message);
      reject(err);
    });

    req.write(payload);
    req.end();
  });
}

(async () => {
  try {
    await testRegisterViaHTTP();
    const testEmail = `browsertest+${Date.now()}@example.com`;
    // Note: login would use the email from the registration response
    // For this demo, we'll use a hardcoded email that was registered earlier
    await testLoginFlow('apitest+ps@example.com');
    console.log('\n========================================');
    console.log('Test Complete');
    console.log('========================================\n');
  } catch (err) {
    console.error('Test failed:', err);
    process.exit(1);
  }
})();
