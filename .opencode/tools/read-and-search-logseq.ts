import path from "path"
import { tool } from "@opencode-ai/plugin"

function resolvePath(filePath: string, worktree: string) {
  return path.isAbsolute(filePath) ? filePath : path.join(worktree, filePath)
}

async function runPython(args: string[]) {
  const proc = Bun.spawn(args, {
    stdout: "pipe",
    stderr: "pipe",
  })

  const stdout = await new Response(proc.stdout).text()
  const stderr = await new Response(proc.stderr).text()
  const exitCode = await proc.exited

  if (exitCode !== 0) {
    throw new Error(stderr.trim() || stdout.trim() || `Command failed with exit code ${exitCode}`)
  }

  return stdout.trim()
}

export default tool({
  description: "Read or search the Logseq graph",
  args: {
    action: tool.schema.enum(["read", "search"]).describe("Whether to read a file or search the graph"),
    file_path: tool.schema.string().optional().describe("Target file path when action is read"),
    query: tool.schema.string().optional().describe("Search query when action is search"),
    search_scope: tool.schema.enum(["file", "block"]).optional().describe("Search result granularity"),
  },
  async execute(args, context) {
    const script = path.join(context.worktree, "skills", "read-and-search-logseq", "handler.py")
    const command = ["python3", script, "--action", args.action]

    if (args.file_path) {
      command.push("--file_path", resolvePath(args.file_path, context.worktree))
    }

    if (args.query) {
      command.push("--query", args.query)
    }

    if (args.search_scope) {
      command.push("--search_scope", args.search_scope)
    }

    return runPython(command)
  },
})
