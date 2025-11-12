import discord
from discord.ext import commands
from discord.ui import View, Select
import requests, random, json, os
import config

# -----------------------------
# CONFIGURACIÓN DEL BOT
# -----------------------------
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

INVENTARIO_FILE = "inventario.json"
inventario = {}

# -----------------------------
# FUNCIONES DE INVENTARIO
# -----------------------------
def cargar_inventario():
    global inventario
    if os.path.exists(INVENTARIO_FILE):
        with open(INVENTARIO_FILE, "r", encoding="utf-8") as f:
            inventario = json.load(f)
    else:
        inventario = {}

def guardar_inventario():
    with open(INVENTARIO_FILE, "w", encoding="utf-8") as f:
        json.dump(inventario, f, ensure_ascii=False, indent=4)

cargar_inventario()

# -----------------------------
# COMANDO: SACAR CARTA
# -----------------------------
@bot.command()
async def pokem(ctx):
    try:
        cartas = requests.get("https://api.tcgdex.net/v2/en/cards").json()
        carta = random.choice(cartas)

        nombre = carta.get("name", "Desconocido")
        rareza = carta.get("rarity", "Normal")
        imagen = f"{carta['image']}/high.png"
        hp = int(carta.get("hp", 0) or 0)
        tipos = carta.get("types", [])
        ataques = carta.get("attacks", [])

        user_id = str(ctx.author.id)
        inventario.setdefault(user_id, {})
        inventario[user_id].setdefault(rareza, [])

        inventario[user_id][rareza].append({
            "name": nombre,
            "url": imagen,
            "hp": hp,
            "types": tipos,
            "attacks": ataques
        })
        guardar_inventario()

        # Embed para mostrar la carta
        embed = discord.Embed(
            title=f"🎴 {nombre}",
            description=f"**Rareza:** {rareza}\n**HP:** {hp}\n**Tipos:** {', '.join(tipos) if tipos else 'Desconocido'}",
            color=discord.Color.blue()
        )
        if ataques:
            atk_text = ", ".join([f"{atk.get('name','')} ({atk.get('damage','0')})" for atk in ataques if isinstance(atk, dict)])
            embed.add_field(name="Ataques", value=atk_text or "Ninguno")
        embed.set_image(url=imagen)
        await ctx.send(embed=embed)

    except Exception as e:
        await ctx.send(f"⚠️ Error al sacar carta: {e}")

# -----------------------------
# COMANDO: VER INVENTARIO
# -----------------------------
@bot.command(name="inve")
async def inve(ctx):
    user_id = str(ctx.author.id)
    if user_id not in inventario or not any(inventario[user_id].values()):
        await ctx.send("📭 No tienes cartas. Usa `!pokem` para conseguir una.")
        return

    todas_cartas = []
    for rareza, cartas in inventario[user_id].items():
        for c in cartas:
            todas_cartas.append({"name": c["name"], "url": c["url"], "rareza": rareza})

    opciones = [
        discord.SelectOption(
            label=c["name"],
            description=f"Rareza: {c['rareza']}",
            value=str(i)
        )
        for i, c in enumerate(todas_cartas[:25])
    ]

    menu = Select(placeholder="📚 Selecciona una carta", options=opciones)

    async def callback(interaction: discord.Interaction):
        index = int(menu.values[0])
        c = todas_cartas[index]
        embed = discord.Embed(
            title=f"🎴 {c['name']}",
            description=f"Rareza: {c['rareza']}",
            color=discord.Color.green()
        )
        embed.set_image(url=c["url"])
        await interaction.response.send_message(embed=embed, ephemeral=True)

    menu.callback = callback
    view = View()
    view.add_item(menu)
    await ctx.send("📚 Tu inventario:", view=view)

# -----------------------------
# COMANDO: ESTADÍSTICAS
# -----------------------------
@bot.command(name="stats")
async def stats(ctx):
    user_id = str(ctx.author.id)
    if user_id not in inventario or not any(inventario[user_id].values()):
        await ctx.send("📭 No tienes cartas aún.")
        return

    total = 0
    hp_total = 0
    raras = 0
    poder_total = 0

    for rareza, cartas in inventario[user_id].items():
        total += len(cartas)
        if rareza.lower() in ["rare", "ultra rare", "legendary"]:
            raras += len(cartas)
        for c in cartas:
            hp_total += int(c.get("hp", 0) or 0)
            for atk in c.get("attacks", []):
                if isinstance(atk, dict):
                    dmg = atk.get("damage","0").replace("+","").replace("×","0")
                    if dmg.isdigit():
                        poder_total += int(dmg)

    promedio_hp = hp_total // total if total else 0

    embed = discord.Embed(title=f"📊 Estadísticas de {ctx.author.name}", color=discord.Color.purple)
    embed.add_field(name="Total cartas", value=str(total))
    embed.add_field(name="Cartas raras", value=str(raras))
    embed.add_field(name="Promedio HP", value=str(promedio_hp))
    embed.add_field(name="Poder total ataques", value=str(poder_total))

    await ctx.send(embed=embed)

# -----------------------------
# COMANDO: RANKING
# -----------------------------
@bot.command(name="ranking")
async def ranking(ctx):
    ranking = []
    for user_id, rarezas in inventario.items():
        total_raras = sum(len(rarezas[r]) for r in rarezas if r.lower() in ["rare","ultra rare","legendary"])
        ranking.append((user_id, total_raras))

    ranking.sort(key=lambda x: x[1], reverse=True)

    texto = ""
    for i, (uid, raras) in enumerate(ranking[:10], start=1):
        try:
            user = await bot.fetch_user(int(uid))
            texto += f"{i}. {user.name} - {raras} cartas raras\n"
        except:
            texto += f"{i}. Usuario eliminado - {raras} cartas raras\n"

    embed = discord.Embed(title="🏆 Ranking cartas raras", description=texto or "Aún no hay jugadores", color=discord.Color.gold)
    await ctx.send(embed=embed)

# -----------------------------
# INICIO DEL BOT
# -----------------------------
bot.run(config.TOKEN)
