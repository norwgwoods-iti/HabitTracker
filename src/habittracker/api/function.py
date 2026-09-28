from starlette import status
from starlette.responses import Response



async def get_habit_function(session, model, id):
    habit = await session.get(model, id)

    if not habit:
        return Response(
            status_code=status.HTTP_404_NOT_FOUND,
            content=f'Habit with ID={id} not found'
        )

    return habit