import asyncio
import os
import django
from asgiref.sync import sync_to_async

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webcore.settings")
django.setup()
from Core.models import UserTask

async def test():
    # Используем select_related для user и prefetch_related для tags
    dataset = await sync_to_async(list)(
        UserTask.objects.select_related('user').prefetch_related('tags').filter(id=1)
    )
    result = []
    for task in dataset:
        result.append(
            {
                "name": task.name,
                "descriptions": task.descriptions,
                "datetime": task.datetime,
                "tags": [tag.name for tag in task.tags.all()],  # Преобразуем QuerySet в список имен
            }
        )
    return result

async def main():
    t = await test()  # Ожидаем результат выполнения test()
    return t

# Запускаем основную функцию с помощью asyncio
result = asyncio.run(main())
print(result)  # Это должно вывести результат
