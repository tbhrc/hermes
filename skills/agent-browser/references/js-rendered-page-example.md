# JS-Rendered Page Automation Example
## Task
Extract first 3 jobs from Talent Bridge Dubai careers page (JS-rendered Manatal site).

## Steps Taken
1. Dump homepage with mobile UA to find jobs link:
   `/opt/google-chrome/chrome --headless=new --no-sandbox --user-agent="Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1" --dump-dom https://talentbridgedubai.com > /tmp/talentbridge_home.html 2>&1`
2. Found jobs link to `https://talent-bridge-dubai.careers-page.com/`
3. Dump careers page with virtual time budget for JS rendering:
   `/opt/google-chrome/chrome --headless=new --no-sandbox --user-agent="Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1" --virtual-time-budget=5000 --dump-dom https://talent-bridge-dubai.careers-page.com/ > /tmp/talentbridge_careers.html 2>&1`
4. Extract structured content via `web_extract` tool for verified job listings.

## Result
Successfully extracted 3 jobs:
1. Marketing Executive | Email Campaign Specialist
2. Yacht Hostess (Cabin Crew Background)
3. HRBP | HR Generalist