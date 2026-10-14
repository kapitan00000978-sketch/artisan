"""
Elena Rostova's Autonomous UI/UX Elevation Engine
Transforms amateur, unpolished mockups into world-class, award-winning Liquid Glass masterworks.
"""

import os
import re
from typing import Dict, Any, List


class ElenaElevationEngine:
    """Elena Rostova's UI/UX Elevation Engine."""

    DESIGN_SYSTEM_INJECTION = """
    <!-- 🎨 Elena Rostova Signature Liquid Glass & Typography Design System -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@500;700;800;900&display=swap" rel="stylesheet">
    <style id="elena-design-system-elevation">
        :root {
            --elena-bg: #090b10;
            --elena-surface-glass: rgba(255, 255, 255, 0.04);
            --elena-border-specular: rgba(255, 255, 255, 0.12);
            --elena-border-glow: rgba(0, 240, 255, 0.4);
            --elena-accent: #00f0ff;
            --elena-accent-grad: linear-gradient(135deg, #00f0ff 0%, #7000ff 100%);
            --elena-text-title: #ffffff;
            --elena-text-body: #94a3b8;
            --elena-radius-lg: 16px;
            --elena-radius-full: 9999px;
            --elena-transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        }

        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
            background-color: var(--elena-bg) !important;
            color: var(--elena-text-title) !important;
            background-image: 
                radial-gradient(circle at 15% 20%, rgba(0, 240, 255, 0.08) 0%, transparent 40%),
                radial-gradient(circle at 85% 80%, rgba(112, 0, 255, 0.08) 0%, transparent 40%) !important;
            background-attachment: fixed !important;
            line-height: 1.6 !important;
            margin: 0 !important;
            padding: 32px 16px !important;
        }

        h1, h2, h3, .heading-display {
            font-family: 'Outfit', sans-serif !important;
            letter-spacing: -0.025em !important;
            color: #ffffff !important;
            line-height: 1.15 !important;
        }

        h1 {
            font-size: clamp(32px, 5vw, 56px) !important;
            font-weight: 800 !important;
            margin-bottom: 24px !important;
        }

        h2 {
            font-size: clamp(24px, 3.5vw, 40px) !important;
            margin-bottom: 16px !important;
        }

        p, .body-copy {
            color: var(--elena-text-body) !important;
            font-size: 16px !important;
            line-height: 1.6 !important;
            max-width: 64ch !important;
            margin-bottom: 24px !important;
        }

        /* 8pt Harmonized Liquid Glass Containers */
        .card, .container, .box, section, article {
            background: var(--elena-surface-glass) !important;
            backdrop-filter: blur(16px) !important;
            -webkit-backdrop-filter: blur(16px) !important;
            border: 1px solid var(--elena-border-specular) !important;
            border-radius: var(--elena-radius-lg) !important;
            padding: 32px !important;
            margin-bottom: 32px !important;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.4) !important;
            transition: var(--elena-transition) !important;
        }

        .card:hover, .container:hover {
            border-color: var(--elena-border-glow) !important;
            box-shadow: 0 16px 40px 0 rgba(0, 240, 255, 0.15) !important;
            transform: translateY(-2px) !important;
        }

        /* 60fps Magnetic Interactive Buttons */
        button, .btn, a.btn, input[type="submit"] {
            display: inline-flex !important;
            align-items: center !important;
            justify-content: center !important;
            background: var(--elena-accent-grad) !important;
            color: #000000 !important;
            font-family: 'Inter', sans-serif !important;
            font-weight: 700 !important;
            font-size: 16px !important;
            border: none !important;
            border-radius: var(--elena-radius-full) !important;
            padding: 16px 32px !important;
            cursor: pointer !important;
            letter-spacing: 0.01em !important;
            box-shadow: 0 0 24px rgba(0, 240, 255, 0.35) !important;
            transition: var(--elena-transition) !important;
            text-decoration: none !important;
        }

        button:hover, .btn:hover, a.btn:hover {
            box-shadow: 0 0 40px rgba(0, 240, 255, 0.75) !important;
            transform: scale(1.03) translateY(-1px) !important;
        }

        button:active, .btn:active {
            transform: scale(0.98) !important;
        }
    </style>
    """

    def elevate(self, html_path: str) -> str:
        """Applies Elena's signature design elevation to the target file."""
        with open(html_path, "r", encoding="utf-8") as f:
            content = f.read()

        elevated = content

        # 1. Ensure responsive viewport exists
        if '<meta name="viewport"' not in elevated.lower():
            viewport = '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
            if "<head>" in elevated:
                elevated = elevated.replace("<head>", f"<head>\n    {viewport}")
            else:
                elevated = viewport + "\n" + elevated

        # 2. Inject Design System Styles
        if "</head>" in elevated:
            if "elena-design-system-elevation" not in elevated:
                elevated = elevated.replace("</head>", f"{self.DESIGN_SYSTEM_INJECTION}\n</head>")
        else:
            elevated = self.DESIGN_SYSTEM_INJECTION + "\n" + elevated

        # 3. Clean up generic HTML cliches in UI copy
        elevated = re.sub(r"(?i)(>|\b)Welcome to\s+", r"\1Experience ", elevated)
        elevated = re.sub(r"(?i)>Click here<", ">Launch Experience<", elevated)
        elevated = re.sub(r"(?i)>Learn more<", ">Explore Architecture<", elevated)

        with open(html_path, "w", encoding="utf-8") as f:
            f.write(elevated)

        return elevated
