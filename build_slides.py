#!/usr/bin/env python3
"""Render an Instagram carousel (1080x1350 JPEG) for the ecomrs brand.

Usage:
    python3 build_slides.py content.json out_dir

content.json schema:
{
  "handle": "@ecom__rs",               # footer left label (бренд-хендл, НЕ особисте імʼя)
  "footer_email": "",                   # лишай порожнім — НЕ писати особистий email на слайдах
  "slides": [
     # kind "cover":
     {"kind":"cover","label":"KLAVIYO · EMAIL · RETENTION",
      "title":"Перетворюю email у [[канал]] продажів.",   # [[..]] = amber
      "kicker":"Один рядок підзаголовка."},
     # kind "list":
     {"kind":"list","label":"ЩО Я РОБЛЮ  /  01",
      "title":"Заголовок із [[акцентом]].",
      "items":[{"ix":"01","tx":"Пункт","small":"дрібний опис"}, ...]},  # ix може бути "→"
     # kind "cta":
     {"kind":"cta","label":"ДАВАЙТЕ ПРАЦЮВАТИ  /  03",
      "title":"Заголовок [[CTA]].",
      "kicker":"Рядок пояснення.",
      "cta":["→ Пишіть у Direct","↳ деталі — в шапці профілю"]}
  ]
}
Footer page numbers (NN — total) are added automatically.
"""
import sys, json, base64, os, html, re
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
FONTDIR = os.path.join(HERE, "fonts")

# ECOMRS brand palette (ТІЛЬКИ бренд-кольори):
# фон графіт/чорний, акцент — зелений смарагд (носій уваги), золото — лише тонкі лінії/дрібні деталі.
INK="#0c0c0c"; INK2="#161616"; PAPER="#ececea"; MUTE="#8a8f88"
AMBER="#10a060"   # зелений смарагд — головний акцент (виділені слова, цифри, стрілки)
GOLD="#c8a24c"    # золото — лише тонкі канти/лінії
LINE="rgba(200,162,76,0.22)"

def b64(name):
    with open(os.path.join(FONTDIR, name), "rb") as f:
        return base64.b64encode(f.read()).decode()

FONT_FILES = [
    ("IBMPlexSerif-Regular.ttf","PlexSerif",400,"normal"),
    ("IBMPlexSerif-Bold.ttf","PlexSerif",700,"normal"),
    ("IBMPlexSerif-Italic.ttf","PlexSerif",400,"italic"),
    ("IBMPlexSerif-BoldItalic.ttf","PlexSerif",700,"italic"),
    ("IBMPlexMono-Regular.ttf","PlexMono",400,"normal"),
    ("IBMPlexMono-Bold.ttf","PlexMono",700,"normal"),
]

def face_css():
    css=""
    for fn,fam,wt,st in FONT_FILES:
        css+=(f"@font-face{{font-family:'{fam}';font-weight:{wt};font-style:{st};"
              f"src:url('data:font/ttf;base64,{b64(fn)}') format('truetype');}}\n")
    return css

def amber(text):
    # escape, then turn [[..]] into amber spans
    out=[]; i=0
    for m in re.finditer(r"\[\[(.+?)\]\]", text):
        out.append(html.escape(text[i:m.start()]))
        out.append(f"<span class='amber'>{html.escape(m.group(1))}</span>")
        i=m.end()
    out.append(html.escape(text[i:]))
    return "".join(out).replace("\n","<br>")

def base_css():
    return f"""<style>
{face_css()}
*{{margin:0;padding:0;box-sizing:border-box;}}
html,body{{width:1080px;height:1350px;}}
.slide{{width:1080px;height:1350px;position:relative;overflow:hidden;
  background:radial-gradient(130% 90% at 100% 0%, {INK2} 0%, {INK} 55%),{INK};
  color:{PAPER};padding:96px 92px;display:flex;flex-direction:column;}}
.grain{{position:absolute;inset:0;opacity:0.035;pointer-events:none;
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='120' height='120'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='2'/%3E%3C/filter%3E%3Crect width='120' height='120' filter='url(%23n)'/%3E%3C/svg%3E");}}
.toplabel{{font-family:'PlexMono';font-weight:400;font-size:21px;letter-spacing:0.42em;
  color:{MUTE};text-transform:uppercase;display:flex;align-items:center;gap:20px;}}
.toplabel .dot{{width:11px;height:11px;border-radius:50%;background:{AMBER};
  box-shadow:0 0 0 6px rgba(16,160,96,0.14);display:inline-block;flex:0 0 auto;}}
.rule{{height:1px;background:{LINE};width:100%;}}
.mid{{flex:1;display:flex;flex-direction:column;justify-content:center;}}
.h1{{font-family:'PlexSerif';font-weight:700;color:{PAPER};letter-spacing:-0.015em;}}
.amber{{color:{AMBER};}}
.foot{{display:flex;justify-content:space-between;align-items:flex-end;
  font-family:'PlexMono';font-size:22px;letter-spacing:0.08em;color:{MUTE};}}
.foot b{{color:{PAPER};font-weight:400;}}
.led{{display:flex;flex-direction:column;gap:30px;margin-top:8px;}}
.row{{display:flex;align-items:baseline;gap:30px;}}
.row .ix{{font-family:'PlexMono';font-size:24px;color:{AMBER};letter-spacing:0.05em;flex:0 0 64px;}}
.row .tx{{font-family:'PlexSerif';font-weight:400;font-size:46px;color:{PAPER};line-height:1.18;letter-spacing:-0.01em;}}
.row .tx small{{display:block;font-family:'PlexMono';font-size:20px;color:{MUTE};letter-spacing:0.04em;margin-top:7px;}}
.kick{{font-family:'PlexSerif';font-style:italic;font-weight:400;font-size:40px;color:{MUTE};line-height:1.3;}}
.ctalines{{margin-top:60px;font-family:'PlexMono';font-size:30px;letter-spacing:0.04em;line-height:1.6;}}
.ctalines .muted{{color:{MUTE};}}
</style>"""

