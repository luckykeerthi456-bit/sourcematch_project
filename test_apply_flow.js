#!/usr/bin/env node
/**
 * Test the Apply flow: register user, login, then apply to a job
 */

const http = require('http');

function makeRequest(method, path, headers, body) {
  return new Promise((resolve, reject) => {
    const options = {
      hostname: 'localhost',
      port: 8001,
      path,
      method,
      headers: {
        ...headers,
        ...(body && { 'Content-Length': Buffer.byteLength(body) }),
      },
    };

    const req = http.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => { data += chunk; });
      res.on('end', () => {
        try {
          resolve({ status: res.statusCode, data: JSON.parse(data), headers: res.headers });
        } catch {
          resolve({ status: res.statusCode, data, headers: res.headers });
        }
      });
    });

    req.on('error', reject);
    if (body) req.write(body);
    req.end();
  });
}

async function test() {
  console.log('\n=== TESTING APPLY FLOW ===\n');

  try {
    // 1. Register user
    console.log('1️⃣  Registering user...');
    const regResp = await makeRequest('POST', '/api/users/register', 
      { 'Content-Type': 'application/json' },
      JSON.stringify({ email: `apply-test+${Date.now()}@example.com`, password: 'pass123', role: 'candidate', full_name: 'Apply Tester' })
    );
    if (regResp.status !== 200) {
      console.log('❌ Register failed:', regResp.status, regResp.data);
      return;
    }
    const userId = regResp.data.id;
    const userEmail = regResp.data.email;
    console.log(`✅ User registered (ID: ${userId}, Email: ${userEmail})\n`);

    // 2. Login user
    console.log('2️⃣  Logging in...');
    const loginResp = await makeRequest('POST', '/api/users/login',
      { 'Content-Type': 'application/json' },
      JSON.stringify({ email: userEmail, password: 'pass123' })
    );
    if (loginResp.status !== 200) {
      console.log('❌ Login failed:', loginResp.status, loginResp.data);
      return;
    }
    const token = loginResp.data.access_token;
    console.log(`✅ Logged in (Token: ${token.slice(0, 20)}...)\n`);

    // 3. Get jobs
    console.log('3️⃣  Fetching jobs...');
    const jobsResp = await makeRequest('GET', '/api/jobs/', {});
    if (jobsResp.status !== 200) {
      console.log('❌ Fetch jobs failed:', jobsResp.status);
      return;
    }
    const jobs = Array.isArray(jobsResp.data) ? jobsResp.data : [];
    if (jobs.length === 0) {
      console.log('❌ No jobs available');
      return;
    }
    const jobId = jobs[0].id;
    console.log(`✅ Found ${jobs.length} jobs (first job ID: ${jobId})\n`);

    // 4. Apply to job (using FormData-like multipart/form-data)
    console.log('4️⃣  Applying to job...');
    const boundary = '----FormBoundary' + Date.now();
    const resumeFileContent = 'This is a test resume for applying to job.';
    const multipartBody = [
      `--${boundary}`,
      'Content-Disposition: form-data; name="job_id"',
      '',
      String(jobId),
      `--${boundary}`,
      'Content-Disposition: form-data; name="candidate_id"',
      '',
      String(userId),
      `--${boundary}`,
      `Content-Disposition: form-data; name="resume"; filename="test_resume.txt"`,
      'Content-Type: text/plain',
      '',
      resumeFileContent,
      `--${boundary}--`,
    ].join('\r\n');

    const applyResp = await makeRequest('POST', '/api/applications/apply',
      { 'Content-Type': `multipart/form-data; boundary=${boundary}` },
      multipartBody
    );

    if (applyResp.status === 200) {
      console.log(`✅ Application submitted successfully!`);
      console.log(`   Response:`, applyResp.data);
    } else {
      console.log(`❌ Apply failed (${applyResp.status}):`, applyResp.data);
    }

  } catch (err) {
    console.error('❌ Test error:', err.message);
  }

  console.log('\n=== TEST COMPLETE ===\n');
}

test();
