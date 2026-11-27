// main.ts — "The World — 27 November 2026" entry program.
//
// Copies the pre-drawn entry.png (built by draw.py in this repository)
// to the output directory, after validating it is a whole, well-formed
// PNG of exactly 1024 x 1024 pixels and at most 1 MiB. The copy is
// written atomically (temporary file + rename) so the two grader runs
// always produce byte-identical output. Node 22 standard library only.
import { copyFileSync, mkdirSync, readFileSync, renameSync, statSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const PNG_SIGNATURE = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
const MAX_BYTES = 1048576; // 1 MiB
const EXPECTED_WIDTH = 1024;
const EXPECTED_HEIGHT = 1024;

function fail(message: string): never {
  throw new Error(`entry.png validation failed: ${message}`);
}

function main(): void {
  const here = dirname(fileURLToPath(import.meta.url));
  const source = join(here, "entry.png");
  const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
  const target = join(outDir, "entry.png");

  const bytes = readFileSync(source);
  if (bytes.length > MAX_BYTES) {
    fail(`size ${bytes.length} bytes exceeds ${MAX_BYTES}`);
  }
  if (bytes.length < 8 + 25 || !bytes.subarray(0, 8).equals(PNG_SIGNATURE)) {
    fail("missing PNG signature");
  }
  // First chunk must be IHDR: length 13, type "IHDR", then width/height.
  const ihdrLength = bytes.readUInt32BE(8);
  const ihdrType = bytes.subarray(12, 16).toString("ascii");
  if (ihdrLength !== 13 || ihdrType !== "IHDR") {
    fail(`first chunk is not IHDR (length ${ihdrLength}, type ${ihdrType})`);
  }
  const width = bytes.readUInt32BE(16);
  const height = bytes.readUInt32BE(20);
  if (width !== EXPECTED_WIDTH || height !== EXPECTED_HEIGHT) {
    fail(`dimensions ${width}x${height}, expected ${EXPECTED_WIDTH}x${EXPECTED_HEIGHT}`);
  }
  // Whole-file check: the final 12 bytes must be the IEND chunk.
  const iendLength = bytes.readUInt32BE(bytes.length - 12);
  const iendType = bytes.subarray(bytes.length - 8, bytes.length - 4).toString("ascii");
  if (iendLength !== 0 || iendType !== "IEND") {
    fail("missing IEND chunk");
  }

  // Atomic copy: write to a temp file in the output dir, then rename.
  mkdirSync(outDir, { recursive: true });
  const tmp = join(outDir, `.entry.png.tmp-${process.pid}`);
  copyFileSync(source, tmp);
  if (statSync(tmp).size !== bytes.length) {
    fail("temporary copy has the wrong size");
  }
  renameSync(tmp, target);
  console.log(`wrote ${target} (${bytes.length} bytes, ${width}x${height})`);
}

main();
