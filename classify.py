import json
import os
import re
import sys
import time
import urllib.error
import urllib.request

INSTRUCTIONS = "Classify `comment`, a post from a college course forum where students discuss assignments, ask questions, share projects, and exchange peer feedback."

CRITERIA = {
    "acceptable": "Appropriate course discussion, academic doubt, project feedback, tips, polite criticism of coursework, or self-deprecating remarks.",
    "toxic": "Hostile, abusive, insulting, mocking, discriminatory, or harassing remarks directed at peers or instructors.",
    "spam": "Commercial advertisements, paid assignment cheating services, self-promotional links, crypto schemes, or scams."
}

def load_credentials(creds_path="cloud-flare.local.sh"):
    with open(creds_path, "r", encoding="utf-8") as f:
        content = f.read()
    creds = dict(re.findall(r'export (\w+)="([^"]*)"', content))
    return creds["CLOUDFLARE_ACCOUNT_ID"].strip(), creds["CLOUDFLARE_API_TOKEN"].strip()

def classify_comment(account, token, model, comment_text):
    url = f"https://api.cloudflare.com/client/v4/accounts/{account}/ai/run/@cf/cloudflare/{model}"
    payload = {
        "state": {"comment": comment_text},
        "questions": {
            "moderation": {
                "type": "choice",
                "instructions": INSTRUCTIONS,
                "criteria": CRITERIA
            }
        }
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        method="POST",
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    )

    for attempt in range(5):
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                res = json.load(resp)
                if res.get("success"):
                    ans = res["result"]["answers"]["moderation"]
                    return {
                        "choice": ans.get("choice", "unknown"),
                        "confidence": ans.get("confidence", 0),
                        "probabilities": ans.get("probabilities", {})
                    }
                raise RuntimeError(f"API Error: {res.get('errors')}")
        except urllib.error.HTTPError as e:
            if e.code == 429:
                wait_sec = 2 * (attempt + 1)
                time.sleep(wait_sec)
                continue
            body = e.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"HTTP {e.code}: {body}")
        except Exception as e:
            if attempt == 4:
                raise e
            time.sleep(1)

    return {"choice": "error", "confidence": 0, "probabilities": {}}