def slide_html(inner):
    return (f"<!doctype html><html><head><meta charset='utf-8'>{base_css()}</head>"
            f"<body><div class='slide'><div class='grain'></div>{inner}</div></body></html>")

def render_cover(s):
    kicker=f"<div class='kick' style='margin-top:46px;max-width:720px;'>{amber(s.get('kicker',''))}</div>" if s.get('kicker') else ""
    return f"""
  <div class='toplabel'><span class='dot'></span>{html.escape(s.get('label',''))}</div>
  <div class='mid'>
    <div class='h1' style="font-size:108px;line-height:1.03;">{amber(s['title'])}</div>
    {kicker}
  </div>"""

def render_list(s):
    rows=""
    for it in s.get('items',[]):
        small=f"<small>{html.escape(it['small'])}</small>" if it.get('small') else ""
        rows+=f"<div class='row'><div class='ix'>{html.escape(str(it.get('ix','→')))}</div><div class='tx'>{amber(it['tx'])}{small}</div></div>"
    return f"""
  <div class='toplabel'><span class='dot'></span>{html.escape(s.get('label',''))}</div>
  <div class='mid'>
    <div class='h1' style="font-size:70px;line-height:1.06;margin-bottom:54px;max-width:880px;">{amber(s['title'])}</div>
    <div class='led'>{rows}</div>
  </div>"""

def render_cta(s):
    kicker=f"<div class='kick' style=\"margin-top:40px;max-width:760px;font-style:normal;font-family:'PlexSerif';color:{PAPER};font-size:48px;line-height:1.25;\">{amber(s.get('kicker',''))}</div>" if s.get('kicker') else ""
    cta=""
    if s.get('cta'):
        lines=[]
        for i,l in enumerate(s['cta']):
            cls="" if i==0 else " class='muted'"
            lines.append(f"<span{cls}>{amber(l)}</span>")
        cta=f"<div class='ctalines'>{'<br>'.join(lines)}</div>"
    return f"""
  <div class='toplabel'><span class='dot'></span>{html.escape(s.get('label',''))}</div>
  <div class='mid'>
    <div class='h1' style="font-size:86px;line-height:1.04;">{amber(s['title'])}</div>
    {kicker}{cta}
  </div>"""

RENDER={"cover":render_cover,"list":render_list,"cta":render_cta}

def footer(handle, email, n, total, last):
    left = f"<b>{html.escape(email)}</b>" if (last and email) else f"<b>{html.escape(handle)}</b>"
    return (f"<div class='rule' style='margin-bottom:34px;'></div>"
            f"<div class='foot'><span>{left}</span><span>{n:02d} — {total:02d}</span></div>")

def main():
    content=json.load(open(sys.argv[1], encoding="utf-8"))
    out=sys.argv[2] if len(sys.argv)>2 else "out"
    os.makedirs(out, exist_ok=True)
    slides=content["slides"]; total=len(slides)
    handle=content.get("handle","@ecom__rs"); email=content.get("footer_email","")
    pages=[]
    for i,s in enumerate(slides):
        inner=RENDER[s["kind"]](s)
        inner+=footer(handle,email,i+1,total,last=(i==total-1))
        pages.append(slide_html(inner))
    with sync_playwright() as p:
        b=p.chromium.launch()
        pg=b.new_page(viewport={"width":1080,"height":1350}, device_scale_factor=2)
        for i,htmlpage in enumerate(pages):
            pg.set_content(htmlpage, wait_until="networkidle"); pg.wait_for_timeout(250)
            path=os.path.join(out, f"slide{i+1}.png")
            pg.screenshot(path=path, clip={"x":0,"y":0,"width":1080,"height":1350})
        b.close()
    # downscale + jpeg for hosting
    from PIL import Image
    for i in range(total):
        im=Image.open(os.path.join(out,f"slide{i+1}.png")).convert("RGB").resize((1080,1350), Image.LANCZOS)
        im.save(os.path.join(out,f"slide{i+1}.jpg"),"JPEG",quality=84,optimize=True,progressive=True)
    print(f"Rendered {total} slides to {out}")

if __name__=="__main__":
    main()
