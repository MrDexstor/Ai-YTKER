from asgiref.sync import sync_to_async

from Core.models import TGUsers, Tags, UserTask


async def taskCreate(user_id, data):
    name = data['inter_data']['name']
    description = data['inter_data']['description']
    datetime = data['inter_data']['datetime']
    tags_list = data['inter_data']['tags']

    user, created = await sync_to_async(TGUsers.objects.get_or_create)(user_id=user_id)

    tags = []
    for tag_name in tags_list:
        tag, created = await sync_to_async(Tags.objects.get_or_create)(name=tag_name)
        tags.append(tag)

    user_task = await sync_to_async(UserTask.objects.create)(
        user=user,
        name=name,
        descriptions=description,
        datetime=datetime
    )

    await sync_to_async(user_task.tags.set)(tags)
    await sync_to_async(user_task.save)()

async def getUserTask(user_id):
    dataset = await sync_to_async(list)(
        UserTask.objects.select_related('user').prefetch_related('tags').all()
    )
    tasks = []
    for task in dataset:
        tasks.append(
            {
                "name": task.name,
                "descriptions": task.descriptions,
                "datetime": task.datetime,
                "tags": [tag.name for tag in task.tags.all()],  # Преобразуем QuerySet в список имен
            }
        )
    if not tasks:
        tasks = ['У пользователя нет ни одного задания']
    return 'Задачи пользователя: '+ str(tasks)