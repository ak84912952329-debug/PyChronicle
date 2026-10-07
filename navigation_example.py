from pychronicle.history import History, ExecutionState
from navigation import Navigation


history = History()

for i in range(3):
    state = ExecutionState(
        step=i + 1,
        line=i + 1,
        function="<module>",
        source=f"x = {i}",
        variables={"x": i}
    )
    history.add(state)


navigation = Navigation(history)

navigation.jump_to(0)
print("Current:", navigation.current())

print("Next:", navigation.next())
print("Next:", navigation.next())

print("Previous:", navigation.previous())