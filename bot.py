import logging
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    filters,
    ContextTypes,
)

from config import BOT_TOKEN
from receipt_generator import generar_comprobante

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# Estados
NOMBRE, MONTO = range(2)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "👋 ¡Hola! Soy el generador de comprobantes Nequi.\n\n"
        "Usa /nuevo para crear un comprobante."
    )


async def nuevo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data.clear()
    await update.message.reply_text(
        "👤 ¿Cuál es el *nombre* del remitente?",
        parse_mode="Markdown",
        reply_markup=ReplyKeyboardRemove(),
    )
    return NOMBRE


async def recibir_nombre(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["nombre"] = update.message.text.strip()
    await update.message.reply_text(
        "💵 ¿Cuál es el *monto* enviado?\n_(solo el número, ej: 100000)_",
        parse_mode="Markdown",
    )
    return MONTO


async def recibir_monto(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    texto = update.message.text.strip().replace(",", ".").replace(" ", "")
    try:
        float(texto)
    except ValueError:
        await update.message.reply_text(
            "⚠️ Ingresa solo el número, sin símbolos. Ej: *100000*",
            parse_mode="Markdown",
        )
        return MONTO

    nombre = context.user_data["nombre"]
    await update.message.reply_text("⏳ Generando comprobante...")

    imagen = generar_comprobante(nombre=nombre, monto=texto)
    await update.message.reply_photo(
        photo=imagen,
        caption="✅ Comprobante generado.",
    )
    return ConversationHandler.END


async def cancelar(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("❌ Cancelado.", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def main() -> None:
    app = Application.builder().token(BOT_TOKEN).build()

    conv = ConversationHandler(
        entry_points=[CommandHandler("nuevo", nuevo)],
        states={
            NOMBRE: [MessageHandler(filters.TEXT & ~filters.COMMAND, recibir_nombre)],
            MONTO:  [MessageHandler(filters.TEXT & ~filters.COMMAND, recibir_monto)],
        },
        fallbacks=[CommandHandler("cancelar", cancelar)],
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(conv)

    logger.info("Bot corriendo...")
    app.run_polling()


if __name__ == "__main__":
    main()
