import logging
from deep_translator import GoogleTranslator
import pandas as pd
from random_word import RandomWords
from telegram import ForceReply, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
    CallbackQueryHandler,
)
import asyncio
from Telegram_Token import PERSONAL_TOKEN


# Crear un objetos traductor
translatorEsEn = GoogleTranslator(source="es", target="en")
translatorEsDe = GoogleTranslator(source="es", target="de")
translatorEnEs = GoogleTranslator(source="en", target="es")
translatorEnDe = GoogleTranslator(source="en", target="de")
translatorDeEs = GoogleTranslator(source="de", target="es")
translatorDeEn = GoogleTranslator(source="de", target="en")

# Crear objeto para obtener palabras aleatorias
rw = RandomWords()

# Variables globales para las selecciones
origin_lang = ""
destiny_lang = ""
type_translation = ""
ran_word = ""
glosary = """(🇨🇴 Español), (🇺🇸 English), (🇩🇪 Deutsch)\n"""


# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando para iniciar el bot"""

    # Mensaje en Español
    message_es = """
    🚀 Para comenzar a configurar el bot, ingresa los comandos en este orden:

    1️⃣ /changeorigin – Establece el idioma de origen para la traducción.

    2️⃣ /changetype – Define el tipo de traducción para elegir en cuántos idiomas se mostrará la traducción.

    3️⃣ /changedestiny – Establece el destino de la traducción (solo necesario si se usa traducción simultánea).
    """

    # Mensaje en Inglés
    message_en = """
    🚀 To start configuring the bot, enter the commands in this order:

    1️⃣ /changeorigin – Set the source language for the translation.

    2️⃣ /changetype – Set the translation type to choose how many languages the translation will display.

    3️⃣ /changedestiny – Set the destination of the translation (only required if using simultaneous translation).
    """

    # Mensaje en Alemán
    message_de = """
    🚀 Um den Bot zu konfigurieren, geben Sie die Befehle in dieser Reihenfolge ein:

    1️⃣ /changeorigin – Legen Sie die Ausgangssprache für die Übersetzung fest.

    2️⃣ /changetype – Wählen Sie den Übersetzungstyp, um festzulegen, wie viele Sprachen die Übersetzung anzeigen soll.

    3️⃣ /changedestiny – Legen Sie das Ziel der Übersetzung fest (nur erforderlich, wenn die gleichzeitige Übersetzung verwendet wird).
    """

    # Envío de mensajes con intervalos de 0.2 segundos
    await update.message.reply_text(message_es)
    await asyncio.sleep(0.2)
    await update.message.reply_text(message_en)
    await asyncio.sleep(0.2)
    await update.message.reply_text(message_de)


