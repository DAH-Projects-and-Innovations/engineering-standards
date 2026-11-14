# Security policy

## Reporting a vulnerability

**Do not open a public issue for a security problem.**

This repository contains reusable CI workflows and hooks that many DAH Labs repositories run. A weakness here (for example a script injection in a workflow, or an action pinned to a compromised version) can affect every project.

Report it privately:

1. Go to the **Security** tab of this repository.
2. Click **Report a vulnerability** (GitHub private vulnerability reporting).
3. Describe the problem, the affected file and version, and how to reproduce it.

If you cannot use GitHub, write to **TODO: security contact e-mail address of DAH Labs**.

We acknowledge reports within **5 working days**, keep you informed, and credit you in the advisory unless you prefer to stay anonymous.

## Supported versions

Only the latest release of each major version (`v1`) receives security fixes. Projects that call the workflows with `@v1` get the fixes automatically.

## Security problems in other DAH Labs repositories

Use the **Report a vulnerability** button of the affected repository. If it is not available, use the contact above.
