#!/usr/bin/env python3
"""
Script de Despliegue Automático
================================
Ejecuta el build pipeline y despliega automáticamente el sitio.

Uso:
    python3 deploy.py [--target netlify|github-pages|ftp]
"""

import argparse
import os
import subprocess
import sys


class DeployManager:
    """Gestor de despliegue multi-plataforma."""

    def __init__(self):
        """Inicializa el gestor de despliegue."""
        self.project_root = os.path.dirname(os.path.abspath(__file__))

    def run_build(self):
        """
        Ejecuta el pipeline de construcción.

        Returns:
            bool: True si el build fue exitoso
        """
        print("🔨 Ejecutando build pipeline...")
        try:
            result = subprocess.run(
                ['python3', 'build_site.py'],
                cwd=self.project_root,
                check=True,
                capture_output=True,
                text=True
            )
            print(result.stdout)
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Error en el build: {e.stderr}")
            return False

    def deploy_github_pages(self):
        """
        Despliega a GitHub Pages usando gh-pages branch.

        Returns:
            bool: True si el deploy fue exitoso
        """
        print("\n🚀 Desplegando a GitHub Pages...")

        commands = [
            # Crear rama gh-pages si no existe
            ['git', 'checkout', '-b', 'gh-pages'],
            # Copiar index.min.html como index.html
            ['cp', 'index.min.html', 'index.html'],
            # Hacer commit
            ['git', 'add', 'index.html', 'index.min.html', '*.png', '*.css'],
            ['git', 'commit', '-m', 'Deploy to GitHub Pages'],
            # Push
            ['git', 'push', 'origin', 'gh-pages', '--force'],
            # Volver a main
            ['git', 'checkout', 'main']
        ]

        for cmd in commands:
            try:
                subprocess.run(cmd, cwd=self.project_root, check=True)
            except subprocess.CalledProcessError as e:
                # Ignorar algunos errores comunes
                if 'already exists' in str(e) or 'nothing to commit' in str(e):
                    continue
                print(f"⚠️  Advertencia: {e}")

        print("✅ Deploy a GitHub Pages completado")
        print("📝 Activa GitHub Pages en: Settings > Pages > Source: gh-pages")
        return True

    def deploy_netlify(self):
        """
        Despliega a Netlify usando Netlify CLI.

        Returns:
            bool: True si el deploy fue exitoso
        """
        print("\n🚀 Desplegando a Netlify...")

        # Verificar si Netlify CLI está instalado
        try:
            subprocess.run(
                ['netlify', '--version'],
                check=True,
                capture_output=True
            )
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("❌ Netlify CLI no está instalado")
            print("📦 Instala con: npm install -g netlify-cli")
            return False

        try:
            # Deploy
            subprocess.run(
                ['netlify', 'deploy', '--prod', '--dir', '.'],
                cwd=self.project_root,
                check=True
            )
            print("✅ Deploy a Netlify completado")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Error en deploy: {e}")
            return False

    def deploy_local_preview(self):
        """
        Crea un servidor local para preview en un puerto disponible.

        Returns:
            bool: True si se inició correctamente
        """
        print("\n🌐 Iniciando servidor local de preview...")
        
        # Buscar puerto disponible
        import socket
        port = 8000
        while port < 8010:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                res = sock.connect_ex(('localhost', port))
                if res != 0: # Puerto libre (no pudo conectar)
                    break
                port += 1
        
        url = f"http://localhost:{port}"
        print(f"✅ Servidor activo en: {url}")
        print("📝 Presiona Ctrl+C para detener\n")

        try:
            # Abrir navegador automáticamente (opcional, pero útil)
            try:
                if os.uname().sysname == 'Linux':
                    subprocess.run(['xdg-open', url], stderr=subprocess.DEVNULL)
            except Exception:
                pass

            subprocess.run(
                ['python3', '-m', 'http.server', str(port)],
                cwd=self.project_root,
                check=True
            )
            return True
        except KeyboardInterrupt:
            print("\n\n✅ Servidor detenido")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Error al iniciar servidor: {e}")
            return False

    def deploy(self, target):
        """
        Ejecuta el despliegue según el target especificado.

        Args:
            target (str): Plataforma de despliegue

        Returns:
            bool: True si fue exitoso
        """
        # Ejecutar build primero
        if not self.run_build():
            return False

        # Desplegar según target
        deploy_methods = {
            'github-pages': self.deploy_github_pages,
            'netlify': self.deploy_netlify,
            'preview': self.deploy_local_preview
        }

        method = deploy_methods.get(target)
        if not method:
            print(f"❌ Target desconocido: {target}")
            print(f"Opciones: {', '.join(deploy_methods.keys())}")
            return False

        return method()


def main():
    """Función principal del script."""
    parser = argparse.ArgumentParser(
        description='🚀 Script de Despliegue Automático'
    )
    parser.add_argument(
        '--target',
        choices=['github-pages', 'netlify', 'preview'],
        default='preview',
        help='Plataforma de despliegue (default: preview)'
    )

    args = parser.parse_args()

    # Ejecutar despliegue
    deployer = DeployManager()
    success = deployer.deploy(args.target)

    exit(0 if success else 1)


if __name__ == '__main__':
    main()
