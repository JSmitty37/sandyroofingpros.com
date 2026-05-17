// One-shot status pull — run with: node status_check.js
import "dotenv/config";
import Anthropic from "@anthropic-ai/sdk";
import { AGENT_MODEL, MAX_TOKENS } from "./config.js";
import { TOOL_DEFINITIONS, dispatch } from "./tools.js";

const SYSTEM_PROMPT = `You are the Smith Asset Group AI Agent. Pull live data and give a concise business status report covering: unrouted leads, partner pipeline, ad spend, and the top 3 action items Jackson should tackle today. Be direct and specific.`;

const client = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY });
const conversation = [{ role: "user", content: "Give me a full live status report on the business right now." }];

console.log("Pulling live data from Notion...\n");

while (true) {
  const response = await client.messages.create({
    model: AGENT_MODEL,
    max_tokens: MAX_TOKENS,
    system: SYSTEM_PROMPT,
    tools: TOOL_DEFINITIONS,
    messages: conversation,
  });

  conversation.push({ role: "assistant", content: response.content });

  if (response.stop_reason === "end_turn") {
    for (const block of response.content) {
      if (block.type === "text") console.log(block.text);
    }
    break;
  }

  if (response.stop_reason === "tool_use") {
    const toolResults = [];
    for (const block of response.content) {
      if (block.type !== "tool_use") continue;
      process.stdout.write(`  [${block.name}] `);
      try {
        const result = await dispatch(block.name, block.input);
        console.log("✓");
        toolResults.push({ type: "tool_result", tool_use_id: block.id, content: JSON.stringify(result) });
      } catch (err) {
        console.log(`✗ ${err.message}`);
        toolResults.push({ type: "tool_result", tool_use_id: block.id, is_error: true, content: err.message });
      }
    }
    conversation.push({ role: "user", content: toolResults });
  }
}
