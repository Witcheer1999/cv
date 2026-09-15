import re
import markdown

CSS_TEMPLATE = """<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="UTF-8">
  <title>Michael Bagnoli - Curriculum Vitae ({lang_upper})</title>
  <style>
    @page {
      size: A4;
      margin: 16mm 16mm 16mm 16mm;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      color: #0f172a;
      background-color: #ffffff;
      line-height: 1.5;
      font-size: 9.5pt;
      -webkit-font-smoothing: antialiased;
    }

    .cv-container {
      max-width: 100%;
      margin: 0 auto;
    }

    header {
      border-bottom: 2.5px solid #0f172a;
      padding-bottom: 12px;
      margin-bottom: 16px;
    }

    h1 {
      font-size: 24pt;
      font-weight: 800;
      letter-spacing: -0.5px;
      color: #0f172a;
      text-transform: uppercase;
      margin-bottom: 3px;
    }

    .headline {
      font-size: 11pt;
      font-weight: 600;
      color: #1e3a8a;
      margin-bottom: 8px;
    }

    .contact-bar {
      font-size: 8.5pt;
      color: #475569;
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      align-items: center;
    }

    .contact-bar a {
      color: #0284c7;
      text-decoration: none;
      font-weight: 500;
    }

    section {
      margin-bottom: 18px;
    }

    h2 {
      font-size: 12pt;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.8px;
      color: #0f172a;
      border-bottom: 1.5px solid #cbd5e1;
      padding-bottom: 4px;
      margin-top: 18px;
      margin-bottom: 12px;
      page-break-after: avoid;
    }

    h3 {
      font-size: 10.5pt;
      font-weight: 700;
      color: #0f172a;
      margin-top: 12px;
      margin-bottom: 4px;
      page-break-after: avoid;
    }

    h4 {
      font-size: 9.6pt;
      font-weight: 700;
      color: #1e3a8a;
      margin-top: 8px;
      margin-bottom: 3px;
      page-break-after: avoid;
    }

    p {
      font-size: 9pt;
      color: #334155;
      margin-bottom: 6px;
      text-align: justify;
      line-height: 1.5;
    }

    p strong {
      color: #0f172a;
    }

    em {
      color: #475569;
    }

    ul {
      list-style-type: disc;
      padding-left: 18px;
      margin-bottom: 8px;
    }

    li {
      font-size: 9pt;
      color: #334155;
      margin-bottom: 4px;
      line-height: 1.45;
      text-align: justify;
    }

    li strong {
      color: #0f172a;
    }

    hr {
      border: none;
      border-top: 1px solid #e2e8f0;
      margin: 14px 0;
    }

    code {
      display: inline-block;
      background: #f1f5f9;
      color: #1e293b;
      border: 1px solid #cbd5e1;
      padding: 1px 5px;
      border-radius: 3px;
      margin: 1px 1px;
      font-size: 8pt;
      font-family: inherit;
      font-weight: 500;
    }

    .job-block {
      margin-bottom: 16px;
      page-break-inside: avoid;
    }

    .matrix-category {
      margin-bottom: 12px;
      page-break-inside: avoid;
    }

    @media print {
      body {
        font-size: 9pt;
      }
      .cv-container {
        width: 100%;
      }
      a {
        text-decoration: none;
        color: #0284c7 !important;
      }
      .job-block {
        page-break-inside: avoid;
      }
      .matrix-category {
        page-break-inside: avoid;
      }
      h2, h3, h4 {
        page-break-after: avoid;
      }
    }
  </style>
</head>
<body>
  <div class="cv-container">
    {content}
  </div>
</body>
</html>
"""

