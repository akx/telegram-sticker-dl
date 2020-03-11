Telegram sticker downloaderator
===============================

Usage
-----

1. You'll need a valid Telegram bot token in the `TELEGRAM_TOKEN` envvar.
2. Run `sticker_gatherer_bot.py` and send the bot some stickers.
3. Run `get_sticker_sets.py`
4. Run `expand_set_fileids.py > emoji2.jsonl`
5. Run `download_to_cache.py`
6. Run `transcode_cache.py`

You'll end up with PNG stickers in `stickers/`.

You can freely rerun steps 2 to 6 again without having to download stickers you already have.

Caveats
-------

Animated stickers (the TGS format) are not yet supported.
