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
  description: "Write structured content into Logseq files",
  args: {
    file_path: tool.schema.string().describe("Absolute or workspace-relative Logseq markdown path"),
    content: tool.schema.string().describe("Content to write into the Logseq file"),
    mode: tool.schema.enum(["create", "overwrite", "append", "append_child_to_block"]).describe("Write mode"),
    parent_block_query: tool.schema.string().optional().describe("Parent block text to match when appending a child block"),
  },
  async execute(args, context) {
    const script = path.join(context.worktree, "skills", "write-to-logseq", "handler.py")
    const command = [
      "python3",
      script,
      "--file_path",
      resolvePath(args.file_path, context.worktree),
      "--content",
      args.content,
      "--mode",
      args.mode,
    ]

    if (args.parent_block_query) {
      command.push("--parent_block_query", args.parent_block_query)
    }

    return runPython(command)
  },
})
