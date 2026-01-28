# 🚀 Tu Flujo de Trabajo Diario (Cheat Sheet)

Guarda este archivo cerca. Estos son los únicos pasos que necesitas recordar.

---

## 1️⃣ Fase de Edición (Día a Día)
Trabaja tranquilo en tu archivo principal.
- 📂 Archivo a editar: `index.html`
- ❌ **NO toques:** `index.min.html` (se genera solo)

---

## 2️⃣ Fase de Revisión (¿Cómo va quedando?)
Cuando quieras ver tus avances en el navegador antes de publicar.

**En tu terminal:**
```bash
python3 deploy.py --target preview
```
- Abre: [http://localhost:8000](http://localhost:8000)
- Para detener el servidor: Presiona `Ctrl + C`

---

## 3️⃣ Fase de Publicación (Subir a Internet)
Cuando estés listo para que el mundo vea tus cambios.

**En tu terminal:**
```bash
# 1. Agrega tus cambios
git add .

# 2. Guárdalos con un mensaje (esto activa el MINIFICADOR automático 🤖)
git commit -m "Descripción de lo que cambiaste"

# 3. Envíalos a la nube (esto activa el DEPLOY automático ✈️)
git push origin main
```
*(Si te pide contraseña, usa el Token que generamos hoy)*

---

## 🆘 Emergencias

### "¡Rompí algo y quiero volver atrás!"
No entres en pánico. El sistema guardó una copia antes de que hicieras nada.
1. Ve a la carpeta `backups/`.
2. Busca el archivo con la fecha de hoy.
3. Copia su contenido y pégalo de vuelta en `index.html`.

### "Git me da error de permisos"
Seguramente caducó tu sesión.
- Vuelve a generar el Token siguiendo el link: [GitHub Tokens](https://github.com/settings/tokens/new)
- Recuerda marcar: `repo` y `workflow`.

---
*Cystec Global - Automation Pipeline v1.0*
