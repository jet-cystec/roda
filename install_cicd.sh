#!/bin/bash

# =================================================================
# Ancla CI/CD - Inyector de Infraestructura con Validación
# "Protegiendo el proyecto del error humano desde el origen"
# =================================================================

# Colores Profesionales
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Rutas del Almacén Maestro
MASTER_PATH="/home/jet/cystec/CICD"
TEMPLATES="$MASTER_PATH/infra-templates"
DOCS="$MASTER_PATH/docs/architecture"

echo -e "${BLUE}🛡️  Iniciando Protocolo Sentinel - Arquitectura Ancla${NC}"

# 1. VALIDACIÓN CRÍTICA: ¿Existe el archivo fuente?
echo -e "\n${YELLOW}[1/5] Validando entorno del proyecto...${NC}"
if [ ! -f "index.html" ]; then
    echo -e "${RED}❌ ERROR: No se encontró 'index.html' en este directorio.${NC}"
    echo -e "💡 Sugerencia: Coloca tu archivo HTML principal antes de inyectar la infraestructura."
    exit 1
fi
echo -e "${GREEN}✅ Archivo fuente 'index.html' detectado.${NC}"

# 2. VALIDACIÓN DEL MAESTRO: ¿Está el almacén disponible?
if [ ! -d "$MASTER_PATH" ]; then
    echo -e "${RED}❌ ERROR: El almacén maestro no está en $MASTER_PATH${NC}"
    exit 1
fi

# 3. PREPARACIÓN DE GIT
if [ ! -d ".git" ]; then
    echo -e "${YELLOW}⚠️  No se detectó repositorio Git. Inicializando...${NC}"
    git init
fi

# 4. INYECCIÓN DE ARCHIVOS (Desde Central a Local)
echo -e "\n${YELLOW}[2/5] Inyectando plantillas desde el almacén central...${NC}"
cp "$TEMPLATES/build_site.py" .
cp "$TEMPLATES/deploy.py" .
cp "$TEMPLATES/WORKFLOW_CHEATSHEET.md" .
cp "$DOCS/CI_CD_ARCHITECTURE.md" .
echo -e "${GREEN}✅ Componentes core inyectados.${NC}"

# 5. CONFIGURACIÓN DE VIGILANCIA (Hooks)
echo -e "\n${YELLOW}[3/5] Configurando Git Hooks personalizados...${NC}"
mkdir -p .githooks
cp "$TEMPLATES/pre-commit" .githooks/
chmod +x .githooks/pre-commit
chmod +x build_site.py
chmod +x deploy.py

# Vincular Git con nuestra carpeta de hooks
git config core.hooksPath .githooks
echo -e "${GREEN}✅ Git Hook vinculado a .githooks/pre-commit${NC}"

# 6. INICIALIZACIÓN DE ENTORNO
echo -e "\n${YELLOW}[4/5] Creando áreas de seguridad...${NC}"
mkdir -p backups
echo -e "${GREEN}✅ Directorio de backups listo.${NC}"

# 7. PRUEBA DE FUEGO (Build Inicial)
echo -e "\n${YELLOW}[5/5] Ejecutando primer ciclo de optimización...${NC}"
python3 build_site.py

if [ $? -eq 0 ]; then
    echo -e "\n${GREEN}=================================================${NC}"
    echo -e "${GREEN}🚀 INFRAESTRUCTURA INSTALADA Y VALIDADA${NC}"
    echo -e "${GREEN}=================================================${NC}"
    echo -e "Proyecto: $(basename "$PWD")"
    echo -e "Estado: Listo para desarrollo profesional"
else
    echo -e "${RED}❌ El build inicial falló. Revisa errores en index.html.${NC}"
fi