import asyncio
import os
from pyngrok import ngrok


# Configurar Django
async def run_django():
    os.system("python manage.py runserver 0.0.0.0:8000")


# Configurar Gradio
async def run_gradio():
    from ui.app import create_ui
    app = create_ui()
    gradio_tunnel = ngrok.connect(7860)
    print("Gradio public URL:", gradio_tunnel.public_url)
    app.launch(server_name="0.0.0.0", server_port=7860, share=False)


async def main():
    # Configurar ngrok antes de iniciar servidores
    ngrok.kill()
    auth_token = os.getenv("NGROK_TOKEN")
    ngrok.set_auth_token(auth_token)
    django_tunnel = ngrok.connect(8000)
    print("Django public URL:", django_tunnel.public_url)
    os.environ["DJANGO_PUBLIC_URL"] = django_tunnel.public_url

    # Ejecutar Django y Gradio en paralelo
    await asyncio.gather(
        asyncio.to_thread(os.system, "python manage.py runserver 0.0.0.0:8000"),
        run_gradio()
    )


if __name__ == "__main__":
    asyncio.run(main())