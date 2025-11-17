// get-reddit-refresh-token.js
// Usage: node get-reddit-refresh-token.js <CLIENT_ID> "UserAgent/1.0"
const http = require('http');
const https = require('https');
const { URLSearchParams } = require('url');
const { spawn } = require('child_process');

const CLIENT_ID   = process.argv[2] || process.env.REDDIT_CLIENT_ID;
const USER_AGENT  = process.argv[3] || process.env.REDDIT_USER_AGENT || 'azure-noob-blog-publisher';
const REDIRECT    = 'http://localhost:8080/callback';
const PORT        = 8080;

if (!CLIENT_ID) {
  console.error('Provide CLIENT_ID: node get-reddit-refresh-token.js <CLIENT_ID> "UserAgent/1.0"');
  process.exit(1);
}

// 1) Build auth URL (installed app; empty secret)
const scopes = ['read','submit','identity','flair'];
const params = new URLSearchParams({
  client_id: CLIENT_ID,
  response_type: 'code',
  state: Math.random().toString(36).slice(2),
  redirect_uri: REDIRECT,
  duration: 'permanent',
  scope: scopes.join(' ')
});
const AUTH_URL = `https://www.reddit.com/api/v1/authorize?${params.toString()}`;

function open(url) {
  const cmd = process.platform === 'win32' ? 'cmd' : (process.platform === 'darwin' ? 'open' : 'xdg-open');
  const args = process.platform === 'win32' ? ['/c','start', '', url] : [url];
  spawn(cmd, args, { stdio: 'ignore', detached: true }).unref();
}

function exchangeCodeForTokens(code) {
  return new Promise((resolve, reject) => {
    const body = new URLSearchParams({
      grant_type: 'authorization_code',
      code,
      redirect_uri: REDIRECT
    }).toString();

    // Basic auth header is base64("client_id:") — empty secret for installed apps
    const auth = Buffer.from(`${CLIENT_ID}:`).toString('base64');

    const req = https.request({
      method: 'POST',
      hostname: 'www.reddit.com',
      path: '/api/v1/access_token',
      headers: {
        'Authorization': `Basic ${auth}`,
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': USER_AGENT,
        'Content-Length': Buffer.byteLength(body)
      }
    }, res => {
      let data = '';
      res.on('data', d => data += d);
      res.on('end', () => {
        try {
          const json = JSON.parse(data);
          if (json.error) return reject(json);
          resolve(json);
        } catch (e) { reject(e); }
      });
    });

    req.on('error', reject);
    req.write(body);
    req.end();
  });
}

// 2) Start local server to catch the redirect
const server = http.createServer(async (req, res) => {
  if (!req.url.startsWith('/callback')) {
    res.writeHead(404); res.end('Not found'); return;
  }
  const q = new URL(req.url, `http://localhost:${PORT}`).searchParams;
  const code = q.get('code');
  const state = q.get('state');

  if (!code) { res.writeHead(400); res.end('Missing code'); return; }

  try {
    const tokens = await exchangeCodeForTokens(code);
    res.writeHead(200, {'Content-Type': 'text/plain'});
    res.end('All set! You can close this tab.\n');
    console.log('\n✅ SUCCESS');
    console.log('ACCESS TOKEN :', tokens.access_token);
    console.log('REFRESH TOKEN:', tokens.refresh_token);
    console.log('\nAdd REFRESH TOKEN to GitHub secret: REDDIT_REFRESH_TOKEN');
  } catch (e) {
    res.writeHead(500, {'Content-Type': 'text/plain'});
    res.end('Token exchange failed. See console.');
    console.error('Token exchange failed:', e);
  } finally {
    setTimeout(() => server.close(), 500);
  }
});

server.listen(PORT, () => {
  console.log('Opening browser for Reddit authorization…');
  console.log('If it does not open, navigate to:\n', AUTH_URL, '\n');
  open(AUTH_URL);
});
