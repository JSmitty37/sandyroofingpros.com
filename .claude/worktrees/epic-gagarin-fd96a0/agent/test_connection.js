import "dotenv/config";

const dbs = {
  "Live Leads":        "8bc8b705-8629-4b17-ac80-f84adce107a8",
  "Partner Directory": "24f3a86e-c101-4d49-8a2a-d062d9d6a19b",
  "Ad Metrics":        "47d3c105-4ffa-4a9e-8455-66a4c1c3c355",
  "Finances & P&L":   "8458dc3f-6b78-4f3c-9b42-b5dd143ecdfa",
};

const headers = {
  "Authorization":  `Bearer ${process.env.NOTION_API_KEY}`,
  "Notion-Version": "2022-06-28",
  "Content-Type":   "application/json",
};

console.log("Testing Notion API connections...\n");
for (const [name, id] of Object.entries(dbs)) {
  const res = await fetch(`https://api.notion.com/v1/databases/${id}`, { headers });
  if (res.ok) {
    const data = await res.json();
    const title = data.title?.[0]?.plain_text ?? "(no title)";
    console.log(`✓  ${name.padEnd(22)} — "${title}"`);
  } else {
    const body = await res.text();
    console.log(`✗  ${name.padEnd(22)} — ${res.status}: ${body}`);
  }
}
console.log("\nDone.");
