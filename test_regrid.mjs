import https from 'node:https';

const token = "eyJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJyZWdyaWQuY29tIiwiaWF0IjoxNzkxMzE2MDI4LCJleHAiOjE3OTM5MDgwMjgsInUiOjkwNDYwNSwiZyI6MjMxNTMsImNhcCI6InBhOnRzOnBzOmJmOm1hOnR5OmVvOnpvOnNiIn0.tKEXZ5USsXGPiSXH9XkcRpHZO-wBr_4Z_v2OGAJIdLI";

const url = `https://app.regrid.com/api/v1/search.json?query=${encodeURIComponent("4320 NW CR 225")}&token=${token}`;

https.get(url, res => {
  let data = '';
  res.on('data', chunk => data += chunk);
  res.on('end', () => {
    const parsed = JSON.parse(data);
    if (parsed.results && parsed.results.length > 0) {
      console.log("FIELDS of result[0]:", JSON.stringify(parsed.results[0].properties, null, 2));
    }
  });
});
