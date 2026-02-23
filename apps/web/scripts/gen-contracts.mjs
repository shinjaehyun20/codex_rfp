import { promises as fs } from "node:fs";
import path from "node:path";
import { compileFromFile } from "json-schema-to-typescript";

const root = path.resolve(process.cwd(), "..", "..");
const schemaDir = path.join(root, "contracts", "schemas");
const outFile = path.join(process.cwd(), "src", "lib", "contracts.ts");

const files = [
  "envelope.v1.schema.json",
  "artifact.v1.schema.json",
  "stateref.v1.schema.json",
  "rfp.meta.v1.schema.json",
  "rfp.parsed.v1.schema.json",
  "requirements.v1.schema.json",
  "evaluation.v1.schema.json",
  "mapping.v1.schema.json",
  "proposal.draft.v1.schema.json",
  "compliance.v1.schema.json",
  "case.analysis.v1.schema.json",
];

let out = "";
out += "/* eslint-disable */\n";
out += "/* This file is auto-generated. Do not edit manually. */\n\n";

for (const f of files) {
  const p = path.join(schemaDir, f);
  const ts = await compileFromFile(p, { bannerComment: "" });
  out += ts + "\n\n";
}

await fs.writeFile(outFile, out, "utf8");
console.log(`Generated: ${outFile}`);
