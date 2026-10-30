# Notes

## Tools and Models Used

- **Cloudflare Workers AI:** `@cf/cloudflare/clef-flash` (for `comments.json`) and `@cf/cloudflare/clef` (for `comments-v2.json`).
- **Python 3:** Built using standard library modules (`urllib.request`, `json`, `re`, `os`, `sys`, `time`) without external package dependencies.
- **AI Coding Assistant:** Antigravity (powered by Gemini) for repository automation, API integration script, and formatting HTML visualizer reports.

## Honest Reflection

Doing this task showed the clear gap between fast AI classification and actual contextual understanding:

1. **Tone vs. Intent:** Clef often gets tricked by polite language. Several toxic remarks (sexist assumptions about grading, insulting the TA) were labeled "acceptable" simply because the sentences used polite grammar rather than overt profanity.
2. **Missing Meta-Narrative:** When a student quoted an offensive remark to report it to moderators, Clef labeled the report itself as toxic because it failed to grasp the context of reporting.
3. **The Need for Authentication / Gating:** A major takeaway was that text alone is insufficient for spam detection. A genuine professor's workshop link got flagged as spam due to promotional words, while a phishing link (`moodle-verify-cse.in`) passed as acceptable due to its formal tone. In a real system, user role gating (instructor vs. student) must happen before AI moderation.
4. **Overall Experience:** The task was straightforward to automate with AI tools, but reviewing the model's blind spots was the most insightful part. It proved that while AI drastically cuts down repetitive triage, human review and domain-specific gating remain indispensable.
