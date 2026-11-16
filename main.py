"""Inicialização do protótipo visual MeuBolso (somente View)."""
from views.main_view import MainView
from controllers import UsuarioController
from sessao import Sessao

usuario_ctrl = UsuarioController()
usuario = usuario_ctrl.buscar_por_id(1) # Ou o ID retornado pelo login
Sessao.iniciar(usuario)

if __name__ == '__main__':
    MainView().mainloop()