async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando para mostrar el menú de opciones"""

    # Validar configuración
    if await validate_config(update, context):
        return

    # Obtener el mensaje según el idioma
    menu_titles = {
        "es": "🤖 Menú Principal - Selecciona una opción:",
        "en": "🤖 Main Menu - Select an option:",
        "de": "🤖 Hauptmenü - Wählen Sie eine Option:",
    }

    # Definir los textos de los botones según el idioma
    button_texts = {
        "es": {
            "start": "🚀 Iniciar configuración",
            "traductions": "🔄 Traducir",
            "random": "🎲 Palabra aleatoria",
            "glossary": "📚 Ver glosario",
            "viewconfig": "⚙️ Ver configuración",
            "changeorigin": "🔤 Cambiar idioma origen",
            "changetype": "📝 Cambiar tipo traducción",
            "changedestiny": "🎯 Cambiar idioma destino",
        },
        "en": {
            "start": "🚀 Start setup",
            "traductions": "🔄 Translate",
            "random": "🎲 Random word",
            "glossary": "📚 View glossary",
            "viewconfig": "⚙️ View settings",
            "changeorigin": "🔤 Change source language",
            "changetype": "📝 Change translation type",
            "changedestiny": "🎯 Change target language",
        },
        "de": {
            "start": "🚀 Setup starten",
            "traductions": "🔄 Übersetzen",
            "random": "🎲 Zufälliges Wort",
            "glossary": "📚 Glossar anzeigen",
            "viewconfig": "⚙️ Einstellungen anzeigen",
            "changeorigin": "🔤 Ausgangssprache ändern",
            "changetype": "📝 Übersetzungstyp ändern",
            "changedestiny": "🎯 Zielsprache ändern",
        },
    }

    # Crear los botones
    keyboard = [
        [
            InlineKeyboardButton(
                button_texts[origin_lang]["start"], callback_data="menu_start"
            )
        ],
        [
            InlineKeyboardButton(
                button_texts[origin_lang]["traductions"],
                callback_data="menu_traductions",
            )
        ],
        [
            InlineKeyboardButton(
                button_texts[origin_lang]["random"], callback_data="menu_random"
            )
        ],
        [
            InlineKeyboardButton(
                button_texts[origin_lang]["glossary"], callback_data="menu_glossary"
            )
        ],
        [
            InlineKeyboardButton(
                button_texts[origin_lang]["viewconfig"], callback_data="menu_viewconfig"
            )
        ],
        [
            InlineKeyboardButton(
                button_texts[origin_lang]["changeorigin"],
                callback_data="menu_changeorigin",
            )
        ],
        [
            InlineKeyboardButton(
                button_texts[origin_lang]["changetype"], callback_data="menu_changetype"
            )
        ],
        [
            InlineKeyboardButton(
                button_texts[origin_lang]["changedestiny"],
                callback_data="menu_changedestiny",
            )
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(menu_titles[origin_lang], reply_markup=reply_markup)


async def traductions(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando para mostrar las traducciones"""
    await update.message.reply_text("Comando /traductions")


