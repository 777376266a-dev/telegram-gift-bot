import asyncio
from telethon import TelegramClient
from telethon.tl.functions.payments import GetResaleStarGiftsRequest
from aiogram import Bot

# --- ВАШИ ДАННЫЕ УЖЕ ВСТАВЛЕНЫ ---
API_ID = 30514856
API_HASH = '578602f0ca28809ee9e1a0a359812328'
BOT_TOKEN = '8848261748:AAFYKRloLmVESyJJ6o7AE_A0d6mL6Gw0SoA'
MY_CHAT_ID = 7939582075

# Максимальная цена в Telegram Stars, которую считаем выгодной (можете изменить позже)
MAX_PRICE_STARS = 500 

client = TelegramClient('gift_session', API_ID, API_HASH)
bot = Bot(token=BOT_TOKEN)
seen_gifts = set()

async def monitor_gifts():
    print("🚀 Монитор подарков запущен...")
    await bot.send_message(MY_CHAT_ID, "✅ Мониторинг Telegram-подарков запущен!")
    
    while True:
        try:
            resale_gifts = await client(GetResaleStarGiftsRequest(
                offset='',
                limit=20
            ))
            
            for gift in resale_gifts.gifts:
                gift_id = getattr(gift, 'id', str(gift))
                
                if gift_id not in seen_gifts:
                    seen_gifts.add(gift_id)
                    
                    if gift.stars <= MAX_PRICE_STARS:
                        buy_link = f"https://t.me/gift/{gift.slug}" if hasattr(gift, 'slug') else "https://t.me/nft"
                        
                        message_text = (
                            f"🚨 **НАЙДЕН ВЫГОДНЫЙ ПОДАРOК!**\n\n"
                            f"⭐ **Цена:** {gift.stars} Stars\n"
                            f"🔗 [Нажмите сюда, чтобы купить]({buy_link})"
                        )
                        
                        await bot.send_message(
                            MY_CHAT_ID, 
                            message_text, 
                            parse_mode="Markdown",
                            disable_web_page_preview=False
                        )
                        
        except Exception as e:
            print(f"⚠️ Ошибка/пауза: {e}")
            
        await asyncio.sleep(3) # Пауза 3 сек (защита от банов без прокси)

async def main():
    await client.start()
    await monitor_gifts()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
