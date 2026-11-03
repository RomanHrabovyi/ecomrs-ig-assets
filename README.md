# ecomrs-ig-assets

Публічний хостинг зображень + будівник каруселей для щоденних Instagram-постів бренду **@ecom__rs** (Klaviyo / email / retention для Shopify та e-commerce).

Публічні raw-URL використовуються як медіа-джерело для Telegram-доставки та для Metricool (→ Instagram).

## Будівник слайдів

```
python3 build_slides.py content.json out_dir
```

- Рендерить 1080×1350 JPEG **тільки в брендових кольорах ECOMRS**: графіт/чорне тло (#0C0C0C), зелений смарагдовий акцент (#10A060, носій уваги), золото (#C8A24C) — лише тонкі лінії/дрібні деталі; текст сріблясто-білий (#ECECEA). IBM Plex Serif/Mono.
- **НЕ писати на слайдах особисте імʼя чи email Романа.** У футері — лише бренд-хендл `@ecom__rs` (handle у `content.json`, `footer_email` лишати порожнім).
- Шрифти — у `fonts/` (самодостатньо, не залежить від середовища).
- Схема `content.json` і типи слайдів (`cover`, `list`, `cta`) описані у шапці `build_slides.py`.
- `[[текст]]` у заголовку → бурштиновий акцент.

## Щоденна процедура (12:00 за Варшавою)

1. Прочитати `topics-log.md`, вибрати **нову** тему (не з логу).
2. Написати українською: caption + тексти 3–4 слайдів (cover → 1–2 list → cta) у `content.json`.
3. `python3 build_slides.py content.json out` → `out/slide*.jpg`.
4. Запушити слайди у папку за датою: `YYYY-MM-DD/slideN.jpg`.
5. Raw-URL: `https://raw.githubusercontent.com/RomanHrabovyi/ecomrs-ig-assets/main/YYYY-MM-DD/slideN.jpg`.
6. Надіслати в Telegram (бот @ecomrs_posts_bot, chat_id 7392238208): слайди по порядку + caption окремим повідомленням.
7. Дописати тему в `topics-log.md`, запушити.
8. **Не публікувати в Instagram** — тільки доставка на перегляд. Публікація — з підтвердження Романа.

Теми — у ніші: поради/помилки Klaviyo, флоу (welcome, кошик, браузинг, пост-покупка, реактивація), сегментація, deliverability, міфи про email, before/after, міні-кейси, метрики (open/CTR/revenue share).
