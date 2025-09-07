#!/usr/bin/env node
const fs = require('fs')
const path = require('path')

function parseEnv(file) {
  const env = {}
  if (!fs.existsSync(file)) return env
  for (const line of fs.readFileSync(file, 'utf8').split(/\r?\n/)) {
    const m = line.match(/^([^#=]+)=(.*)$/)
    if (m) env[m[1].trim()] = m[2].trim()
  }
  return env
}

const env = parseEnv(path.resolve('.env.ci'))
const apiBase = env.VITE_API_BASE || ''
console.log('VITE_API_BASE from .env.ci:', apiBase)
if (!apiBase) {
  console.error('VITE_API_BASE is missing in .env.ci')
  process.exit(1)
}
const viteConfig = fs.readFileSync(path.join('frontend', 'vite.config.ts'), 'utf8')
if (viteConfig.includes('http://localhost:8000')) {
  console.error('vite.config.ts should not reference http://localhost:8000')
  process.exit(1)
}
const targetLine = viteConfig
  .split('\n')
  .find((l) => l.includes('target'))
console.log('vite.config.ts target line:', targetLine?.trim())
if (apiBase !== 'http://backend:8000') {
  console.error('VITE_API_BASE should be http://backend:8000 in CI')
  process.exit(1)
}
console.log('Frontend config check passed.')
