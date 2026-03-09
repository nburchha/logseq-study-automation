import { tool } from "@opencode-ai/plugin"

export default tool({
  description: "Convert a PDF file to clean Markdown using MarkItDown",
  args: {
    pdfPath: tool.schema.string().describe("Path to the input PDF file"),
    outputPath: tool.schema.string().describe("Path to save the output Markdown file"),
  },
  async execute(args, context) {
    try {
      // Bun.$ is OpenCode's native way to execute shell commands
      const result = await Bun.$`markitdown ${args.pdfPath} > ${args.outputPath}`.text()
      return `Successfully converted ${args.pdfPath} to ${args.outputPath}.\n${result}`
    } catch (error) {
      return `Failed to convert PDF: ${error}`
    }
  },
})