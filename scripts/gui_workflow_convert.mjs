#!/usr/bin/env node
import { readFile, writeFile } from 'node:fs/promises'
import path from 'node:path'
import process from 'node:process'
import { chromium } from 'playwright'

const DEFAULT_BASE_URL = 'http://127.0.0.1:8188'

function usage() {
  console.error(`Usage: node scripts/gui_workflow_convert.mjs [options] <workflow.json>

Loads a ComfyUI GUI workflow in the real frontend, calls app.graphToPrompt(),
and writes the converted API prompt data to a JSON file.

Options:
  --base-url URL      ComfyUI URL (default: ${DEFAULT_BASE_URL})
  --output PATH      Write converted API prompt data to PATH
  --timeout SEC      Navigation/conversion timeout (default: 600)
  --debug            Print browser console messages
  -h, --help         Show this help
`)
}

function parseArgs(argv) {
  const opts = {
    baseUrl: DEFAULT_BASE_URL,
    outputPath: null,
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
    } else if (arg === '--output') {
      opts.outputPath = argv[++i]
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
  if (!opts.outputPath) {
    usage()
    throw new Error('--output path is required')
  }
  if (!Number.isFinite(opts.timeoutSec) || opts.timeoutSec <= 0) {
    throw new Error('--timeout must be a positive number')
  }
  return opts
}

async function waitForFrontendPrompt(page, timeoutSec, expectedWorkflow) {
  return page.evaluate(async ({ timeoutMs, expected }) => {
    const app = window.app || window.comfyAPI?.app?.app
    const deadline = Date.now() + timeoutMs
    let lastPrompt = null
    let lastMissing = []
    let lastMismatch = ''
    let lastReload = 0

    while (Date.now() < deadline) {
      lastPrompt = await app.graphToPrompt()
      lastMissing = Object.entries(lastPrompt.output ?? {})
        .filter(([, node]) => !node?.class_type)
        .map(([id]) => id)
      const workflow = lastPrompt.workflow ?? {}
      const matchesExpected =
        workflow.id === expected.id &&
        (workflow.nodes?.length ?? null) === expected.nodeCount &&
        (workflow.links?.length ?? null) === expected.linkCount

      if (
        Object.keys(lastPrompt.output ?? {}).length &&
        lastMissing.length === 0 &&
        matchesExpected
      ) {
        return {
          output: lastPrompt.output,
          workflow,
          nodeCount: Object.keys(lastPrompt.output ?? {}).length,
          workflowNodeCount: workflow.nodes?.length ?? null,
          workflowLinkCount: workflow.links?.length ?? null,
        }
      }

      lastMismatch =
        `workflow id ${workflow.id ?? '<missing>'}, ` +
        `${workflow.nodes?.length ?? 0} nodes, ${workflow.links?.length ?? 0} links`

      if (!matchesExpected && Date.now() - lastReload > 1000) {
        lastReload = Date.now()
        await app.loadGraphData(expected.graphData)
        await new Promise((resolve) => requestAnimationFrame(() => resolve()))
      }

      await new Promise((resolve) => setTimeout(resolve, 250))
    }

    throw new Error(
      `frontend graphToPrompt() did not produce the expected workflow; ` +
        `last missing class_type nodes: ${lastMissing.join(', ') || 'none'}; ` +
        `last converted workflow: ${lastMismatch}`,
    )
  }, {
    timeoutMs: timeoutSec * 1000,
    expected: {
      id: expectedWorkflow.id,
      nodeCount: expectedWorkflow.nodes?.length ?? null,
      linkCount: expectedWorkflow.links?.length ?? null,
      graphData: expectedWorkflow,
    },
  })
}

async function main() {
  const opts = parseArgs(process.argv.slice(2))
  const workflowPath = path.resolve(opts.workflowPath)
  const outputPath = path.resolve(opts.outputPath)
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

    await page.waitForTimeout(1500)

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

    const result = await waitForFrontendPrompt(page, opts.timeoutSec, workflow)

    if (!result.output || !Object.keys(result.output).length) {
      throw new Error('frontend graphToPrompt() returned an empty API prompt')
    }

    console.log(
      `MJS workflow conversion ok: ${result.nodeCount} API nodes, ` +
        `${result.workflowNodeCount ?? '?'} workflow nodes, ` +
        `${result.workflowLinkCount ?? '?'} workflow links`,
    )

    await writeFile(
      outputPath,
      JSON.stringify(
        {
          prompt: result.output,
          workflow: result.workflow,
          node_count: result.nodeCount,
          workflow_node_count: result.workflowNodeCount,
          workflow_link_count: result.workflowLinkCount,
        },
        null,
        2,
      ) + '\n',
    )
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
