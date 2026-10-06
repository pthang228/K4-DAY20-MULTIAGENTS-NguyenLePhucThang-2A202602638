---
name: verify-artifacts-and-environment
description: Use before finishing any task that runs scripts or writes files, to confirm the interpreter, paths, and final artifacts are correct.
---
- Probe which interpreter/commands actually exist instead of assuming an alias is available.
- Confirm required input files exist at the paths you intend to open before running.
- Run scripts from a working directory that makes relative paths valid, or use absolute paths.
- After producing outputs, read them back and confirm they parse and contain the required content.
- Skip any internal validation step that cannot produce visible output; write a script file and run it instead of fighting complex inline quoting.
- Delete only temporary files you created; never remove required deliverables.
- Re-run the final validation command after cleanup to confirm nothing required was removed or broken.
