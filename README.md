# Dynamic DNS
This is a tool if you have a local server with dynamic API address and you want it to automate the DNS records via Cloudflare

## Usage
1. Go to Cloudflare > Overview. Copy "Zone ID" (hex code)
2. Go to all subdomains which you want to be automated and write `autoupdate` in the comment
3. Go to [API Tokens](https://dash.cloudflare.com/profile/api-tokens)
4. Generate a token with DNS edit. Copy the token
5. Paste the 2 tokens in the script
6. Run the script in your computer