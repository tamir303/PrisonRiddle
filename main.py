import prisoners_controller
import prisoners_game_model
import prisoners_view

c = prisoners_controller.Controller(prisoners_game_model.prisoners_model, prisoners_view.main_view)