COMPACT_CSS_TEMPLATE = """<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="UTF-8">
  <title>Michael Bagnoli - Curriculum Vitae ({lang_upper} Compact)</title>
  <style>
    @page {
      size: A4;
      margin: 12mm 14mm 12mm 14mm;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      color: #0f172a;
      background-color: #ffffff;
      line-height: 1.38;
      font-size: 8.8pt;
      -webkit-font-smoothing: antialiased;
    }

    .cv-container {
      max-width: 100%;
      margin: 0 auto;
    }

    header {
      border-bottom: 2px solid #0f172a;
      padding-bottom: 8px;
      margin-bottom: 10px;
    }

    h1 {
      font-size: 20pt;
      font-weight: 800;
      letter-spacing: -0.4px;
      color: #0f172a;
      text-transform: uppercase;
      margin-bottom: 2px;
    }

    .headline {
      font-size: 9.8pt;
      font-weight: 600;
      color: #1e3a8a;
      margin-bottom: 4px;
    }

    .contact-bar {
      font-size: 8pt;
      color: #475569;
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      align-items: center;
    }

    .contact-bar a {
      color: #0284c7;
      text-decoration: none;
      font-weight: 500;
    }

    h2 {
      font-size: 10.5pt;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.6px;
      color: #0f172a;
      border-bottom: 1.5px solid #cbd5e1;
      padding-bottom: 2px;
      margin-top: 10px;
      margin-bottom: 6px;
      page-break-after: avoid;
    }

    h3 {
      font-size: 9.5pt;
      font-weight: 700;
      color: #0f172a;
      margin-top: 8px;
      margin-bottom: 2px;
      page-break-after: avoid;
    }

    p {
      font-size: 8.6pt;
      color: #334155;
      margin-bottom: 4px;
      text-align: justify;
      line-height: 1.38;
    }

    p strong {
      color: #0f172a;
    }

    em {
      color: #475569;
    }

    ul {
      list-style-type: disc;
      padding-left: 16px;
      margin-bottom: 5px;
    }

    li {
      font-size: 8.6pt;
      color: #334155;
      margin-bottom: 2.5px;
      line-height: 1.36;
      text-align: justify;
    }

    li strong {
      color: #0f172a;
    }

    hr {
      border: none;
      border-top: 1px solid #cbd5e1;
      margin: 8px 0;
    }

    code {
      display: inline-block;
      background: #f1f5f9;
      color: #1e293b;
      border: 1px solid #cbd5e1;
      padding: 0.5px 4px;
      border-radius: 3px;
      margin: 0.5px;
      font-size: 7.6pt;
      font-family: inherit;
      font-weight: 500;
    }

    .job-block {
      margin-bottom: 7px;
      page-break-inside: avoid;
    }

    @media print {
      body {
        font-size: 8.6pt;
      }
      .cv-container {
        width: 100%;
      }
      a {
        text-decoration: none;
        color: #0284c7 !important;
      }
      .job-block {
        page-break-inside: avoid;
      }
      h2, h3 {
        page-break-after: avoid;
      }
    }
  </style>
</head>
<body>
  <div class="cv-container">
    {content}
  </div>
</body>
</html>
"""

def convert_md_to_html(md_path, html_path, lang="it", compact=False):
    with open(md_path, "r", encoding="utf-8") as f:
        md_text = f.read()

    # Convert markdown to html using python-markdown with tables and attr_list extensions
    raw_html = markdown.markdown(md_text, extensions=["extra", "sane_lists"])

    # Enhance job blocks to have page-break-inside: avoid wrappers
    parts = re.split(r'(<h3>.*?</h3>)', raw_html)
    processed_parts = []
    
    in_block = False
    for part in parts:
        if part.startswith("<h3>"):
            if in_block:
                processed_parts.append("</div>\n")
            processed_parts.append('<div class="job-block">\n' + part)
            in_block = True
        elif part.startswith("<h2>"):
            if in_block:
                processed_parts.append("</div>\n")
                in_block = False
            processed_parts.append(part)
        else:
            processed_parts.append(part)
            
    if in_block:
        processed_parts.append("</div>\n")

    final_content = "".join(processed_parts)

    template = COMPACT_CSS_TEMPLATE if compact else CSS_TEMPLATE
    full_html = template.replace("{lang}", lang).replace("{lang_upper}", lang.upper()).replace("{content}", final_content)

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(full_html)
    print(f"Generated {html_path}")

if __name__ == "__main__":
    # Full versions
    convert_md_to_html("cv_it.md", "cv_it.html", lang="it", compact=False)
    convert_md_to_html("cv_en.md", "cv_en.html", lang="en", compact=False)
    # Compact versions
    convert_md_to_html("cv_it_compact.md", "cv_it_compact.html", lang="it", compact=True)
    convert_md_to_html("cv_en_compact.md", "cv_en_compact.html", lang="en", compact=True)
