const axios = require('axios');
const FormData = require('form-data');
const fs = require('fs');

const API = 'http://localhost:8001/api';

let testUser = null;
let testCandidate = null;

// Sample resume text
const resumeText = `
John Doe
john@example.com
(555) 123-4567

PROFESSIONAL SUMMARY
Experienced software developer with 5+ years in full-stack web development.

SKILLS
- JavaScript, Python, React, Node.js
- SQL, MongoDB, PostgreSQL
- AWS, Docker, Kubernetes
- REST APIs, GraphQL

WORK EXPERIENCE
Senior Developer at Tech Corp (2020-Present)
- Led development of microservices architecture
- Improved performance by 40%
- Mentored junior developers

EDUCATION
Bachelor of Science in Computer Science
State University, Graduated 2018
`;

async function testHistoryFlow() {
  try {
    console.log('=== Testing History Feature ===\n');

    // Step 1: Create a test user
    console.log('1. Registering test user...');
    const registerRes = await axios.post(API + '/users/register', {
      email: `test${Date.now()}@example.com`,
      password: 'TestPassword123!',
      full_name: 'History Test User',
      role: 'candidate',
    });
    testUser = registerRes.data;
    testCandidate = testUser.id;
    console.log(`✓ User registered with ID: ${testCandidate}\n`);

    // Step 2: Upload resume and score it
    console.log('2. Uploading resume for scoring...');
    const resumeBuffer = Buffer.from(resumeText);
    const form = new FormData();
    form.append('resume', resumeBuffer, 'test_resume.txt');

    const scoreRes = await axios.post(API + '/applications/score', form, {
      headers: form.getHeaders(),
    });
    
    console.log(`✓ Resume scored. Received ${scoreRes.data.length} matches\n`);
    
    // Show first few matches
    if (scoreRes.data.length > 0) {
      console.log('Sample matches from scoring:');
      scoreRes.data.slice(0, 2).forEach((match, idx) => {
        console.log(`  ${idx + 1}. ${match.job_title} - Score: ${(match.score * 100).toFixed(1)}%`);
      });
      console.log();
    }

    // Step 3: Fetch history to verify it was saved
    console.log('3. Fetching history from backend...');
    const historyRes = await axios.get(API + '/applications/history', {
      headers: {
        'Authorization': `Bearer ${testUser.token || 'test'}`
      }
    });

    console.log(`✓ History retrieved. Found ${historyRes.data.length} searches\n`);

    // Step 4: Display history details
    if (historyRes.data.length > 0) {
      const latestSearch = historyRes.data[0];
      console.log('Latest search history:');
      console.log(`  Search ID: ${latestSearch.search_id}`);
      console.log(`  Candidate ID: ${latestSearch.candidate_id}`);
      console.log(`  Resume: ${latestSearch.resume_path}`);
      console.log(`  Created: ${latestSearch.created_at}`);
      console.log(`  Results: ${latestSearch.results.length} matches`);
      
      if (latestSearch.results.length > 0) {
        console.log('\n  Top 3 matches:');
        latestSearch.results.slice(0, 3).forEach((result, idx) => {
          const scorePercent = Math.round(result.score * 100);
          console.log(`    ${idx + 1}. ${result.job_title} - ${scorePercent}% match`);
          if (result.matched_skills && result.matched_skills.length > 0) {
            console.log(`       Skills: ${result.matched_skills.join(', ')}`);
          }
        });
      }
    } else {
      console.log('⚠ No history found - backend may not be storing search results');
    }

    console.log('\n✓ History flow test completed successfully!');

  } catch (err) {
    console.error('❌ Test failed:', err.response?.data || err.message);
    process.exit(1);
  }
}

testHistoryFlow();