async def random_word(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Genera y traduce una palabra aleatoria según la configuración actual"""

    # Validar configuraci��n
    if await validate_config(update, context):
        return

    # 1. Obtener y guardar palabra aleatoria
    global ran_word
    word = rw.get_random_word().capitalize()
    ran_word = word

    # 2. Obtener el objeto message independientemente del origen
    message = update.message if update.message else update.callback_query.message
    # 3. Definir textos de botones según idioma de origen
    button_texts = {
        "es": {"add": "📝 Agregar al glosario", "new": "🎲 Generar otra palabra"},
        "en": {"add": "📝 Add to glossary", "new": "🎲 Generate another word"},
        "de": {"add": "📝 Zum Glossar hinzufügen", "new": "🎲 Neues Wort generieren"},
    }

    # 4. Crear botones con el texto correspondiente
    keyboard = [
        [
            InlineKeyboardButton(
                button_texts[origin_lang]["add"], callback_data="add_to_glossary"
            ),
            InlineKeyboardButton(
                button_texts[origin_lang]["new"], callback_data="random_word"
            ),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # 5. Procesar traducción según configuración
    if type_translation == "Individual":
        if origin_lang == "es":
            es_word = translatorEnEs.translate(word)
            if destiny_lang == "en":
                await message.reply_text(
                    f"🇨🇴 {es_word}\n🇺🇸 {word}", reply_markup=reply_markup
                )
            else:  # destiny_lang == "de"
                de_word = translatorEnDe.translate(word)
                await message.reply_text(
                    f"🇨🇴 {es_word}\n🇩🇪 {de_word}", reply_markup=reply_markup
                )
        elif origin_lang == "en":
            if destiny_lang == "es":
                es_word = translatorEnEs.translate(word)
                await message.reply_text(
                    f"🇺🇸 {word}\n🇨🇴 {es_word}", reply_markup=reply_markup
                )
            else:  # destiny_lang == "de"
                de_word = translatorEnDe.translate(word)
                await message.reply_text(
                    f"🇺🇸 {word}\n🇩🇪 {de_word}", reply_markup=reply_markup
                )
        else:  # origin_lang == "de"
            de_word = translatorEnDe.translate(word)
            if destiny_lang == "es":
                es_word = translatorEnEs.translate(word)
                await message.reply_text(
                    f"🇩🇪 {de_word}\n🇨🇴 {es_word}", reply_markup=reply_markup
                )
            else:  # destiny_lang == "en"
                await message.reply_text(
                    f"🇩🇪 {de_word}\n🇺🇸 {word}", reply_markup=reply_markup
                )
    else:  # type_translation == "Simultaneous"
        # 6. Para traducción simultánea, obtener todas las traducciones
        es_word = translatorEnEs.translate(word)
        de_word = translatorEnDe.translate(word)

        # 7. Mostrar según idioma de origen
        if origin_lang == "es":
            await message.reply_text(
                f"🇨🇴 {es_word}\n🇺🇸 {word}\n🇩🇪 {de_word}", reply_markup=reply_markup
            )
        elif origin_lang == "en":
            await message.reply_text(
                f"🇺🇸 {word}\n🇨🇴 {es_word}\n🇩🇪 {de_word}", reply_markup=reply_markup
            )
        else:  # origin_lang == "de"
            await message.reply_text(
                f"🇩🇪 {de_word}\n🇨🇴 {es_word}\n🇺🇸 {word}", reply_markup=reply_markup
            )


async def show_glossary(
    update: Update, context: ContextTypes.DEFAULT_TYPE = None
) -> None:
    """Muestra y exporta el glosario actual en formato CSV"""

    global glosary

    # Verificar si hay idioma de origen configurado
    if not origin_lang:
        await update.message.reply_text(
            "🇨🇴 ❌ No has seleccionado el idioma de origen.\n usa el comando /changeorigin para configurarlo.\n\n"
            "🇺🇸 ❌ You haven't selected the source language.\n use the /changeorigin command to set it.\n\n"
            "🇩🇪 ❌ Sie haben keine Ausgangssprache ausgewählt.\n verwenden Sie den Befehl /changeorigin, um sie einzustellen."
        )
        return
    glosary_default = """(🇨🇴 Español), (🇺🇸 English), (🇩🇪 Deutsch)\n"""
    # Verificar si el glosario está vacío
    if glosary == glosary_default:
        message = {
            "es": "📜 El glosario está vacío. Traduce algunas palabras para empezar.",
            "en": "📜 The glossary is empty. Translate some words to get started.",
            "de": "📜 Das Glossar ist leer. Übersetzen Sie einige Wörter, um zu beginnen.",
        }

        if update.callback_query:
            await update.callback_query.message.reply_text(message[origin_lang])
        else:
            await update.message.reply_text(message[origin_lang])
        return
    # Mensaje inicial según el idioma
    intro_message = {
        "es": "📜 Glosario:\nEl glosario se restablecerá después de mostrarlo.",
        "en": "📜 Glossary:\nThe glossary will be reset after showing it.",
        "de": "📜 Glossar:\nDas Glossar wird nach der Anzeige zurückgesetzt.",
    }

    # Obtener el objeto message independientemente del origen
    message = update.callback_query.message if update.callback_query else update.message

    # Mostrar glosario y exportar CSV
    await message.reply_text(intro_message[origin_lang])
    await asyncio.sleep(0.3)
    await message.reply_text(glosary)

    # Enviar como documento CSV
    from io import StringIO, BytesIO

    buffer = StringIO()
    buffer.write(glosary)
    buffer.seek(0)
    bytes_buffer = BytesIO(buffer.getvalue().encode("utf-8"))
    bytes_buffer.seek(0)

    await message.reply_document(document=bytes_buffer, filename="glosario.csv")

    buffer.close()
    bytes_buffer.close()

    # Reiniciar el glosario
    glosary = glosary_default


async def view_config(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando para ver la configuración"""
    global origin_lang
    global destiny_lang
    global type_translation

    # Mapeo de códigos de idioma a emojis y nombres
    lang_names = {"es": "🇨🇴 Español", "en": "🇺🇸 English", "de": "🇩🇪 Deutsch"}

    # Mapeo de tipos de traducción según el idioma
    type_names = {
        "es": {"Individual": "🔤 Individual", "Simultaneous": "🔄 Simultáneo"},
        "en": {"Individual": "🔤 Individual", "Simultaneous": "🔄 Simultaneous"},
        "de": {"Individual": "🔤 Individuell", "Simultaneous": "🔄 Simultan"},
    }

    # Obtener nombres de idiomas con emojis
    origin_name = lang_names.get(origin_lang, "No configurado")
    destiny_name = lang_names.get(destiny_lang, "No configurado")

    if origin_lang == "es":
        no_config = "No configurado"
        config_message = (
            f"Idioma de origen: {origin_name}\n"
            f"Idioma de destino: {destiny_name if destiny_lang else no_config}\n"
            f"Tipo de traducción: {type_names['es'].get(type_translation, no_config)}"
        )
    elif origin_lang == "en":
        no_config = "Not configured"
        config_message = (
            f"Origin language: {origin_name}\n"
            f"Destination language: {destiny_name if destiny_lang else no_config}\n"
            f"Translation type: {type_names['en'].get(type_translation, no_config)}"
        )
    elif origin_lang == "de":
        no_config = "Nicht konfiguriert"
        config_message = (
            f"Ausgangssprache: {origin_name}\n"
            f"Zielsprache: {destiny_name if destiny_lang else no_config}\n"
            f"Übersetzungstyp: {type_names['de'].get(type_translation, no_config)}"
        )
    else:
        config_message = "🇨🇴 No se ha configurado el idioma de origen, usa el comando /start.\n🇺🇸 No origin language has been configured, use the /start command.\n🇩🇪 Es wurde keine Ausgangssprache konfiguriert, verwenden Sie den Befehl /start."

    await update.message.reply_text(config_message)


async def change_origin_lang(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Comando para cambiar el idioma de origen"""

    msg = "🇨🇴 Selecciona el idioma de origen:\n🇺🇸 Select the origin language:\n🇩🇪 Wählen Sie die Ausgangssprache:"
    options = {
        "es": "🇨🇴 Español",
        "en": "🇺🇸 English",
        "de": "🇩🇪 Deutsch",
    }

    keyboard = [
        [InlineKeyboardButton(options["es"], callback_data="origin_es")],
        [InlineKeyboardButton(options["en"], callback_data="origin_en")],
        [InlineKeyboardButton(options["de"], callback_data="origin_de")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(msg, reply_markup=reply_markup)


async def change_type_translation(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Comando para cambiar el tipo de traducción"""

    if origin_lang == "es":
        msg = "🇨🇴 Selecciona el tipo de traducción:"
        keyboard = [
            [InlineKeyboardButton("🔤 Individual", callback_data="type_individual")],
            [InlineKeyboardButton("🔄 Simultáneo", callback_data="type_simultaneous")],
        ]
    elif origin_lang == "en":
        msg = "🇺🇸 Select the translation type:"
        keyboard = [
            [InlineKeyboardButton("🔤 Individual", callback_data="type_individual")],
            [
                InlineKeyboardButton(
                    "🔄 Simultaneous", callback_data="type_simultaneous"
                )
            ],
        ]
    elif origin_lang == "de":
        msg = "🇩🇪 Wählen Sie den Übersetzungstyp:"
        keyboard = [
            [InlineKeyboardButton("🔤 Individuell", callback_data="type_individual")],
            [InlineKeyboardButton("🔄 Simultan", callback_data="type_simultaneous")],
        ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(msg, reply_markup=reply_markup)


async def change_destiny_lang(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Comando para cambiar el idioma de destino"""
    if type_translation != "Simultaneous":
        # Determinar idiomas disponibles excluyendo el idioma de origen
        available_langs = {"es", "en", "de"} - {origin_lang}

        # Preparar mensajes y botones según el idioma de origen
        if origin_lang == "es":
            msg = "🇨🇴 Selecciona el idioma de destino:"
            options = {"en": "🇺🇸 English", "de": "🇩🇪 Deutsch"}
        elif origin_lang == "en":
            msg = "🇺🇸 Select the destination language:"
            options = {"es": "🇨🇴 Español", "de": "🇩🇪 Deutsch"}
        elif origin_lang == "de":
            msg = "🇩🇪 Wählen Sie die Zielsprache:"
            options = {"es": "🇨🇴 Español", "en": "🇺🇸 English"}

        # Crear botones solo para los idiomas disponibles
        keyboard = [
            [InlineKeyboardButton(options[lang], callback_data=f"destiny_{lang}")]
            for lang in available_langs
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(msg, reply_markup=reply_markup)
    else:
        # Si es traducción simultánea, no se necesita seleccionar idioma de destino
        if origin_lang == "es":
            msg = "🇨🇴 En modo simultáneo se traduce a todos los idiomas automáticamente"
        elif origin_lang == "en":
            msg = "🇺🇸 In simultaneous mode, translation is done to all languages automatically"
        elif origin_lang == "de":
            msg = "🇩🇪 Im simultanen Modus wird automatisch in alle Sprachen übersetzt"
        await update.message.reply_text(msg)


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Procesa y traduce mensajes de texto según la configuración actual"""
    global glosary
    global origin_lang
    global destiny_lang
    global type_translation

    # Validar configuración
    if await validate_config(update, context):
        return

    # Preparar la nueva entrada según el idioma de origen
    if origin_lang == "es":
        new_entry = f"{update.message.text}, {translatorEsEn.translate(update.message.text)}, {translatorEsDe.translate(update.message.text)}"
    elif origin_lang == "en":
        new_entry = f"{translatorEnEs.translate(update.message.text)}, {update.message.text}, {translatorEnDe.translate(update.message.text)}"
    elif origin_lang == "de":
        new_entry = f"{translatorDeEs.translate(update.message.text)}, {translatorDeEn.translate(update.message.text)}, {update.message.text}"

    # Verificar si la entrada ya existe en el glosario
    existing_entries = glosary.split("\n")
    if new_entry not in existing_entries:
        glosary += f"{new_entry}\n"

    # Muestra un eco segun el idioma de origen, destino y tipo de traducción, usando el traductor correspondiente
    if type_translation == "Individual":
        if origin_lang == "es" and destiny_lang == "en":
            await update.message.reply_text(
                f"🇨🇴 {update.message.text}\n🇺🇸 {translatorEsEn.translate(update.message.text)}"
            )
        elif origin_lang == "es" and destiny_lang == "de":
            await update.message.reply_text(
                f"🇨🇴 {update.message.text}\n🇩🇪 {translatorEsDe.translate(update.message.text)}"
            )
        elif origin_lang == "en" and destiny_lang == "es":
            await update.message.reply_text(
                f"🇺🇸 {update.message.text}\n🇨🇴 {translatorEnEs.translate(update.message.text)}"
            )
        elif origin_lang == "en" and destiny_lang == "de":
            await update.message.reply_text(
                f"🇺🇸 {update.message.text}\n🇩🇪 {translatorEnDe.translate(update.message.text)}"
            )
        elif origin_lang == "de" and destiny_lang == "es":
            await update.message.reply_text(
                f"🇩🇪 {update.message.text}\n🇨🇴 {translatorDeEs.translate(update.message.text)}"
            )
        elif origin_lang == "de" and destiny_lang == "en":
            await update.message.reply_text(
                f"🇩🇪 {update.message.text}\n🇺🇸 {translatorDeEn.translate(update.message.text)}"
            )
    elif type_translation == "Simultaneous":
        if origin_lang == "es":
            await update.message.reply_text(
                f"🇨🇴 {update.message.text}\n🇺🇸 {translatorEsEn.translate(update.message.text)}\n🇩🇪 {translatorEsDe.translate(update.message.text)}"
            )
        elif origin_lang == "en":
            await update.message.reply_text(
                f"🇺🇸 {update.message.text}\n🇨🇴 {translatorEnEs.translate(update.message.text)}\n🇩🇪 {translatorEnDe.translate(update.message.text)}"
            )
        elif origin_lang == "de":
            await update.message.reply_text(
                f"🇩🇪 {update.message.text}\n🇨🇴 {translatorDeEs.translate(update.message.text)}\n🇺🇸 {translatorDeEn.translate(update.message.text)}"
            )


async def origin_lang_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Maneja la selección del idioma de origen"""
    query = update.callback_query
    await query.answer()

    global origin_lang
    selected_lang = query.data.split("_")[1]
    origin_lang = selected_lang

    # Mensaje de confirmación usando query.edit_message_text en lugar de update.message
    if origin_lang == "es":
        await query.edit_message_text("🇨🇴 Idioma de origen cambiado")
    elif origin_lang == "en":
        await query.edit_message_text("🇺🇸 Origin language changed")
    elif origin_lang == "de":
        await query.edit_message_text("🇩🇪 Ausgangssprache geändert")


async def type_translation_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Maneja la selección del tipo de traducción"""
    query = update.callback_query
    await query.answer()

    global type_translation

    # Obtener el tipo seleccionado del callback_data y actualizar la variable global
    selected_type = query.data.split("_")[1]
    type_translation = "Individual" if selected_type == "individual" else "Simultaneous"

    # Mensaje de confirmación según el idioma de origen
    if origin_lang == "es":
        tipo = "🔤 Individual" if type_translation == "Individual" else "🔄 Simultánea"
        await query.edit_message_text(f"🇨🇴 Tipo de traducción cambiado a: {tipo}")
    elif origin_lang == "en":
        tipo = (
            "🔤 Individual" if type_translation == "Individual" else "🔄 Simultaneous"
        )
        await query.edit_message_text(f"🇺🇸 Translation type changed to: {tipo}")
    elif origin_lang == "de":
        tipo = "🔤 Individuell" if type_translation == "Individual" else "🔄 Simultan"
        await query.edit_message_text(f"🇩🇪 Übersetzungstyp geändert zu: {tipo}")


async def destiny_lang_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Maneja la selección del idioma de destino"""
    query = update.callback_query
    await query.answer()

    global destiny_lang
    selected_lang = query.data.split("_")[1]
    destiny_lang = selected_lang

    # Mensaje de confirmación según el idioma de origen
    if origin_lang == "es":
        lang_names = {"en": "🇺🇸 Inglés", "de": "🇩🇪 Alemán"}
        await query.edit_message_text(
            f"🇨🇴 Idioma de destino cambiado a: {lang_names[destiny_lang]}"
        )
    elif origin_lang == "en":
        lang_names = {"es": "🇨🇴 Spanish", "de": "🇩🇪 German"}
        await query.edit_message_text(
            f"🇺🇸 Destination language changed to: {lang_names[destiny_lang]}"
        )
    elif origin_lang == "de":
        lang_names = {"es": "🇨🇴 Spanisch", "en": "🇺🇸 Englisch"}
        await query.edit_message_text(
            f"🇩🇪 Zielsprache geändert zu: {lang_names[destiny_lang]}"
        )


async def random_word_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Maneja los callbacks de los botones en la función random_word"""
    query = update.callback_query
    await query.answer()  # Responde al callback para quitar el estado de "cargando"

    # Determinar qué botón se presionó
    if query.data == "random_word":

        # Generar nueva palabra aleatoria
        await random_word(update, context)

    elif query.data == "add_to_glossary":

        # Validar configuración
        if await validate_config(update, context):
            return

        global glosary, ran_word

        # Preparar la nueva entrada es igual a para todos los idiomas es-en-de
        new_entry = f"{translatorEnEs.translate(ran_word)}, {ran_word}, {translatorEsDe.translate(ran_word)}"

        # Verificar si la palabra ya existe en el glosario
        existing_entries = glosary.split("\n")
        if new_entry not in existing_entries:
            glosary += f"{new_entry}\n"

            # Mensaje de confirmación según el idioma
            success_messages = {
                "es": "✅ Palabra agregada al glosario exitosamente",
                "en": "✅ Word successfully added to glossary",
                "de": "✅ Wort erfolgreich zum Glossar hinzugefügt",
            }
            await query.message.reply_text(success_messages[origin_lang])
        else:
            # Mensaje si la palabra ya existe
            duplicate_messages = {
                "es": "⚠️ Esta palabra ya existe en el glosario",
                "en": "⚠️ This word already exists in the glossary",
                "de": "⚠️ Dieses Wort existiert bereits im Glossar",
            }
            await query.message.reply_text(duplicate_messages[origin_lang])


async def validate_config(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """
    Valida la configuración actual
    Returns:
        bool: True si hay error en la configuración, False si todo está correcto
    """
    message = update.callback_query.message if update.callback_query else update.message

    # Verificar idioma de origen
    if not origin_lang:
        await message.reply_text(
            "🇨🇴 ❌ No has seleccionado el idioma de origen.\n"
            "📝 Usa el comando /changeorigin para configurarlo.\n\n"
            "🇺🇸 ❌ You haven't selected the source language.\n"
            "📝 Use the /changeorigin command to set it.\n\n"
            "🇩🇪 ❌ Sie haben keine Ausgangssprache ausgewählt.\n"
            "📝 Verwenden Sie den Befehl /changeorigin, um sie einzustellen."
        )
        return True

    # Verificar tipo de traducción
    if not type_translation:
        if origin_lang == "es":
            await message.reply_text(
                "❌ No has seleccionado el tipo de traducción.\n"
                "📝 Usa el comando /changetype para configurarlo."
            )
        elif origin_lang == "en":
            await message.reply_text(
                "❌ You haven't selected the translation type.\n"
                "📝 Use the /changetype command to set it."
            )
        else:
            await message.reply_text(
                "❌ Sie haben keinen Übersetzungstyp ausgewählt.\n"
                "📝 Verwenden Sie den Befehl /changetype, um ihn einzustellen."
            )
        return True

    # Verificar idioma de destino para traducción individual
    if not destiny_lang and type_translation == "Individual":
        if origin_lang == "es":
            await message.reply_text(
                "❌ No has seleccionado el idioma de destino.\n"
                "📝 Usa el comando /changedestiny para configurarlo."
            )
        elif origin_lang == "en":
            await message.reply_text(
                "❌ You haven't selected the destination language.\n"
                "📝 Use the /changedestiny command to set it."
            )
        else:
            await message.reply_text(
                "❌ Sie haben keine Zielsprache ausgewählt.\n"
                "📝 Verwenden Sie den Befehl /changedestiny, um sie einzustellen."
            )
        return True

    # Si no hay errores, retornar False
    return False


async def menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Maneja los callbacks de los botones del menú"""
    query = update.callback_query
    await query.answer()

    # Crear un objeto Update modificado para que funcione con los comandos existentes
    new_update = Update(update.update_id, message=query.message, callback_query=None)

    # Mapeo de callbacks a funciones
    command_mapping = {
        "menu_start": start,
        "menu_traductions": traductions,
        "menu_random": random_word,
        "menu_glossary": show_glossary,
        "menu_viewconfig": view_config,
        "menu_changeorigin": change_origin_lang,
        "menu_changetype": change_type_translation,
        "menu_changedestiny": change_destiny_lang,
    }

    try:
        # Obtener la función correspondiente y ejecutarla con el update modificado
        command_function = command_mapping.get(query.data)
        if command_function:
            await command_function(new_update, context)
    except Exception as e:
        # Mensajes de error según el idioma
        error_messages = {
            "es": "❌ Error al ejecutar el comando. Por favor, intenta de nuevo.",
            "en": "❌ Error executing command. Please try again.",
            "de": "❌ Fehler bei der Ausführung des Befehls. Bitte versuchen Sie es erneut.",
        }
        current_lang = origin_lang if origin_lang else "en"
        await query.message.reply_text(error_messages[current_lang])
        logging.error(f"Error in menu_callback: {str(e)}")


def main() -> None:
    """Inicializa y configura el bot con todos sus manejadores"""
    application = Application.builder().token(PERSONAL_TOKEN).build()

    # Comandos básicos
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("menu", menu))
    application.add_handler(CommandHandler("traductions", traductions))
    application.add_handler(CommandHandler("random", random_word))
    application.add_handler(CommandHandler("glossary", show_glossary))
    application.add_handler(CommandHandler("viewconfig", view_config))

    # Comandos de configuración
    application.add_handler(CommandHandler("changeorigin", change_origin_lang))
    application.add_handler(CommandHandler("changetype", change_type_translation))
    application.add_handler(CommandHandler("changedestiny", change_destiny_lang))

    # Manejadores de interacción
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    application.add_handler(
        CallbackQueryHandler(origin_lang_callback, pattern="^origin_")
    )
    application.add_handler(
        CallbackQueryHandler(type_translation_callback, pattern="^type_")
    )
    application.add_handler(
        CallbackQueryHandler(destiny_lang_callback, pattern="^destiny_")
    )
    application.add_handler(
        CallbackQueryHandler(
            random_word_callback, pattern="^(random_word|add_to_glossary)$"
        )
    )
    application.add_handler(CallbackQueryHandler(menu_callback, pattern="^menu_"))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
