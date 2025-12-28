"""Example web server for the add-on."""

import logging

from aiohttp import web

from my_addon.config import Config
from my_addon.supervisor import SupervisorAPI

logger = logging.getLogger(__name__)


async def handle_index(request: web.Request) -> web.Response:
    """Handle index page request."""
    return web.Response(
        text="<h1>My Python Add-on</h1><p>The add-on is running!</p>",
        content_type="text/html",
    )


async def handle_health(request: web.Request) -> web.Response:
    """Handle health check request."""
    supervisor: SupervisorAPI = request.app["supervisor"]

    try:
        info = await supervisor.get_addon_info()
        return web.json_response(
            {
                "status": "healthy",
                "addon": info.get("data", {}).get("name", "unknown"),
            }
        )
    except Exception as e:
        logger.error("Health check failed: %s", e)
        return web.json_response({"status": "unhealthy", "error": str(e)}, status=500)


async def start_server(config: Config) -> None:
    """Start the web server.

    Args:
        config: Add-on configuration
    """
    app = web.Application()

    # Initialize Supervisor API client
    supervisor = SupervisorAPI()
    app["supervisor"] = supervisor
    app["config"] = config

    # Setup routes
    app.router.add_get("/", handle_index)
    app.router.add_get("/health", handle_health)

    # Run the server
    logger.info("Starting web server on port 8000...")
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 8000)
    await site.start()

    logger.info("Server started successfully")

    # Keep the server running
    try:
        # This will run forever until interrupted
        import asyncio

        await asyncio.Event().wait()
    finally:
        await supervisor.__aexit__(None, None, None)
        await runner.cleanup()
