"""Entry point."""

import logging
import sys
from .gui.app import App


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.FileHandler("app.log", encoding="utf-8"),
            logging.StreamHandler(sys.stdout),
        ],
    )
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
