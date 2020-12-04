# -*- coding: utf-8 -*-

import contextlib
from copy import copy
from io import StringIO
from typing import TYPE_CHECKING, Any, AsyncGenerator, Generator, Optional, TypeVar, Union

import pytest

import steam
from steam.ext import commands
from tests.mocks import GROUP_MESSAGE

CE = TypeVar("CE", bound=commands.CommandError)
T = TypeVar("T")
IsInstanceable = Union["type[T]", "tuple[type[T], ...]"]

if TYPE_CHECKING:
    SomeCoolType = int


@pytest.mark.asyncio
async def test_commands():
    with pytest.raises(TypeError):

        @commands.command
        def not_valid(_):
            ...

    with pytest.raises(TypeError):

        @commands.command(name=123)
        async def _123(_) -> None:
            ...

    with pytest.raises(TypeError):

        @commands.command(aliases=[1, 2, 3])
        async def _123(_) -> None:
            ...

    with pytest.raises(steam.ClientException):

        @commands.command
        async def not_valid() -> None:
            ...

    class MyCog(commands.Cog):
        with pytest.raises(steam.ClientException):

            @commands.command
            async def not_even_close() -> None:  # noqa
                ...

    bot = TestBot()

    class MyCog(commands.Cog):
        @commands.command
        async def not_valid(self) -> None:
            ...

    with pytest.raises(steam.ClientException):
        bot.add_cog(MyCog())


def test_annotations() -> None:
    @commands.command
    async def cool(ctx: "OopsATypo"):  # noqa
        ...

    @commands.command
    async def cool_ctx(ctx: "SomeCoolType") -> None:
        ...

    assert cool_ctx.params.popitem()[1].annotation == "SomeCoolType"  # not evaluated cause its on ctx

    @commands.command
    async def some_cool_command(ctx, cool_type: "SomeCoolType") -> None:
        ...

    assert some_cool_command.clean_params.popitem()[1].annotation is SomeCoolType  # should be evaluated

    users = Union[steam.User, int, str]

    @commands.command
    async def get_an_user(ctx, user: "users") -> None:
        ...

    assert get_an_user.clean_params.popitem()[1].annotation == users


class CustomConverter(commands.Converter[tuple]):
    async def convert(self, ctx: commands.Context, argument: str) -> tuple:
        ...


@pytest.mark.parametrize(
    "param_type, expected",
    [
        (None, TypeError),
        (str, TypeError),
        (int, int),
        (CustomConverter, CustomConverter),
        ("None", TypeError),
        ("str", TypeError),
        ("int", int),
        ("CustomConverter", CustomConverter),
    ],
)
def test_greedy(param_type: Union[type, str], expected: Union[int, "type[Exception]"]):
    if issubclass(expected, Exception):
        with pytest.raises(TypeError):

            @commands.command
            async def greedy(_, param: commands.Greedy[param_type]) -> None:
                ...

    else:

        @commands.command
        async def greedy(_, param: commands.Greedy[param_type]) -> None:
            ...

        assert greedy.clean_params["param"].annotation.converter is expected


class TestBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="")
        self.MESSAGE = GROUP_MESSAGE

    @contextlib.asynccontextmanager
    async def raises_command_error(
        self, expected_errors: "IsInstanceable[type[CE]]", content: str
    ) -> AsyncGenerator[None, None]:
        expected_errors = (expected_errors,) if not isinstance(expected_errors, tuple) else expected_errors

        async def on_command_error(ctx: commands.Context, error: CE) -> None:
            error = error.__class__ if isinstance(error, Exception) else error
            if ctx.message.content == content:
                if error not in expected_errors:
                    raise error

        self.add_listener(on_command_error)

        yield

    @contextlib.asynccontextmanager
    async def returns_command_completion(self, content: str) -> AsyncGenerator[None, None]:
        async def on_command_error(ctx: commands.Context, error: CE) -> None:
            if ctx.message.content == content:
                raise error

        self.add_listener(on_command_error)

        yield

    async def process_commands(
        self,
        arguments: Optional[str] = None,
        exception: Optional["type[CE]"] = None,
        command: Optional[commands.Command] = None,
    ) -> None:
        command = command or list(self.__commands__.values())[-1]
        message = copy(self.MESSAGE)
        message.content = f"{command.qualified_name} {arguments or ''}".strip()

        if exception is not None:

            async with self.raises_command_error(exception, message.content):
                await super().process_commands(message)

        else:

            async with self.returns_command_completion(message.content):
                await super().process_commands(message)

    async def on_error(self, event: str, error: Exception, *args: Any, **kwargs: Any) -> None:
        try:
            ctx: commands.Context = args[0]  # expose some locals
            lex = ctx.lex
            message = ctx.message
            command = ctx.command
        except (IndexError, AttributeError):
            pass
        raise SystemExit  # we need to propagate a SystemExit for pytest to be able to pick up errors


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "input, excepted_exception",
    [
        ("", commands.MissingRequiredArgument),
        ("1234", None),
        ("1234 1234", None),
        ("string", commands.BadArgument),
    ],
)
async def test_positional_or_keyword_commands(
    input: str, excepted_exception: Optional["type[commands.CommandError]"]
) -> None:
    bot = TestBot()

    @bot.command
    async def test_positional(_, number: int) -> None:
        assert isinstance(number, int)
        assert len(str(number)) == 4

    await bot.process_commands(input, excepted_exception)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "input, expected_exception",
    [
        ("", None),
        ("1234", None),
        ("1234 1234", None),
        ("1234        1234        1234        1234        1234", None),
        ("string", commands.BadArgument),
    ],
)
async def test_variadic_commands(input: str, expected_exception: commands.CommandError) -> None:
    bot = TestBot()

    @bot.command
    async def test_var(_, *numbers: int) -> None:
        assert isinstance(numbers, tuple)
        for number in numbers:
            assert isinstance(number, int)
            assert len(str(number)) == 4

    await bot.process_commands(input, expected_exception)


@pytest.mark.asyncio
async def test_positional_only_commands():
    bot = TestBot()

    @bot.command
    async def test_consume_rest_int(_, *, number: int) -> None:
        assert isinstance(number, int)

    inputs = [
        ("", commands.MissingRequiredArgument),
        ("1234", None),
        ("123412341234", None),
        ("string", commands.BadArgument),
    ]

    for args, excepted_exception in inputs:
        await bot.process_commands(args, excepted_exception)

    @bot.command
    async def test_consume_rest_str(_, *, string: str) -> None:
        assert isinstance(string, str)
        assert len(string.split()) == 3

    inputs = [
        ("", commands.MissingRequiredArgument),
        ("string string string", None),
        ("1234 1234 1234", None),
    ]

    for args, excepted_exception in inputs:
        await bot.process_commands(args, excepted_exception)

    @bot.group
    async def test_sub(_) -> None:
        pass

    inputs = [
        ("", None),
        ("string string string", None),
        ("1234123412134", None),
        ("string", None),
    ]

    for args, excepted_exception in inputs:
        await bot.process_commands(args, excepted_exception)

    @test_sub.command
    async def sub(_, *, string: str) -> None:
        assert string == "cool string string string"

    inputs = [
        ("", commands.MissingRequiredArgument),
        ("cool string string string", None),
    ]

    for args, excepted_exception in inputs:
        await bot.process_commands(args, excepted_exception, command=sub)


@pytest.mark.asyncio
async def test_group_commands() -> None:
    bot = TestBot()

    @contextlib.contextmanager
    def writes_to_console(msg: str) -> Generator[None, None, None]:
        stdout = StringIO()
        with contextlib.redirect_stdout(stdout):
            yield

        assert msg == stdout.getvalue().strip()

    @bot.group
    async def parent(_) -> None:
        print("In parent")

    @parent.group
    async def child(_) -> None:
        print("In child")

    @child.command
    async def grand_child(_) -> None:
        print("In grand child")

    @parent.group
    async def other_child(_) -> None:
        print("In other child")

    assert bot.get_command("parent") is parent

    with writes_to_console("In parent"):
        await bot.process_commands(command=parent)

    assert bot.get_command("child") is None
    assert bot.get_command("parent child") is child

    with writes_to_console("In child"):
        await bot.process_commands(command=child)

    assert bot.get_command("grand_child") is None
    assert bot.get_command("child grand_child") is None
    assert bot.get_command("parent child grand_child") is grand_child

    with writes_to_console("In grand child"):
        await bot.process_commands(command=grand_child)

    assert bot.get_command("other_child") is None
    assert bot.get_command("parent other_child") is other_child

    with writes_to_console("In other child"):
        await bot.process_commands(command=other_child)
