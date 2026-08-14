import { copyFile, mkdir, readFile } from 'node:fs/promises'
import { dirname, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..')
const outputDirectory = resolve(root, 'dist/lucky-skills/evidence')

const evidenceFiles = [
  'lucky-v3-endpoints.json',
  'lucky-v3-runtime-verification.json'
]

await mkdir(outputDirectory, { recursive: true })

for (const filename of evidenceFiles) {
  const source = resolve(root, 'evidence', filename)
  const destination = resolve(outputDirectory, filename)

  // Fail the docs build if a canonical evidence file is missing or invalid.
  JSON.parse(await readFile(source, 'utf8'))
  await copyFile(source, destination)
}

console.log(`Published ${evidenceFiles.length} evidence JSON files to dist/lucky-skills/evidence`)
