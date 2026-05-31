#!/usr/bin/env node
import { readFile } from 'node:fs/promises'
import path from 'node:path'
import process from 'node:process'
import { chromium } from 'playwright'

const DEFAULT_BASE_URL = 'http://127.0.0.1:8188'

function usage() {
  console.error(`Usage: node scripts/gui_workflow_smoke.mjs [options] <workflow.json>

Loads a ComfyUI GUI workflow in the real frontend, calls app.graphToPrompt(),
and optionally submits the converted API prompt to ComfyUI.

Options:
  --base-url URL      ComfyUI URL (default: ${DEFAULT_BASE_URL})
  --submit           POST converted prompt to /prompt
  --wait             Wait for /history/<prompt_id> after --submit
  --timeout SEC      Navigation/history timeout (default: 600)
  --debug            Print browser console messages
  -h, --help         Show this help
`)
}

function parseArgs(argv) {
  const opts = {
    baseUrl: DEFAULT_BASE_URL,
    submit: false,
    wait: false,
    timeoutSec: 600,
    debug: false,
    workflowPath: null,
  }

  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i]
    if (arg === '-h' || arg === '--help') {
      usage()
      process.exit(0)
    } else if (arg === '--base-url') {
      opts.baseUrl = argv[++i]
    } else if (arg === '--submit') {
      opts.submit = true
    } else if (arg === '--wait') {
      opts.wait = true
    } else if (arg === '--timeout') {
      opts.timeoutSec = Number(argv[++i])
    } else if (arg === '--debug') {
      opts.debug = true
    } else if (arg.startsWith('-')) {
      throw new Error(`unknown option: ${arg}`)
    } else if (!opts.workflowPath) {
      opts.workflowPath = arg
    } else {
      throw new Error(`unexpected argument: ${arg}`)
    }
  }

  if (!opts.workflowPath) {
    usage()
    throw new Error('workflow path is required')
  }
  if (!Number.isFinite(opts.timeoutSec) || opts.timeoutSec <= 0) {
    throw new Error('--timeout must be a positive number')
  }
  return opts
}

async function getJson(baseUrl, route) {
  const res = await fetch(`${baseUrl}${route}`)
  if (!res.ok) {
    throw new Error(`GET ${route} failed: HTTP ${res.status} ${await res.text()}`)
  }
  return res.json()
}

