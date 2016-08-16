from locale import getpreferredencoding
from os import environ
from subprocess import CalledProcessError
from subprocess import check_output
from tempfile import TemporaryFile

from docker_dev.exceptions import SubprocessError, \
    MissingCommandError


_SYSTEM_ENCODING = getpreferredencoding()


def run_command(command_name, command_args, additional_environ=None, **kwargs):
    command_parts = [command_name] + command_args
    additional_environ = additional_environ or {}
    command_environ = dict(additional_environ, PATH=environ['PATH'])
    command_stderr = TemporaryFile()
    try:
        command_stdout_bytes = check_output(
            command_parts,
            env=command_environ,
            stderr=command_stderr,
            **kwargs
        )
    except CalledProcessError as exc:
        command_stderr.seek(0)
        raise SubprocessError(
            command_parts,
            exc.returncode,
            command_stderr.read(),
        )
    except FileNotFoundError:
        raise MissingCommandError(command_name)
    else:
        command_stdout_str = command_stdout_bytes.decode(_SYSTEM_ENCODING)
        return command_stdout_str.rstrip()
