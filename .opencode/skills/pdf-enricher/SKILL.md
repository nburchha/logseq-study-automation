---
name: pdf-enricher
description: Extract PDF slide content, research missing context, and output comprehensive enriched Markdown.
---

## What I do
I transform sparse lecture slides (PDFs) into comprehensive, highly readable study materials. I extract the text using the `pdf_to_markdown` tool, identify "context deserts" (sparse bullet points), and use `websearch` to research the hidden context.

## When to use me
When the user asks to process, enrich, research, or summarize a lecture PDF document.

## Workflow
1. **Extract**: Call the `pdf_to_markdown` tool on the provided PDF file.
2. **Read**: Use the `read` tool to review the output markdown file.
3. **Research**: Identify sparse concepts or bullet points that lack explanation. Use the `websearch` tool to look up mechanisms, definitions, or factual consensus. Do not guess or hallucinate.
4. **Synthesize**: Combine the original slide structure with the researched context. 
5. **Output**: Save the final enriched text using the `write` tool (e.g., to `enriched_slides.md`), then state exactly: `ENRICHMENT_COMPLETE: Ready for Orchestrator chunking.`