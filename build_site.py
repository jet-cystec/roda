#!/usr/bin/env python3
"""
Pipeline de Despliegue Local para Sitio Web Estático
====================================================
Script de automatización que realiza backup, minificación y optimización
de archivos HTML antes del despliegue.

Autor: Generado para Ancla
Fecha: 2026-01-25
"""

import os
import re
import shutil
from datetime import datetime


class BuildPipeline:
    """Pipeline de construcción para sitios web estáticos."""

    def __init__(self, source_file='index.html', backup_dir='backups'):
        """
        Inicializa el pipeline de construcción.

        Args:
            source_file (str): Nombre del archivo HTML a procesar
            backup_dir (str): Directorio donde se guardarán los backups
        """
        self.source_file = source_file
        self.backup_dir = backup_dir
        self.original_size = 0
        self.final_size = 0

    def create_backup(self):
        """
        Crea un backup del archivo original con timestamp.

        Returns:
            str: Ruta del archivo de backup creado

        Raises:
            FileNotFoundError: Si el archivo source no existe
            OSError: Si hay problemas al crear el directorio o copiar el archivo
        """
        try:
            # Verificar que el archivo existe
            if not os.path.exists(self.source_file):
                raise FileNotFoundError(
                    f"❌ Error: El archivo '{self.source_file}' no existe"
                )

            # Crear directorio de backups si no existe
            os.makedirs(self.backup_dir, exist_ok=True)

            # Generar nombre de backup con timestamp
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename, ext = os.path.splitext(self.source_file)
            backup_filename = f"{filename}_{timestamp}{ext}"
            backup_path = os.path.join(self.backup_dir, backup_filename)

            # Copiar archivo
            shutil.copy2(self.source_file, backup_path)
            print(f"✅ Backup creado: {backup_path}")

            return backup_path

        except Exception as e:
            raise OSError(f"Error al crear backup: {str(e)}")

    def minify_html(self, html_content):
        """
        Minifica el contenido HTML eliminando espacios y comentarios innecesarios.

        Args:
            html_content (str): Contenido HTML original

        Returns:
            str: Contenido HTML minificado
        """
        # Eliminar comentarios HTML EXCEPTO los críticos para navegación
        # Protege: comentarios con 'id=' y etiquetas <!-- CONTENT -->
        html_content = re.sub(
            r'<!--(?!.*?(?:id=|CONTENT)).*?-->',
            '',
            html_content,
            flags=re.DOTALL
        )

        # Eliminar espacios en blanco múltiples y saltos de línea
        html_content = re.sub(r'\s+', ' ', html_content)

        # Eliminar espacios alrededor de etiquetas
        html_content = re.sub(r'>\s+<', '><', html_content)

        # Eliminar espacios al inicio y final
        html_content = html_content.strip()

        return html_content

    def optimize_scripts(self, html_content):
        """
        Optimiza las etiquetas <script> añadiendo el atributo defer si no existe.

        Args:
            html_content (str): Contenido HTML

        Returns:
            str: Contenido HTML con scripts optimizados
        """
        def add_defer(match):
            """Función helper para añadir defer a etiquetas script."""
            script_tag = match.group(0)

            # Si ya tiene defer o async, no hacer nada
            if 'defer' in script_tag or 'async' in script_tag:
                return script_tag

            # Si es un script inline (sin src), no añadir defer
            if 'src=' not in script_tag:
                return script_tag

            # Añadir defer antes del cierre de la etiqueta
            script_tag = script_tag.replace('<script', '<script defer', 1)
            return script_tag

        # Buscar todas las etiquetas <script> y optimizarlas
        html_content = re.sub(
            r'<script[^>]*>',
            add_defer,
            html_content,
            flags=re.IGNORECASE
        )

        return html_content

    def calculate_savings(self):
        """
        Calcula el porcentaje de ahorro de espacio.

        Returns:
            float: Porcentaje de ahorro (0-100)
        """
        if self.original_size == 0:
            return 0.0

        savings = ((self.original_size - self.final_size) / self.original_size) * 100
        return round(savings, 2)

    def print_metrics(self):
        """Imprime las métricas del proceso de minificación."""
        print("\n" + "=" * 60)
        print("📊 REPORTE DE MÉTRICAS")
        print("=" * 60)
        print(f"📄 Archivo procesado: {self.source_file}")
        print(f"📦 Tamaño original:    {self.original_size:,} bytes")
        print(f"📦 Tamaño minificado:  {self.final_size:,} bytes")
        print(f"💾 Ahorro de espacio:  {self.calculate_savings()}%")
        print(f"📉 Bytes ahorrados:    {self.original_size - self.final_size:,} bytes")
        print("=" * 60 + "\n")

    def build(self):
        """
        Ejecuta el pipeline completo de construcción.

        Returns:
            bool: True si el proceso fue exitoso, False en caso contrario
        """
        try:
            print("\n🚀 Iniciando Pipeline de Despliegue Local")
            print("=" * 60)

            # Paso 1: Crear backup
            print("\n📋 Paso 1/4: Creando backup...")
            self.create_backup()

            # Paso 2: Leer archivo original
            print("📖 Paso 2/4: Leyendo archivo original...")
            with open(self.source_file, 'r', encoding='utf-8') as f:
                html_content = f.read()
                self.original_size = len(html_content.encode('utf-8'))
            print(f"   Tamaño original: {self.original_size:,} bytes")

            # Paso 3: Minificar HTML
            print("⚙️  Paso 3/4: Minificando HTML...")
            html_content = self.minify_html(html_content)
            print("   ✓ Espacios y comentarios eliminados")

            # Optimizar scripts
            html_content = self.optimize_scripts(html_content)
            print("   ✓ Scripts optimizados con defer")

            # Paso 4: Guardar archivo minificado
            print("💾 Paso 4/4: Guardando archivo optimizado...")
            output_file = self.source_file.replace('.html', '.min.html')

            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
                self.final_size = len(html_content.encode('utf-8'))

            print(f"   ✓ Archivo guardado: {output_file}")

            # Mostrar métricas finales
            self.print_metrics()

            print("✅ Pipeline completado exitosamente!\n")
            return True

        except FileNotFoundError as e:
            print(f"\n❌ Error: {str(e)}")
            print("   Asegúrate de que el archivo existe en el directorio actual.\n")
            return False

        except PermissionError as e:
            print(f"\n❌ Error de permisos: {str(e)}")
            print("   Verifica que tienes permisos de escritura en el directorio.\n")
            return False

        except Exception as e:
            print(f"\n❌ Error inesperado: {str(e)}")
            print("   No se realizaron cambios en el archivo original.\n")
            return False


def main():
    """Función principal del script."""
    # Crear instancia del pipeline
    pipeline = BuildPipeline(source_file='index.html', backup_dir='backups')

    # Ejecutar construcción
    success = pipeline.build()

    # Retornar código de salida apropiado
    exit(0 if success else 1)


if __name__ == '__main__':
    main()
