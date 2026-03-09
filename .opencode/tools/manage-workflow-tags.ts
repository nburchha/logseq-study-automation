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
  description: "Update workflow tags in Logseq files or blocks",
  args: {
    file_path: tool.schema.string().describe("Absolute or workspace-relative Logseq markdown path"),
    action: tool.schema.enum(["add", "remove", "replace"]).describe("Tag update action"),
    tag: tool.schema.string().optional().describe("Tag to add or remove"),
    old_tag: tool.schema.string().optional().describe("Tag to replace"),
    new_tag: tool.schema.string().optional().describe("Replacement tag"),
    block_id: tool.schema.string().optional().describe("Optional target block UUID"),
    block_content: tool.schema.string().optional().describe("Optional target block text snippet"),
  },
  async execute(args, context) {
    const script = path.join(context.worktree, "skills", "manage-workflow-tags", "handler.py")
    const command = [
      "python3",
      script,
      "--file_path",
      resolvePath(args.file_path, context.worktree),
      "--action",
      args.action,
    ]

    if (args.tag) command.push("--tag", args.tag)
    if (args.old_tag) command.push("--old_tag", args.old_tag)
    if (args.new_tag) command.push("--new_tag", args.new_tag)
    if (args.block_id) command.push("--block_id", args.block_id)
    if (args.block_content) command.push("--block_content", args.block_content)

    return runPython(command)
  },
})