async function postJson(baseUrl, route, payload) {
  const res = await fetch(`${baseUrl}${route}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })
  const text = await res.text()
  let body = {}
  if (text) {
    try {
      body = JSON.parse(text)
    } catch {
      body = { raw: text }
    }
  }
  if (!res.ok) {
    throw new Error(`POST ${route} failed: HTTP ${res.status} ${JSON.stringify(body)}`)
  }
  return body
}

async function waitForHistory(baseUrl, promptId, timeoutSec) {
  const deadline = Date.now() + timeoutSec * 1000
  while (Date.now() < deadline) {
    const history = await getJson(baseUrl, `/history/${promptId}`)
    if (history[promptId]) {
      return history[promptId]
    }
    await new Promise((resolve) => setTimeout(resolve, 2000))
  }
  throw new Error(`timed out waiting for prompt ${promptId}`)
}

async function waitForFrontendPrompt(page, timeoutSec) {
  return page.evaluate(async (timeoutMs) => {
    const app = window.app || window.comfyAPI?.app?.app
    const deadline = Date.now() + timeoutMs
    let lastPrompt = null
    let lastMissing = []

    while (Date.now() < deadline) {
      lastPrompt = await app.graphToPrompt()
      lastMissing = Object.entries(lastPrompt.output ?? {})
        .filter(([, node]) => !node?.class_type)
        .map(([id]) => id)

      if (Object.keys(lastPrompt.output ?? {}).length && lastMissing.length === 0) {
        return {
          output: lastPrompt.output,
          workflow: lastPrompt.workflow,
          nodeCount: Object.keys(lastPrompt.output ?? {}).length,
          workflowNodeCount: lastPrompt.workflow?.nodes?.length ?? null,
          workflowLinkCount: lastPrompt.workflow?.links?.length ?? null,
        }
      }

      await new Promise((resolve) => setTimeout(resolve, 250))
    }

    throw new Error(
      `frontend graphToPrompt() did not produce class_type for nodes: ${lastMissing.join(', ')}`,
    )
  }, timeoutSec * 1000)
}

function collectOutputFiles(historyEntry) {
  const files = []
  for (const output of Object.values(historyEntry.outputs ?? {})) {
    for (const image of output.images ?? []) {
      files.push([image.subfolder, image.filename].filter(Boolean).join('/'))
    }
    for (const gif of output.gifs ?? []) {
      files.push([gif.subfolder, gif.filename].filter(Boolean).join('/'))
    }
  }
  return files
}

async function main() {
  const opts = parseArgs(process.argv.slice(2))
  const workflowPath = path.resolve(opts.workflowPath)
  const workflow = JSON.parse(await readFile(workflowPath, 'utf8'))

  const browser = await chromium.launch({ headless: true })
  const page = await browser.newPage()
  const consoleMessages = []

  page.on('console', (message) => {
    const line = `${message.type()}: ${message.text()}`
    consoleMessages.push(line)
    if (opts.debug) console.error(`[browser] ${line}`)
  })
  page.on('pageerror', (error) => {
    consoleMessages.push(`pageerror: ${error.message}`)
    if (opts.debug) console.error(`[browser] pageerror: ${error.stack ?? error.message}`)
  })

  try {
    await page.goto(opts.baseUrl, {
      waitUntil: 'domcontentloaded',
      timeout: opts.timeoutSec * 1000,
    })

    await page.waitForFunction(
      () => {
        const app = window.app || window.comfyAPI?.app?.app
        return Boolean(
          app?.canvas &&
            app?.rootGraph &&
            typeof app.loadGraphData === 'function' &&
            typeof app.graphToPrompt === 'function',
        )
      },
      undefined,
      { timeout: opts.timeoutSec * 1000 },
    )

    await page.evaluate(async (graphData) => {
      const app =
        window.app ||
        window.comfyAPI?.app?.app

      if (!app) throw new Error('ComfyUI app object was not found')
      if (typeof app.loadGraphData !== 'function') {
        throw new Error('ComfyUI app.loadGraphData() was not found')
      }
      if (typeof app.graphToPrompt !== 'function') {
        throw new Error('ComfyUI app.graphToPrompt() was not found')
      }

      await app.loadGraphData(graphData)
      await new Promise((resolve) => requestAnimationFrame(() => resolve()))
    }, workflow)

    const result = await waitForFrontendPrompt(page, opts.timeoutSec)

    if (!result.output || !Object.keys(result.output).length) {
      throw new Error('frontend graphToPrompt() returned an empty API prompt')
    }

    console.log(
      `PASS frontend conversion: ${result.nodeCount} API nodes, ` +
        `${result.workflowNodeCount ?? '?'} workflow nodes, ` +
        `${result.workflowLinkCount ?? '?'} workflow links`,
    )

    if (opts.submit) {
      const response = await postJson(opts.baseUrl, '/prompt', {
        prompt: result.output,
        client_id: crypto.randomUUID(),
        extra_data: {
          extra_pnginfo: {
            workflow: result.workflow,
          },
        },
      })

      if (response.node_errors && Object.keys(response.node_errors).length) {
        throw new Error(`ComfyUI node_errors: ${JSON.stringify(response.node_errors)}`)
      }

      console.log(`PASS prompt submit: ${response.prompt_id}`)

      if (opts.wait) {
        const history = await waitForHistory(opts.baseUrl, response.prompt_id, opts.timeoutSec)
        const status = history.status ?? {}
        if (status.status_str !== 'success' || status.completed !== true) {
          throw new Error(`prompt did not complete successfully: ${JSON.stringify(status)}`)
        }
        const files = collectOutputFiles(history)
        console.log(`PASS prompt history: ${files.length ? files.join(', ') : 'no saved outputs'}`)
      }
    }
  } catch (error) {
    console.error(`FAIL ${error.stack ?? error.message}`)
    const relevantConsole = consoleMessages.filter((line) => {
      return /error|warn|missing|failed|corrupt|exception/i.test(line)
    })
    if (relevantConsole.length) {
      console.error('Relevant browser console messages:')
      for (const line of relevantConsole.slice(-40)) console.error(`  ${line}`)
    }
    process.exitCode = 1
  } finally {
    await browser.close()
  }
}

main().catch((error) => {
  console.error(`FAIL ${error.stack ?? error.message}`)
  process.exit(1)
})
