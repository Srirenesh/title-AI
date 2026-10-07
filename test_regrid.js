const https = require('https');

const token = "eyJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJyZWdyaWQuY29tIiwiaWF0IjoxNzkxMzE2MDI4LCJleHAiOjE3OTM5MDgwMjgsInUiOjkwNDYwNSwiZyI6MjMxNTMsImNhcCI6InBhOnRzOnBzOmJmOm1hOnR5OmVvOnpvOnNiIn0.tKEXZ5USsXGPiSXH9XkcRpHZO-wBr_4Z_v2OGAJIdLI";
const query = encodeURIComponent("4320 NW CR 225, Lawtey, FL 32058");
const url = `https://app.regrid.com/api/v1/search/parcels?query=${query}&token=${token}`;

https.get(url, (res) => {
  let data = '';
  res.on('data', (chunk) => data += chunk);
  res.on('end', () => {
    console.log("Status Code:", res.statusCode);
    try {
      const parsed = JSON.parse(data);
      console.log("Response JSON:", JSON.stringify(parsed, null, 2).slice(0, 1500));
    } catch(e) {
      console.log("Raw Data:", data.slice(0, 500));
    }
  });
}).on('error', (err) => {
  console.error("Error:", err.message);
});
