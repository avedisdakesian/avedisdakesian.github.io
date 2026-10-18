"""Turns the full-size Framer images in framer-export/assets into web-sized WebP files in assets/img.

Each image is scaled to twice the width it is shown at (sharp on retina screens), never upscaled.
Run from the repo root: python3 scripts/optimize-images.py
"""
from pathlib import Path
from PIL import Image

SRC = Path("framer-export/assets")
OUT = Path("assets/img")

# name in assets/img: (Framer file, widest display width in CSS pixels)
IMAGES = {
    # Home
    "second-caller-cover": ("ccs3H6Pq1LqVw7E8YJzMJrdBK4.png", 1140),
    # Second Caller
    "sc-overview-bg": ("FN48rXdsgPQKNH0g9gKcndsDbNM.jpg", 590),
    "sc-overview-comments": ("Jndy0B0Tv8eOlFyaNfPkRlVBvRU.png", 531),
    "sc-goals-bg": ("hd0cUqVkLLv9f3tsv3UGlEQrQwU.jpg", 590),
    "sc-goals": ("153jkhf7W5w1ddr7YG8172IhM1k.png", 697),
    "sc-purple-bg": ("WOyfsXcx73XyoA2cKK6FKN7g.jpg", 1108),
    "sc-os-share": ("pN7ygfvGKeAZ65X7U2b6C7qSkvc.png", 717),
    "sc-competitors-bg": ("HuN9PDVBlQ3PZWME5HkYKK01ZGU.jpg", 1108),
    "sc-competitors": ("q6R2FHYdUOOeeHGJkGkYOaCWRk.png", 717),
    "sc-spider-chart": ("ka7KDLqK5h0ZJ05zHerZbBclvU.png", 379),
    "sc-heuristics": ("8KIOUJhRqUtRf42KBpmNSzLgHY.png", 590),
    "sc-understanding": ("rjJNWhTo8Rb5yP6di9J2KFwLPvM.png", 590),
    "sc-affinity": ("biFSL2fIfjEJeCdrQA0uaNLF0.png", 590),
    "sc-persona-bg": ("3FunmJSJRdm9EWpVPTFJGc9qvCU.jpg", 1108),
    "sc-persona": ("VJrBz5Mjys3aBvSkK0oJJWSXqDM.png", 717),
    "sc-ideation": ("rE9VPFcfcMoTGkBSwf6RRirA.png", 590),
    "sc-wireframes-bg": ("Uzu4wmnlDrpWAjBVtb3iXwOT8.png", 1108),
    "sc-sketch-1": ("TvFjPUdulhD0q1MbAPnO9dGaHw.png", 327),
    "sc-sketch-2": ("NWqEeLBiV3q3JMJQaNQPTLI0AHE.png", 204),
    "sc-sketch-3": ("FEQNLmLoDD5Uxbd6NKp9PKG2vVk.png", 449),
    "sc-sketch-4": ("zXS6rrzxkvYc0jHF85DW0MEefw.png", 385),
    "sc-lofi-1": ("brpdFpNssA4PAowTE4YnCfClnd8.png", 1108),
    "sc-lofi-2": ("XIBWZChuurbXG4N1izzYunTSXeQ.png", 1108),
    # Woods Center
    "wc-roadmap": ("TNPKOVhMYtxR2NnIK8F6dwwnio.png", 1108),
    "wc-swot": ("r9kvGAccPWw95AgiQbWUO5eSTQ.png", 1108),
    "wc-swot-mobile": ("ivlzT2IAOVo9ZCSvrMaDZ9MydM.png", 400),
    "wc-architecture": ("3Bk7fahEzfsadLKmqUtJHHGchg.png", 1061),
    "wc-persona-1": ("TVcDMifTnWgZM6lfuKhnoYBFAFY.png", 549),
    "wc-persona-2": ("PRgc40o3gsaR0lSdFnUFsv7SWQ.png", 549),
    "wc-components-1": ("s3wOI15z1YgfXNOszKysGCki1gc.png", 498),
    "wc-components-2": ("sPj0fliQx5P4f7VkiBECAlZ6iq0.png", 498),
    "wc-components-3": ("XFxpIf2pTs5lt2HUoN8A6l77lLk.png", 498),
    "wc-mobile-1": ("AD8SoJiwT81T8yf9l7pBcA7aGIU.png", 258),
    "wc-mobile-2": ("4lnLzWDixDN2f9jqZoXwwsENc.png", 258),
    "wc-mobile-3": ("qTOWSmCiyKIMH2JwGsUX7LRFF2w.png", 258),
    "wc-typography": ("WC5MRFmtz3DW4UFcnk5tGzd6p7k.png", 1108),
    "wc-colors": ("NGbEKSPLZJUfSRP9PV9OYLlA9mE.png", 1044),
    "wc-components": ("IiRS3eEthP3il3OrV1bKbGQBCsU.png", 1044),
    "wc-orange-bg": ("7k6ynb3BYhQX3yOMD3oNtiype8.jpg", 1071),
    "wc-ui-desktop-1": ("eWfzFuNKTv2RqxF0sbxWIR0S3Cc.png", 625),
    "wc-ui-desktop-2": ("0ZC5JdAnh7gCQZ3ACBBACwJ7CnQ.png", 693),
    "wc-ui-desktop-3": ("dRjDCcNKZQGCslukp3UB6q4cC8.png", 354),
    "wc-ui-mobile-1": ("lEQTZ7jmhJiCn87dZatikxouVOo.png", 304),
    "wc-ui-mobile-2": ("0v7tOFrG1mWEDdvI5yoHvXRKTo.png", 328),
    "wc-ui-mobile-3": ("QrSdcqh6G7nFQZtj54TOhrnWwsc.png", 294),
}

OUT.mkdir(parents=True, exist_ok=True)
for name, (src, display_width) in IMAGES.items():
    im = Image.open(SRC / src)
    im = im.convert("RGBA" if im.mode in ("P", "RGBA", "LA") else "RGB")
    target = min(im.width, display_width * 2)
    if target < im.width:
        im = im.resize((target, round(im.height * target / im.width)), Image.LANCZOS)
    out = OUT / f"{name}.webp"
    im.save(out, "WEBP", quality=82, method=6)
    print(f"{out}  {im.width}x{im.height}  {out.stat().st_size // 1024} KB")
