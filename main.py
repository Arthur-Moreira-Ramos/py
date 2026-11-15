"""Inicialização do MeuBolso, com DPI-aware no Windows."""
import sys


def configurar_dpi_windows():
    if sys.platform != 'win32':
        return
    try:
        import ctypes
        # A chamada precisa ocorrer antes da criação do primeiro Tk().
        ctypes.windll.shcore.SetProcessDpiAwareness(2)
    except (OSError, AttributeError, ValueError):
        try:
            ctypes.windll.user32.SetProcessDPIAware()
        except (OSError, AttributeError):
            pass


if __name__ == '__main__':
    configurar_dpi_windows()
    from views.main_view import MainView
    MainView().mainloop()