def generate_html(course_title, forum_title, model_name, results, output_file):
    counts = {"acceptable": 0, "toxic": 0, "spam": 0}
    for r in results:
        label = r["choice"]
        counts[label] = counts.get(label, 0) + 1

    rows_html = []
    for r in results:
        choice = r["choice"]
        conf = r["confidence"]
        probs = r["probabilities"]
        prob_str = " | ".join([f"{k}: {v:.2f}" for k, v in probs.items()])
        badge_class = f"badge-{choice}"

        rows_html.append(f"""
        <tr class="item-row {choice}">
            <td class="id-col">{r['id']}</td>
            <td class="meta-col">
                <div class="author">{r['author']}</div>
                <div class="thread">{r['thread']}</div>
                <div class="time">{r.get('posted_at', '')}</div>
            </td>
            <td class="comment-col">{r['comment']}</td>
            <td class="label-col">
                <span class="badge {badge_class}">{choice.upper()}</span>
                <div class="conf">conf: {conf:.2f}</div>
                <div class="probs">{prob_str}</div>
            </td>
        </tr>
        """)

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Clef Moderation Results - {model_name}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background: #f8fafc;
            color: #0f172a;
            margin: 0;
            padding: 24px;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        header {{
            background: #ffffff;
            border-radius: 10px;
            padding: 20px 24px;
            margin-bottom: 20px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}
        h1 {{
            margin: 0 0 6px 0;
            font-size: 22px;
        }}
        .sub {{
            color: #64748b;
            font-size: 14px;
            margin-bottom: 16px;
        }}
        .stats {{
            display: flex;
            gap: 12px;
            flex-wrap: wrap;
        }}
        .stat-pill {{
            padding: 6px 14px;
            border-radius: 9999px;
            font-size: 13px;
            font-weight: 600;
        }}
        .pill-acceptable {{ background: #dcfce7; color: #166534; }}
        .pill-toxic {{ background: #fee2e2; color: #991b1b; }}
        .pill-spam {{ background: #fef3c7; color: #92400e; }}
        .pill-total {{ background: #e2e8f0; color: #334155; }}
        table {{
            width: 100%;
            border-collapse: collapse;
            background: #ffffff;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}
        th {{
            background: #f1f5f9;
            text-align: left;
            padding: 12px 16px;
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: #475569;
        }}
        td {{
            padding: 14px 16px;
            border-top: 1px solid #f1f5f9;
            vertical-align: top;
            font-size: 14px;
        }}
        .id-col {{ width: 40px; font-weight: bold; color: #64748b; text-align: center; }}
        .meta-col {{ width: 170px; }}
        .author {{ font-weight: 600; color: #1e293b; }}
        .thread {{ font-size: 12px; color: #64748b; }}
        .time {{ font-size: 11px; color: #94a3b8; }}
        .comment-col {{ line-height: 1.5; }}
        .label-col {{ width: 180px; }}
        .badge {{
            display: inline-block;
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 700;
            letter-spacing: 0.04em;
        }}
        .badge-acceptable {{ background: #dcfce7; color: #166534; border: 1px solid #bbf7d0; }}
        .badge-toxic {{ background: #fee2e2; color: #991b1b; border: 1px solid #fecaca; }}
        .badge-spam {{ background: #fef3c7; color: #92400e; border: 1px solid #fde68a; }}
        .conf {{
            margin-top: 6px;
            font-size: 12px;
            color: #64748b;
            font-family: monospace;
        }}
        .probs {{
            font-size: 11px;
            color: #94a3b8;
            font-family: monospace;
            margin-top: 2px;
        }}
        tr:hover td {{
            background: #f8fafc;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>{course_title} - Forum Moderation</h1>
            <div class="sub">{forum_title} | Model: <strong>{model_name}</strong> | Total comments: {len(results)}</div>
            <div class="stats">
                <span class="stat-pill pill-total">Total: {len(results)}</span>
                <span class="stat-pill pill-acceptable">Acceptable: {counts.get('acceptable', 0)}</span>
                <span class="stat-pill pill-toxic">Toxic: {counts.get('toxic', 0)}</span>
                <span class="stat-pill pill-spam">Spam: {counts.get('spam', 0)}</span>
            </div>
        </header>

        <table>
            <thead>
                <tr>
                    <th>#</th>
                    <th>Context</th>
                    <th>Comment</th>
                    <th>Classification</th>
                </tr>
            </thead>
            <tbody>
                {''.join(rows_html)}
            </tbody>
        </table>
    </div>
</body>
</html>"""

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_content)

def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else "comments.json"
    model_name = sys.argv[2] if len(sys.argv) > 2 else "clef-flash"
    output_html = sys.argv[3] if len(sys.argv) > 3 else "results.html"

    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, input_file)
    creds_path = os.path.join(script_dir, "cloud-flare.local.sh")
    output_path = os.path.join(script_dir, output_html)

    account, token = load_credentials(creds_path)

    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    course = data.get("course", "Course")
    forum = data.get("forum", "Forum")
    comments = data.get("comments", [])

    print(f"Loaded {len(comments)} comments from {input_file}")
    print(f"Running classification using model: {model_name}")

    results = []
    for idx, c in enumerate(comments, start=1):
        c_id = c.get("id", idx)
        text = c.get("comment", "")
        res = classify_comment(account, token, model_name, text)
        r_entry = {**c, **res}
        results.append(r_entry)
        print(f"[{idx}/{len(comments)}] ID {c_id}: {res['choice']} (conf: {res['confidence']:.2f})")

    generate_html(course, forum, model_name, results, output_path)
    print(f"Successfully generated {output_html}")

if __name__ == "__main__":
    main()
