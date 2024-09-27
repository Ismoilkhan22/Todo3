def main(request):
    result = {}
    path = request.path.replace("/", " ").replace('-', " ").split()
    if path:
        path = path[0]
    else:
        path = 'nothing'
    sidebars = {
        "users": 'users_active',
        "task": "task_active",
    }.get(path, 'nothing')

    result.update({sidebars: 'active'})
    return result
