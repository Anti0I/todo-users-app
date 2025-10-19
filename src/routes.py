from handlers import TaskHandler, UserHandler


def register_routes(app):
    task_view = TaskHandler.as_view('task_api')
    app.add_url_rule('/tasks/', view_func=task_view, methods=['GET'])
    app.add_url_rule('/tasks/', view_func=task_view, methods=['POST'])
    app.add_url_rule('/tasks/<int:item_id>', view_func=task_view, methods=['GET', 'PATCH', 'DELETE'])
    user_view = UserHandler.as_view('user_api')
    app.add_url_rule('/users/', view_func=user_view, methods=['GET'])
    app.add_url_rule('/users/', view_func=user_view, methods=['POST'])
    app.add_url_rule('/users/<int:item_id>', view_func=user_view, methods=['GET', 'PATCH', 'DELETE'])